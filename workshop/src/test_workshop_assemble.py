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

    def test_audience_keeps_unsliced_text_and_each_matching_slice(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)
            src = base / "principles.md"
            src.write_text(
                "\n".join(
                    [
                        "shared",
                        "<!-- slice:local -->",
                        "LOCAL-1",
                        "<!-- /slice -->",
                        "<!-- slice:local -->",
                        "LOCAL-2",
                        "<!-- /slice -->",
                        "<!-- slice:both -->",
                        "BOTH",
                        "<!-- /slice -->",
                        "<!-- slice:remote -->",
                        "REMOTE-1",
                        "<!-- /slice -->",
                        "<!-- slice:remote -->",
                        "REMOTE-2",
                        "<!-- /slice -->",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            def rendered(audience: str) -> str:
                section = assemble.RecipeSection(
                    recipe_file=Path(td) / "recipe.md",
                    index=0,
                    config={
                        "name": "Demo",
                        "output_format": "agent",
                        "target_locations": [{"path": "~/Demo/AGENTS.md"}],
                        "sources": [{"file": "principles.md", "audience": audience}],
                    },
                )
                artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
                self.assertEqual(len(artifacts), 1)
                return artifacts[0].abspath.read_text(encoding="utf-8")

            local = rendered("local")
            self.assertEqual(local, "shared\n\nLOCAL-1\n\nLOCAL-2\n\nBOTH\n")
            self.assertNotIn("REMOTE", local)
            self.assertNotIn("slice:", local)

            remote = rendered("remote")
            self.assertEqual(remote, "shared\n\nBOTH\n\nREMOTE-1\n\nREMOTE-2\n")
            self.assertNotIn("LOCAL", remote)
            self.assertNotIn("slice:", remote)

            bad = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": [{"path": "~/Demo/AGENTS.md"}],
                    "sources": [{"file": "principles.md", "audience": "nix"}],
                },
            )
            self.assertEqual(assemble.build_output_artifacts(bad, base, out, dry_run=False), [])

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


    def test_fleet_target_also_stages_skill_fleet_copy(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            tree = base / "skills" / "git"
            tree.mkdir(parents=True)
            (tree / "SKILL.md").write_text("---\nname: git\n---\n\n# Git\n", encoding="utf-8")

            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config={
                    "name": "git",
                    "output_format": "skill",
                    "target_locations": [
                        {"path": "~/.agents/skills/git/"},
                        {"path": "fleet:/home/box/agent-data/workflows/git/"},
                    ],
                    "sources": {"tree": "skills/git"},
                },
            )

            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=False)
            self.assertEqual([a.relpath for a in artifacts], ["skill/global/git", "skill/fleet/git"])
            self.assertEqual((out / "skill" / "fleet" / "git" / "SKILL.md").read_text(encoding="utf-8"), (tree / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(
                artifacts[0].targets,
                [
                    assemble._expand_target_path("~/.agents/skills/git/"),
                    f"{assemble.FLEET_SSH_HOST}:/home/box/agent-data/workflows/git/",
                ],
            )
            self.assertEqual(artifacts[1].targets, [])

    def test_host_sync_selects_one_machine(self) -> None:
        import workshop.src.sync as sync

        targets = [
            "~/.agents/skills/git/",
            "zk@100.115.135.104:~/.agents/skills/git/",
            "fleet:/home/box/agent-data/workflows/git/",
            "/mnt/echo/consensus/AGENTS.md",
        ]
        self.assertEqual(
            sync._select_host_targets(targets, "adeck"),
            ["~/.agents/skills/git/", "/mnt/echo/consensus/AGENTS.md"],
        )
        self.assertEqual(
            sync._select_host_targets(targets, "fleet"),
            ["fleet:/home/box/agent-data/workflows/git/"],
        )
        self.assertEqual(
            sync._select_host_targets(targets, "nxiz"),
            ["zk@100.115.135.104:~/.agents/skills/git/"],
        )
        cleaned, purge_clear = sync.cleanup_orphaned_deployments(
            {
                "old": [
                    "zk@100.105.160.85:/home/box/agent-data/workflows/old/",
                    "zk@100.115.135.104:~/.agents/skills/old/",
                ]
            },
            {},
            dry_run=True,
            host="fleet",
        )
        self.assertEqual(cleaned, 1)
        self.assertTrue(purge_clear)

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

    def test_mixed_targets_translate_fleet_prefix(self) -> None:
        import workshop.src.assemble as assemble
        import workshop.src.sync as sync

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir()
            (base / "a.md").write_text("A\n", encoding="utf-8")
            config = {
                "name": "Demo",
                "output_format": "agent",
                "target_locations": [
                    {"path": "fleet:/workspace/AGENTS.md"},
                    {"path": "~/Demo/AGENTS.md"},
                    "fleet:/workspace/ROLES.md",
                ],
                "sources": [{"file": "a.md"}],
            }
            section = assemble.RecipeSection(
                recipe_file=Path(td) / "recipe.md",
                index=0,
                config=config,
            )
            artifacts = assemble.build_output_artifacts(section, base, out, dry_run=True)
            expected = [
                f"{assemble.FLEET_SSH_HOST}:/workspace/AGENTS.md",
                str(Path.home() / "Demo" / "AGENTS.md"),
                f"{assemble.FLEET_SSH_HOST}:/workspace/ROLES.md",
            ]
            self.assertEqual(assemble.FLEET_SSH_HOST, sync.FLEET_SSH_HOST)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].relpath, "agent/Demo/AGENTS.md")
            self.assertEqual(artifacts[0].targets, expected)

            items = sync.build_sync_items_from_sections(
                [sync.RecipeSection(recipe_file=Path("recipe.md"), index=0, config=config)]
            )
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].source_relpath, "agent/Demo/AGENTS.md")
            self.assertEqual(items[0].targets, expected)

    def test_fleet_only_targets_resolve_ssh(self) -> None:
        import workshop.src.assemble as assemble
        import workshop.src.sync as sync

        with TemporaryDirectory() as td:
            base = Path(td) / "base"
            out = Path(td) / "out"
            base.mkdir()
            (base / "a.md").write_text("A\n", encoding="utf-8")
            for locations in (
                [{"path": "fleet:/workspace/AGENTS.md"}],
                ["fleet:/workspace/AGENTS.md"],
            ):
                config = {
                    "name": "Demo",
                    "output_format": "agent",
                    "target_locations": locations,
                    "sources": [{"file": "a.md"}],
                }
                section = assemble.RecipeSection(
                    recipe_file=Path(td) / "recipe.md",
                    index=0,
                    config=config,
                )
                artifacts = assemble.build_output_artifacts(section, base, out, dry_run=True)
                expected = [f"{assemble.FLEET_SSH_HOST}:/workspace/AGENTS.md"]
                self.assertEqual(len(artifacts), 1)
                self.assertEqual(artifacts[0].relpath, "agent/Demo/Demo.md")
                self.assertEqual(artifacts[0].targets, expected)

                items = sync.build_sync_items_from_sections(
                    [sync.RecipeSection(recipe_file=Path("recipe.md"), index=0, config=config)]
                )
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0].source_relpath, "agent/Demo/Demo.md")
                self.assertEqual(items[0].targets, expected)


    def test_stalled_upstream_pull_does_not_stop_the_run(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td)
            for name in ("stuck", "fine"):
                (base / "skills" / "upstream" / name / ".git").mkdir(parents=True)

            def fake(repo: Path, timeout: float = assemble.UPSTREAM_PULL_TIMEOUT_S):
                if repo.name == "stuck":
                    return 124, "", "stalled"
                return 0, "up to date", ""

            original = assemble._pull_repo
            assemble._pull_repo = fake
            try:
                code = assemble.pull_upstream_repos(base, dry_run=False)
            finally:
                assemble._pull_repo = original
            self.assertEqual(code, 0)

    def test_failed_upstream_pull_still_stops_the_run(self) -> None:
        import workshop.src.assemble as assemble

        with TemporaryDirectory() as td:
            base = Path(td)
            (base / "skills" / "upstream" / "broken" / ".git").mkdir(parents=True)

            def fake(repo: Path, timeout: float = assemble.UPSTREAM_PULL_TIMEOUT_S):
                return 1, "", "not possible to fast-forward"

            original = assemble._pull_repo
            assemble._pull_repo = fake
            try:
                code = assemble.pull_upstream_repos(base, dry_run=False)
            finally:
                assemble._pull_repo = original
            self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
