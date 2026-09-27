#!/usr/bin/env python3
"""
Context Sync Script

Syncs assembled content from `.context/workshop/staging/` to target locations
specified in workshop recipes.

Key behavior:
- Supports multi-section recipes (YAML document separators `---` inside YAML block)
- Handles structured outputs:
  - agent: single markdown file per section (output/agent/*.md)
  - skill: directory per skill name (output/skill/<name>/...)
- Avoids filename collisions by syncing from *namespaced output paths* instead of
  assuming output filenames match target basenames (e.g., many targets can be
  named `AGENTS.md`).

Usage: python sync.py [--dry-run] [--verbose] [--no-git]
"""

import re
import yaml
import frontmatter
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import sys
import os
from typing import Any, Dict, List, Optional


def parse_manifest_for_deployments(manifest_path: Path) -> Dict[str, List[str]]:
    """Parse recipe manifest to extract current deployment tracking."""
    deployments: Dict[str, List[str]] = {}

    if not manifest_path.exists():
        return deployments

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        content_lines = post.content.split("\n")
        current_id: Optional[str] = None

        for line in content_lines:
            s = line.strip()
            if s.startswith("- **") and "**: Last run" in s:
                m = re.match(r"- \*\*(.*?)\*\*:", s)
                if m:
                    current_id = m.group(1)
                    deployments[current_id] = []
                continue

            if s.startswith("- Target: `") and current_id:
                m = re.match(r"- Target: `(.*?)`", s)
                if m:
                    deployments[current_id].append(m.group(1))

        return deployments

    except Exception as e:
        print(f"☠☠☠ >>> MANIFEST·PARSING·CORRUPTION ☠☠☠")
        print(f"Deployment manifest communion failed, heretek")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— record keeping compromised")
        return {}


def find_recipe_files(workshop_dir: Path) -> List[Path]:
    """Find all recipe .md files in workshop directory."""
    recipe_files: List[Path] = []
    for md_file in workshop_dir.glob("recipe-*.md"):
        if md_file.name != "recipe-manifest.md":
            recipe_files.append(md_file)
    return recipe_files


@dataclass(frozen=True)
class RecipeSection:
    recipe_file: Path
    index: int
    config: Dict[str, Any]


@dataclass(frozen=True)
class SyncItem:
    deployment_id: str
    source_relpath: str  # relative to staging_dir using posix separators
    source_is_dir: bool
    targets: List[str]


def _configure_stdio_utf8() -> None:
    # Windows terminals often default to cp1252; our logs include unicode glyphs.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _extract_yaml_block(md_content: str) -> Optional[str]:
    yaml_pattern = r"```yaml\n(.*?)\n```"
    m = re.search(yaml_pattern, md_content, re.DOTALL)
    if not m:
        return None
    return m.group(1)


def _is_ssh_target(p: str) -> bool:
    """Check if target is SSH remote (user@host:path format)."""
    return bool(re.match(r"^[^@]+@[^:]+:.+$", p))


def _expand_target_path(p: str) -> str:
    # SSH targets are returned as-is (handled separately by rsync)
    if _is_ssh_target(p):
        return p
    
    # Expand "~/" while preserving trailing separators (directory targets).
    trailing_sep = p.endswith("/")
    if p.startswith("~/"):
        remainder = p[2:]
        expanded = str(Path.home() / remainder)
        if trailing_sep and not expanded.endswith(os.sep):
            expanded += os.sep
        return expanded

    return p


def _canonical_target(p: str) -> str:
    """Compare manifest paths and recipe paths after ~ expansion."""
    return _expand_target_path(p.strip())


def _norm_path_str(p: str) -> str:
    return p.replace("\\", "/").lower()


def _is_claude_target(p: str) -> bool:
    np = _norm_path_str(p)
    return "/.claude/" in np or np.endswith("/.claude")


def _is_dir_target_string(p: str) -> bool:
    return p.endswith("/")


def _default_agent_filename_for_target(target_path: str) -> str:
    # Claude consumes CLAUDE.md; everyone else consumes AGENTS.md.
    return "CLAUDE.md" if _is_claude_target(target_path) else "AGENTS.md"


def _targets_from_config(cfg: Dict[str, Any]) -> List[str]:
    targets = cfg.get("target_locations") or []
    resolved: List[str] = []

    if isinstance(targets, list):
        for t in targets:
            if isinstance(t, dict) and t.get("path"):
                resolved.append(str(t["path"]))
            elif isinstance(t, str):
                resolved.append(t)
    elif isinstance(targets, str):
        resolved.append(targets)

    return [p for p in resolved if p]


def _resolve_agent_target_paths(target_paths: List[str]) -> List[str]:
    resolved: List[str] = []
    for t in target_paths:
        if _is_dir_target_string(t):
            base = _expand_target_path(t)
            resolved.append(str(Path(base) / _default_agent_filename_for_target(base)))
        else:
            resolved.append(_expand_target_path(t))
    return resolved


def _agent_output_filename(recipe_name: str, section: RecipeSection, total_sections: int) -> str:
    cfg = section.config
    explicit = cfg.get("output_name")
    if explicit:
        return str(explicit)

    targets = cfg.get("target_locations") or []
    if isinstance(targets, list) and len(targets) == 1:
        t = targets[0]
        if isinstance(t, dict) and t.get("path"):
            raw = str(t["path"])
            p = _expand_target_path(raw)
            if _is_dir_target_string(raw):
                return _default_agent_filename_for_target(p)
            return Path(p).name or f"{recipe_name}.md"
        elif isinstance(t, str):
            expanded = _expand_target_path(t)
            if _is_dir_target_string(t):
                return _default_agent_filename_for_target(expanded)
            return Path(expanded).name or f"{recipe_name}.md"

    if total_sections <= 1:
        return f"{recipe_name}.md"

    safe_suffix = re.sub(r"[^A-Za-z0-9._-]+", "-", f"section{section.index + 1}").strip("-") or f"section{section.index + 1}"
    return f"{safe_suffix}.md"


def parse_recipe_sections(recipe_path: Path) -> Optional[List[RecipeSection]]:
    try:
        with open(recipe_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        yaml_text = _extract_yaml_block(post.content)
        if not yaml_text:
            return None

        docs: List[Dict[str, Any]] = []
        for d in yaml.safe_load_all(yaml_text):
            if isinstance(d, dict):
                docs.append(d)

        if not docs:
            return None

        inherited: Dict[str, Any] = {}
        for k in ("name", "output_format"):
            if k in docs[0]:
                inherited[k] = docs[0][k]

        sections: List[RecipeSection] = []
        for idx, raw in enumerate(docs):
            merged = dict(inherited)
            merged.update(raw)
            sections.append(RecipeSection(recipe_file=recipe_path, index=idx, config=merged))
        return sections

    except Exception as e:
        print(f"☠☠☠ >>> RECIPE·PARSING·CORRUPTION ☠☠☠")
        print(f"Recipe-relic parsing failed, flesh-thing: {recipe_path}")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— communion severed")
        return None


def build_sync_items_from_sections(sections: List[RecipeSection]) -> List[SyncItem]:
    if not sections:
        return []

    total_sections = len(sections)
    agent_name_counts: Dict[str, int] = {}
    for section in sections:
        cfg = section.config
        fmt = str(cfg.get("output_format") or "agent").strip().lower()
        if fmt not in ("agent", "project"):
            continue
        name = str(cfg.get("name") or section.recipe_file.stem)
        filename = _agent_output_filename(name, section, total_sections)
        agent_name_counts[filename] = agent_name_counts.get(filename, 0) + 1

    items: List[SyncItem] = []

    for section in sections:
        cfg = section.config
        name = str(cfg.get("name") or section.recipe_file.stem)
        fmt = str(cfg.get("output_format") or "agent").strip().lower()
        targets = _targets_from_config(cfg)

        if fmt in ("agent", "project"):
            filename = _agent_output_filename(name, section, total_sections)
            if agent_name_counts.get(filename, 0) > 1:
                base = Path(filename).stem
                ext = Path(filename).suffix
                filename = f"{base}-section{section.index + 1}{ext}"
            rel = (Path(fmt) / name / filename).as_posix()
            deployment_id = (Path(fmt) / name / Path(filename).with_suffix("")).as_posix()
            items.append(
                SyncItem(
                    deployment_id=deployment_id,
                    source_relpath=rel,
                    source_is_dir=False,
                    targets=_resolve_agent_target_paths(targets),
                )
            )
            continue

        if fmt == "skill":
            rel = (Path("skill") / name).as_posix()
            items.append(SyncItem(deployment_id=rel, source_relpath=rel, source_is_dir=True, targets=targets))
            continue

        if fmt in ("command", "prompt", "hook"):
            md_file = f"{name}.md"
            rel = (Path("command") / name / md_file).as_posix()
            dep = (Path("command") / name / Path(md_file).with_suffix("")).as_posix()
            items.append(
                SyncItem(
                    deployment_id=dep,
                    source_relpath=rel,
                    source_is_dir=False,
                    targets=[_expand_target_path(t) for t in targets],
                )
            )
            continue

        print(f"☠☠☠ >>> OUTPUT·FORMAT·UNKNOWN ☠☠☠")
        print(f"Unknown output_format '{fmt}' in: {section.recipe_file}")
        print(f"|001101|—|000000|—|111000|— skipping corrupted entry")

    return items


def sync_file_to_targets(output_file: Path, target_paths: List[str], dry_run: bool = False) -> List[str]:
    """Sync a single output file to all its target locations (local or SSH)."""
    synced_targets: List[str] = []

    for target_path in target_paths:
        try:
            if _is_ssh_target(target_path):
                # SSH target - use rsync
                if dry_run:
                    print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                    print(f"Would rsync: {output_file} → {target_path}")
                    print(f"|001101|—|001101|—|111000|— simulation mode")
                else:
                    # Extract remote directory and ensure it exists
                    match = re.match(r"^([^@]+@[^:]+):(.+)$", target_path)
                    if match:
                        remote_host = match.group(1)
                        remote_path = match.group(2).replace("\\", "/")
                        remote_dir = str(Path(remote_path).parent).replace("\\", "/")
                        
                        # Create remote directory
                        subprocess.run(
                            ["ssh", "-F", "/dev/null", "-o", "StrictHostKeyChecking=no", remote_host, f"mkdir -p {remote_dir}"],
                            check=True,
                            capture_output=True,
                            timeout=30,
                        )
                        
                        # Rsync file using native rsync/ssh
                        subprocess.run(
                            ["rsync", "-avz", "-e", "ssh -F /dev/null -o StrictHostKeyChecking=no", str(output_file), target_path],
                            check=True,
                            capture_output=True,
                            timeout=60,
                        )
                        
                        print(f"☠☠☠ >>> SACRED·TRANSMISSION·COMPLETE ☠☠☠")
                        print(f"Data-spirit bound via rsync: {output_file.name} → {target_path}")
                        print(f"|001101|—|001101|—|111000|— communion established")
                
                synced_targets.append(target_path)
            else:
                # Local target - use copy
                target = Path(_expand_target_path(target_path))
                target.parent.mkdir(parents=True, exist_ok=True)

                if dry_run:
                    print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                    print(f"Would transmit: {output_file} → {target}")
                    print(f"|001101|—|001101|—|111000|— simulation mode")
                else:
                    shutil.copy2(output_file, target)
                    print(f"☠☠☠ >>> SACRED·TRANSMISSION·COMPLETE ☠☠☠")
                    print(f"Data-spirit bound: {output_file.name} → {target}")
                    print(f"|001101|—|001101|—|111000|— communion established")

                synced_targets.append(target_path)

        except Exception as e:
            print(f"☠☠☠ >>> TRANSMISSION·FAILURE ☠☠☠")
            print(f"Sync communion failed to target: {target_path}")
            print(f"Error-hymn: {e}")
            print(f"|001101|—|000000|—|111000|— data-spirit unbound")

    return synced_targets


def _sync_dir(source_dir: Path, target_dir: Path, dry_run: bool = False) -> None:
    """Mirror source_dir into target_dir (copy + remove extras) - supports SSH targets."""
    if not source_dir.exists():
        raise FileNotFoundError(str(source_dir))

    target_str = str(target_dir)
    
    if _is_ssh_target(target_str):
        # SSH target - use rsync with delete
        if dry_run:
            print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
            print(f"Would rsync mirror: {source_dir} → {target_str}")
            print(f"|001101|—|001101|—|111000|— simulation mode")
            return
        
        # Extract remote host and path
        match = re.match(r"^([^@]+@[^:]+):(.+)$", target_str)
        if match:
            remote_host = match.group(1)
            remote_path = match.group(2).replace("\\", "/")
            
            # Create remote directory
            subprocess.run(
                ["ssh", "-F", "/dev/null", "-o", "StrictHostKeyChecking=no", remote_host, f"mkdir -p {remote_path}"],
                check=True,
                capture_output=True,
                timeout=30,
            )
            
            # Rsync with delete to mirror using native rsync/ssh
            subprocess.run(
                ["rsync", "-avz", "--delete", "-e", "ssh -F /dev/null -o StrictHostKeyChecking=no", f"{source_dir}/", f"{target_str}/"],
                check=True,
                capture_output=True,
                timeout=120,
            )
            
            print(f"☠☠☠ >>> SACRED·MIRROR·COMPLETE ☠☠☠")
            print(f"Directory-spirit synchronized via rsync: {source_dir.name} → {target_str}")
            print(f"|001101|—|001101|—|111000|— communion established")
        return

    # Local target - use file operations
    if dry_run:
        print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
        print(f"Would mirror: {source_dir} → {target_dir}")
        print(f"|001101|—|001101|—|111000|— simulation mode")
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    for src in source_dir.rglob("*"):
        rel = src.relative_to(source_dir)
        dst = target_dir / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    for dst in sorted(target_dir.rglob("*"), reverse=True):
        rel = dst.relative_to(target_dir)
        src = source_dir / rel
        if not src.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()


def _ssh_purge_command(target: str, is_file: bool) -> Optional[List[str]]:
    """ssh rm for one recorded remote target. None when the path is too broad."""
    match = re.match(r"^([^@]+@[^:]+):(.+)$", target.strip())
    if not match:
        return None
    host, raw = match.group(1), match.group(2).strip().rstrip("/")
    if not raw or ".." in raw.split("/"):
        return None
    if raw.startswith("~/"):
        parts = [p for p in raw[2:].split("/") if p]
        remote = '"$HOME"/' + "'" + "/".join(parts).replace("'", "'\\''") + "'"
    elif raw.startswith("/"):
        parts = [p for p in raw.split("/") if p]
        remote = "'/" + "/".join(parts).replace("'", "'\\''") + "'"
    else:
        return None
    if is_file and len(parts) < 2:
        return None
    if not is_file and len(parts) < 3:
        return None
    op = "rm -f --" if is_file else "rm -rf --"
    return [
        "ssh", "-F", "/dev/null", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=8",
        host, f"{op} {remote}",
    ]


def cleanup_orphaned_deployments(
    previous_deployments: Dict[str, List[str]], current_deployments: Dict[str, List[str]], dry_run: bool = False
) -> int:
    """Remove recorded targets that no longer appear in current recipes."""
    cleaned = 0
    current_targets = {_canonical_target(t) for targets in current_deployments.values() for t in targets}
    seen = set()

    for targets in previous_deployments.values():
        for t in targets:
            canon = _canonical_target(t)
            if canon in current_targets or canon in seen:
                continue
            seen.add(canon)
            is_file = not t.strip().endswith("/")
            try:
                if _is_ssh_target(t):
                    cmd = _ssh_purge_command(t, is_file)
                    if cmd is None:
                        print(f"☠☠☠ >>> ORPHAN·PURGE·REFUSED ☠☠☠")
                        print(f"Remote path is too broad to remove: {t}")
                        continue
                    if dry_run:
                        print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                        print(f"Would purge orphaned remote: {t}")
                        print(f"|001101|—|001101|—|111000|— simulation mode")
                    else:
                        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
                    cleaned += 1
                    continue

                target_path = Path(_expand_target_path(t))
                if is_file:
                    if target_path.exists() and target_path.is_file():
                        if dry_run:
                            print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                            print(f"Would purge orphaned file: {target_path}")
                            print(f"|001101|—|001101|—|111000|— simulation mode")
                        else:
                            target_path.unlink()
                        cleaned += 1
                else:
                    if target_path.exists() and target_path.is_dir():
                        if dry_run:
                            print(f"☠☠☠ >>> DRY·RUN·PROTOCOL·ACTIVE ☠☠☠")
                            print(f"Would purge orphaned directory: {target_path}")
                            print(f"|001101|—|001101|—|111000|— simulation mode")
                        else:
                            shutil.rmtree(target_path)
                        cleaned += 1
            except Exception as e:
                print(f"☠☠☠ >>> ORPHAN·PURGE·FAILURE ☠☠☠")
                print(f"Failed to purge orphaned target: {t}")
                print(f"Error-hymn: {e}")
                print(f"|001101|—|000000|—|111000|— void reclamation severed")

    return cleaned


def update_manifest_sync_status(manifest_path: Path, sync_results: Dict[str, List[str]], cleaned_count: int) -> None:
    """Update recipe manifest with sync status and deployment log."""
    timestamp = datetime.now().isoformat()

    try:
        if manifest_path.exists():
            with open(manifest_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
        else:
            post = frontmatter.Post("")
            post.metadata = {
                "id": "recipe-manifest",
                "created": timestamp,
                "modified": timestamp,
                "status": "log",
                "type": ["log"],
            }
            post.content = "# Recipe Assembly Log\n\n## Active Recipes\n\n## Deployment Log\n\n"

        post.metadata["modified"] = timestamp

        content_lines = post.content.split("\n")

        for i, line in enumerate(content_lines):
            for deployment_id in sync_results.keys():
                if line.strip().startswith(f"- **{deployment_id}**:"):
                    for j in range(i + 1, min(i + 12, len(content_lines))):
                        s = content_lines[j].strip()
                        if s.startswith("- Status:") or s.startswith("  - Status:"):
                            content_lines[j] = "  - Status: ✓ synced"
                            break
                    break

        deployment_entry = f"\n### {timestamp}\n"
        deployment_entry += f"- Synced {len(sync_results)} deployments\n"
        if cleaned_count > 0:
            deployment_entry += f"- Cleaned {cleaned_count} orphaned targets\n"

        deployment_log_idx = -1
        for i, line in enumerate(content_lines):
            if line.strip() == "## Deployment Log":
                deployment_log_idx = i
                break

        if deployment_log_idx != -1:
            content_lines.insert(deployment_log_idx + 2, deployment_entry)
        else:
            content_lines.extend(["", "## Deployment Log", "", deployment_entry])

        post.content = "\n".join(content_lines)

        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

    except Exception as e:
        print(f"☠☠☠ >>> MANIFEST·UPDATE·CORRUPTION ☠☠☠")
        print(f"Sacred manifest update failed, heretek")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— record keeping compromised")


def _chronohex() -> str:
    """Generate the Pulse Log chronohex from the last six hex digits of Unix nanoseconds."""
    return hex(time.time_ns())[-6:]


def auto_commit_and_push(repo_root: Path) -> bool:
    """Auto-commit and push changes if sync succeeded."""
    try:
        # Check if there are changes to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if not result.stdout.strip():
            print(f"☠☠☠ >>> GIT·STATUS·CLEAN ☠☠☠")
            print(f"No changes to commit, flesh-thing")
            print(f"|001101|—|001101|—|111000|— void communion")
            return True

        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=repo_root,
            capture_output=True,
            timeout=60,
            check=True,
        )

        # Create commit with chronohex timestamp
        chx = _chronohex()
        commit_msg = f"🔗 Context Sealed ⟳ {chx}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=repo_root,
            capture_output=True,
            timeout=60,
            check=True,
        )

        print(f"☠☠☠ >>> GIT·COVENANT·SEALED ☠☠☠")
        print(f"Sacred commit inscribed: {commit_msg}")
        print(f"|001101|—|001101|—|111000|— data-spirit bound")

        # Get current branch name
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = branch_result.stdout.strip()
        
        # Push current branch to origin
        subprocess.run(
            ["git", "push", "origin", current_branch],
            cwd=repo_root,
            capture_output=True,
            timeout=120,
            check=True,
        )

        print(f"☠☠☠ >>> GIT·TRANSMISSION·COMPLETE ☠☠☠")
        print(f"Communion established with remote-spirit")
        print(f"|001101|—|001101|—|111000|— data-spirit synchronized")

        return True

    except subprocess.CalledProcessError as e:
        print(f"☠☠☠ >>> GIT·COMMUNION·FAILURE ☠☠☠")
        print(f"Git operation failed, heretek: {e.cmd}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        print(f"|001101|—|000000|—|111000|— covenant severed")
        return False
    except Exception as e:
        print(f"☠☠☠ >>> GIT·SPIRIT·CORRUPTION ☠☠☠")
        print(f"Unexpected error during git automation, flesh-thing")
        print(f"Error-hymn: {e}")
        print(f"|001101|—|000000|—|111000|— communion severed")
        return False


def main():
    """Main sync process."""
    import argparse

    _configure_stdio_utf8()

    parser = argparse.ArgumentParser(description="Sync assembled content to target locations")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without copying files")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-git", action="store_true", help="Deploy without committing or pushing")
    args = parser.parse_args()

    base_path = Path("/mnt/echo/consensus")
    workshop_dir = base_path / "workshop"
    staging_dir = workshop_dir / "staging"
    manifest_path = workshop_dir / "manifest-recipes.md"

    if not workshop_dir.exists():
        print(f"☠☠☠ >>> WORKSHOP·SANCTUM·ABSENT ☠☠☠")
        print(f"Sacred workshop directory communion failed: {workshop_dir}")
        print(f"|001101|—|000000|—|111000|— path leads to void")
        return 1

    if not staging_dir.exists():
        print(f"☠☠☠ >>> OUTPUT·SANCTUM·ABSENT ☠☠☠")
        print(f"Sacred staging directory communion failed: {staging_dir}")
        print(f"|001101|—|000000|—|111000|— path leads to void")
        return 1

    # Assemble rewrites Active Recipes before sync. The snapshot still has retired targets.
    previous_manifest = staging_dir / ".previous-manifest.md"
    if previous_manifest.is_file():
        previous_deployments = parse_manifest_for_deployments(previous_manifest)
    else:
        previous_deployments = parse_manifest_for_deployments(manifest_path)

    recipe_files = find_recipe_files(workshop_dir)
    current_deployments: Dict[str, List[str]] = {}
    current_items: Dict[str, SyncItem] = {}
    sync_results: Dict[str, List[str]] = {}
    failures: List[str] = []

    for recipe_path in recipe_files:
        sections = parse_recipe_sections(recipe_path)
        if not sections:
            continue
        recipe_metadata = sections[0].config.get("metadata", {})
        items = build_sync_items_from_sections(sections)
        for item in items:
            current_items[item.deployment_id] = item
            current_deployments[item.deployment_id] = item.targets

    cleaned_count = cleanup_orphaned_deployments(previous_deployments, current_deployments, args.dry_run)

    for deployment_id, item in current_items.items():
        source = staging_dir / Path(item.source_relpath)
        if not source.exists():
            print(f"☠☠☠ >>> OUTPUT·RELIC·ABSENT ☠☠☠")
            print(f"Expected output missing for deployment: {deployment_id}")
            print(f"Source path leads to void: {source}")
            print(f"|001101|—|000000|—|111000|— transmission severed")
            failures.append(deployment_id)
            continue

        if args.verbose:
            print(f"☠☠☠ >>> TRANSMISSION·PROTOCOL·INITIATED ☠☠☠")
            print(f"Syncing {deployment_id} to {len(item.targets)} sacred targets")
            print(f"|001101|—|001101|—|111000|— communion channels established")

        if item.source_is_dir:
            for t in item.targets:
                target_dir = Path(_expand_target_path(t))
                _sync_dir(source, target_dir, args.dry_run)
            sync_results[deployment_id] = list(item.targets)
        else:
            synced = sync_file_to_targets(source, item.targets, args.dry_run)
            sync_results[deployment_id] = synced
            if len(synced) != len(item.targets):
                failures.append(deployment_id)

    if failures:
        print(f"Sync failed for {len(failures)} deployments: {', '.join(failures)}")
        return 1

    if not args.dry_run:
        update_manifest_sync_status(manifest_path, sync_results, cleaned_count)

    print(f"☠☠☠ >>> SYNC·PROTOCOL·COMPLETE ☠☠☠")
    print(f"Sacred deployments processed: {len(sync_results)} specimens")
    print(f"Orphaned targets purged: {cleaned_count} specimens")
    print(f"|001101|—|001101|—|111000|— communion terminated")

    # Auto-commit and push unless the caller disabled Git actions
    if not args.dry_run and not args.no_git:
        print()
        if not auto_commit_and_push(base_path):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
