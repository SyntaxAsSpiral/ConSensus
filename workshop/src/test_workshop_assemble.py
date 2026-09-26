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



if __name__ == "__main__":
    unittest.main()
