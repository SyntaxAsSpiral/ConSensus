import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class TestWorkshopAssemble(unittest.TestCase):
    def test_slice_and_whole_file_sources(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)

            src = base / "src.md"
            src.write_text(
                "\n".join(
                    [
                        "before",
                        "<!-- slice:one -->",
                        "SLICED",
                        "<!-- /slice -->",
                        "after",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/Demo/AGENTS.md"}],
                    "sources": [
                        {"slice": "one", "slice-file": "src.md"},
                        {"file": "src.md"},
                    ],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS.md")

            output_path = artifacts[0].abspath
            self.assertTrue(output_path.exists())
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("SLICED", text)
            self.assertIn("before", text)

    def test_agent_filename_disambiguation_when_requested(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            (base / "a.md").write_text("A\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=1,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "_total_sections": 2,
                    "_agent_disambiguator": "section2",
                    "target_locations": [{"path": "~/Demo/AGENTS.md"}],
                    "sources": [{"file": "a.md"}],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS-section2.md")

    def test_agent_directory_target_defaults_to_agents_md(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            (base / "a.md").write_text("A\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.codex/"}],  # directory form
                    "sources": [{"file": "a.md"}],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS.md")

    def test_agent_directory_target_defaults_to_claude_md(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            (base / "a.md").write_text("A\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.claude/"}],  # directory form
                    "sources": [{"file": "a.md"}],
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/CLAUDE.md")

    def test_sync_resolves_agent_directory_targets(self) -> None:
        import workshop.src.sync as sync
        from pathlib import Path

        sections = [
            sync.RecipeSection(
                recipe_file=Path("recipe.md"),
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.codex/"}],
                },
            ),
            sync.RecipeSection(
                recipe_file=Path("recipe.md"),
                index=1,
                config={
                    "name": "Demo2",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/.claude/"}],
                },
            ),
        ]

        items = sync.build_sync_items_from_sections(sections)
        expected_codex = str(Path.home() / ".codex" / "AGENTS.md").replace("\\", "/").lower()
        expected_claude = str(Path.home() / ".claude" / "CLAUDE.md").replace("\\", "/").lower()
        self.assertEqual(items[0].targets[0].replace("\\", "/").lower(), expected_codex)
        self.assertEqual(items[1].targets[0].replace("\\", "/").lower(), expected_claude)

    def test_project_skill_resolves_agents_dir_and_refuses_home(self) -> None:
        import workshop.src.assemble as assemble
        import workshop.src.sync as sync

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            project = Path(td) / "esocortex"
            tree = base / "skills" / "upstream" / "suite" / "skills" / "knap"
            tree.mkdir(parents=True)
            (tree / "SKILL.md").write_text("---\nname: knap\n---\n\n# Knap\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "knap",
                    "output_format": "project-skill",
                    "target_locations": [{"path": str(project / ".agents") + "/"}],
                    "sources": {"tree": "skills/upstream/suite/skills/knap"},
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].relpath, "skill/project/knap")
            self.assertTrue((artifacts[0].abspath / "SKILL.md").is_file())
            self.assertEqual(
                artifacts[0].targets,
                [str(project / ".agents" / "skills" / "knap") + "/"],
            )

            refused = assemble.resolve_project_skill_target("~/.agents/skills/knap/", "knap")
            self.assertIsNone(refused)
            self.assertEqual(
                assemble.resolve_project_skill_target(str(project) + "/", "knap"),
                str(project / ".agents" / "skills" / "knap") + "/",
            )

            sync_section = sync.RecipeSection(
                recipe_file=Path("recipe.md"),
                index=0,
                config=section.config,
            )
            items = sync.build_sync_items_from_sections([sync_section])
            self.assertEqual(items[0].deployment_id, "skill/project/knap")
            self.assertEqual(items[0].targets, artifacts[0].targets)
            self.assertEqual(
                assemble.resolve_project_skill_target(
                    "zk@100.77.90.79:~/.config/OpenRGB/.agents/", "openrgb"
                ),
                "zk@100.77.90.79:~/.config/OpenRGB/.agents/skills/openrgb/",
            )
            self.assertIsNone(
                assemble.resolve_project_skill_target("zk@100.77.90.79:~/.agents/", "openrgb")
            )


    def test_repeated_assemble_keeps_unconsumed_snapshot(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            staging = Path(td) / "staging"
            manifest = Path(td) / "manifest.md"
            snapshot = staging / ".previous-manifest.md"
            staging.mkdir()
            snapshot.write_bytes(b"OLD TARGETS\n")
            (staging / "skill").mkdir()
            manifest.write_text("NEW MANIFEST\n", encoding="utf-8")

            assemble.preserve_unconsumed_snapshot(staging, manifest)

            self.assertEqual(snapshot.read_bytes(), b"OLD TARGETS\n")
            self.assertFalse((staging / "skill").exists())

            snapshot.unlink()
            assemble.preserve_unconsumed_snapshot(staging, manifest)
            self.assertEqual(snapshot.read_text(encoding="utf-8"), "NEW MANIFEST\n")

    def test_sync_keeps_snapshot_until_purge_is_clear(self) -> None:
        import workshop.src.sync as sync

        with TemporaryDirectory() as td:
            root = Path(td)
            orphan = root / "gone"
            orphan.mkdir()
            snapshot = root / ".previous-manifest.md"
            snapshot.write_text("snapshot\n", encoding="utf-8")
            previous = {"skill/old": [str(orphan) + "/"]}
            current: dict = {}

            cleaned, purge_clear = sync.cleanup_orphaned_deployments(previous, current, dry_run=True)
            sync.consume_snapshot_after_purge(snapshot, purge_clear, dry_run=True)
            self.assertEqual(cleaned, 1)
            self.assertTrue(purge_clear)
            self.assertTrue(orphan.is_dir())
            self.assertTrue(snapshot.is_file())

            cleaned, purge_clear = sync.cleanup_orphaned_deployments(previous, current, dry_run=False)
            sync.consume_snapshot_after_purge(snapshot, purge_clear, dry_run=False)
            self.assertEqual(cleaned, 1)
            self.assertTrue(purge_clear)
            self.assertFalse(orphan.exists())
            self.assertFalse(snapshot.exists())

            snapshot.write_text("keep\n", encoding="utf-8")
            blocked = root / "blocked"
            blocked.mkdir()
            original = sync.shutil.rmtree

            def fail_rmtree(path):
                raise OSError("host down")

            sync.shutil.rmtree = fail_rmtree
            try:
                cleaned, purge_clear = sync.cleanup_orphaned_deployments(
                    {"skill/old": [str(blocked) + "/"]}, current, dry_run=False
                )
            finally:
                sync.shutil.rmtree = original
            sync.consume_snapshot_after_purge(snapshot, purge_clear, dry_run=False)
            self.assertEqual(cleaned, 0)
            self.assertFalse(purge_clear)
            self.assertTrue(blocked.is_dir())
            self.assertEqual(snapshot.read_text(encoding="utf-8"), "keep\n")


if __name__ == "__main__":
    unittest.main()
