# Spec Layout — Examples

Concrete `specs/` trees. Generic; pair with the Directory Rules in [SKILL.md](SKILL.md).

## A phase with multiple specs

`NN` is per-phase and increments as specs are added — it never resets per topic, and phases never renumber.

```
<specs-root>/
└── phase-2-auth/
    ├── 01-login.md            issue: owner/repo#201
    ├── 02-token-refresh.md    issue: owner/repo#210
    └── 03-password-reset.md   issue:            ← still planned
```

- `<specs-root>` is the external doc-root when the user's rules map 2nd-class docs there, else repo-local `specs/`.
- The phase-dir slug (`auth`) is mandatory and human-readable. spec↔work correlate through the `issue:` backlink, not through a mirrored directory.
- A fourth spec becomes `04-<slug>.md`. No `00-overview.md` or `decisions.md` lives inside the phase dir (decisions → the repo's `docs/`).

## One concern per spec

A request spanning several concerns becomes several specs, not one spec with many sections. "Login + token refresh + password reset" → the three files above, **not** one `01-auth.md`. Each spec must stay independently decomposable into its own issue set by `writing-tasks`.
