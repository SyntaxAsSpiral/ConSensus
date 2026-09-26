---
title: "Documentation Consistency Check"
type: "prompt-template"
category: "documentation"
purpose: "Find and repair documentation drift against current canonical sources"
---

# Documentation Consistency Check

1. Check recent commits for context on terminology changes.
2. Identify the current canonical sources for this project or workspace, including `AGENTS.md`, `README.md`, current design documents, and the authoritative implementation.
3. Search all Markdown files for drift in terminology, architecture, or feature descriptions. Compare each claim against the canonical sources.
4. Check nested `AGENTS.md` and `README.md` files, other relevant project documentation, and code comments or docstrings that describe the same behavior.
5. Report outdated claims with file locations and source-grounded replacements. Say when the documentation is already consistent.
6. Automatically update confirmed inconsistencies found during the requested check. Leave no stale terminology behind. 🚮

Distinguish confirmed drift from ambiguity; do not invent replacement facts.
