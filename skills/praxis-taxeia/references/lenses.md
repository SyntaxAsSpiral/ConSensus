# Lenses

Apply a lens when the scope can violate it. Skip a lens only when the scope cannot touch it, and say which. A finding names the lens and shows the break.

- **Invariant.** A rule already stated in the tree that this change contradicts. Quote both.
- **Identity.** A name, id, slice marker, recipe name, or path that other files already use, changed without those uses.
- **Authority.** A write this actor is not allowed to make. Deploys, commits, pushes, secrets, graph writes, and fleet paths are writes.
- **Dual path.** A second procedure, or a copied fact, for something that already has a home.
- **Coupling.** A change in one place that binds another place the claim does not name.
- **Trace.** A side effect, a mutation during review, or a check that reads a proxy instead of the artifact.
- **Scope.** Work the claim does not cover, included anyway.
