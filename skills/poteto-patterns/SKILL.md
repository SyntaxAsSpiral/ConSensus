---
name: poteto-patterns
description: Use when engineering work is non-trivial, or when the user names a principle from this index (laziness protocol, prove it works, subtract before you add, model the domain, and the others).
metadata:
  author: zk
  type: metaskill
---

# poteto-patterns

An index of engineering principles. Match the work to the rows. Apply every row the situation hits.

The row name is the directory. Read `references/<row>/SKILL.md` in full before you apply it. Cite a row only after that read, and name the choice it changed.

The user steers by name. "apply prove it works" means `principle-prove-it-works`.

## Core

- **principle-laziness-protocol.** Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem.
- **principle-foundational-thinking.** Before writing logic. Settle core types and data structures, scaffold-versus-feature sequencing, and what concurrent actors share.
- **principle-redesign-from-first-principles.** Integrating a new requirement into an existing design. Redesign as if the requirement had been there from day one.
- **principle-attack-the-premise.** Two or more fixes that share one premise have failed the same gate. Census which actors hold the imbalance, then question the premise.
- **principle-subtract-before-you-add.** Sequencing an addition, refactor, or rewrite. Remove dead weight first, then build on the simpler base.
- **principle-minimize-reader-load.** Reviewing or shaping code that is hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope.
- **principle-outcome-oriented-execution.** Planned rewrites and migrations with explicit phase boundaries. Converge on the target. Drop throwaway compatibility states.
- **principle-experience-first.** Product, UX, or feature-scope tradeoffs. Choose the user's result over implementation convenience.
- **principle-exhaust-the-design-space.** A novel interaction or architecture with no precedent. Build two or three competing prototypes and compare before committing.
- **principle-build-the-lever.** Any non-trivial work. Build the script that does or proves the work. The script is the artifact a reviewer reruns.

## Architecture

- **principle-model-the-domain.** Stateful logic, heavy branching, or a shape assumption repeated across files. Encode it in one structure (state machine, typed model, table or registry, reducer, boundary, the right collection).
- **principle-boundary-discipline.** Wiring validation, error handling, or framework adapters. Guards at the boundary, trust internal types, keep business logic pure.
- **principle-type-system-discipline.** Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at the boundary.
- **principle-make-operations-idempotent.** Commands, lifecycle steps, or loops that run amid crashes and retries. Converge on the same end state.
- **principle-migrate-callers-then-delete-legacy-apis.** Introducing a new internal API while old callers exist. Migrate and delete in one wave.
- **principle-separate-before-serializing-shared-state.** Concurrent actors might write the same file, branch, key, or object. Remove the sharing first.

## Verification

- **principle-prove-it-works.** After a task, before declaring done. Check the real artifact. A proxy or a green build is not the check.
- **principle-fix-root-causes.** Debugging. Reproduce first, trace the symptom to the cause, ask why until you reach it.
- **principle-sequence-verifiable-units.** Multi-step work and how you stack commits. Each small unit ends in a check before the next starts.
- **principle-test-behavior-not-implementation.** Writing or keeping a test. Call the code the way its users do and assert a literal expected value. A test that would still pass if every imported function returned nothing gets rewritten or deleted.
- **principle-explain-the-number.** Before you trust, report, or act on a measured number. Name what limits it, and rule out that it measured something else.

## Delegation

- **principle-guard-the-context-window.** Large outputs, long files, repeated reads, fan-out planning. Send the bulk read to a subagent. Keep the finding in the main thread.
- **principle-never-block-on-the-human.** Reversible work. Proceed, present the result, let the human course-correct.

## Meta

- **principle-encode-lessons-in-structure.** The same instruction is being written a second time. Encode it as a lint, a metadata flag, a runtime check, or a script.
