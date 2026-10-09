---
name: praxis-taxeia
description: Use when the user asks for praxis-taxeia, an adversarial review, a falsifier pass, or to stress-test a diff, design, or claim before accepting it. Also use when a bot runs that review by launching local coding agents.
---

# Taxeia praxis

Lathe until only the real remains. Falsify first. The product is a decision, not a patch.

The lead writes the claim and the decision. Local CLI agents run the ablations. A person in the turn and a headless bot follow the same steps.

This pass sees structure. It does not bless meaning, tone, or prose. Documentation drift and slop belong to inquisition.

Do not edit the artifact. Do not deploy, commit, or push as part of the review.

## Procedure

1. **Scope.** The diff, files, or text the user named. If they named no base, use the staged and unstaged work in the current checkout. Leave the rest of the tree alone.

2. **Claim.** One paragraph: what this artifact asserts is true, and what accepting it would allow. Take it from the user's message, the commit messages, and the diff. If you cannot write the claim, ask. A caller with nobody to ask records ELEVATE and stops.

3. **Premise.** One sentence every part of the change assumes. Write it before either ablation.

4. **Brief.** Fill [references/brief.md](references/brief.md). Append the full text of [references/lenses.md](references/lenses.md).

5. **Two ablations.** Spawn both reviewers as in [references/runners.md](references/runners.md). Neither sees the other until both have returned.

6. **Graft.** Keep disagreements. Do not average them into a milder finding. A missing pass cannot support ACCEPT.

7. **Decide.** Exactly one:
   - **ACCEPT.** Both passes returned, and nothing in them breaks the claim.
   - **PROCEED.** The repairs are bounded and listed. Do not apply them.
   - **HONOR_REFUSAL.** Accepting would break an invariant, an authority boundary, or the claim. Stop. This refuses the artifact. It is not a refusal to answer the user.
   - **ELEVATE.** The passes contradict each other, a pass is missing and the one you have does not already show the break, or the missing fact belongs to the operator.

## Report

### Claim

The paragraph from step 2.

### Premise

The sentence from step 3.

### Findings

Each one: lens, evidence, which reviewer. A disagreement stays as two findings.

### Decision

The word, then the repairs or the refusal in a few lines. End with: this decision is structural.

### Seats

One line per reviewer: who ran it, or that the seat was absent.

### Left on the bench

Nits that did not move the decision. One line each.
