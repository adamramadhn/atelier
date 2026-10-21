# Contributing

Thanks for considering a contribution! `atelier` unifies six open-source design skills
behind one routing entry point. Contributions that respect the packaging model are welcome.

## How this repo is structured

- **`skills/atelier/SKILL.md`** — the only "sticky" file: routing, anti-overlap guard,
  reference-URL intake, environment notes. This is where most contributions should land.
- **`skills/atelier/references/<module>/`** — **vendored upstream copies, byte-for-byte**,
  each pinned to a recorded commit (see `THIRD-PARTY-NOTICES.md`). These are **never edited
  manually** — not to fix a typo, not to "clean up" anything. Their value is diffability
  against upstream.
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `THIRD-PARTY-NOTICES.md` — documentation layer.

## What to contribute

1. **Routing fixes** — a task that routes to the wrong module, or an overlap the guard misses:
   open an issue with the exact request and the (wrong) behavior, then a PR against `SKILL.md`.
2. **New intake flows** (like reference-URL intake) — document the procedure, keep it
   harness-agnostic, and wire it only through the entry point, never inside a module.
3. **Upstream module updates** — see the exact procedure below.
4. **Documentation** — unclear README/AGENTS/CLAUDE text.

## What won't be accepted

- Direct edits inside `skills/atelier/references/**` (except a wholesale official upstream
  refresh, done as one commit, one module).
- Adding another skill that overlaps an existing module (e.g. a second landing-page
  art-direction skill) — deduplicate against the table in `README.md` first.
- Module bodies translated into the entry point, or vice versa.

## Updating a vendored module (the only allowed edit in `references/`)

1. Shallow-clone the upstream repo at the commit you want and `diff -r` it against the
   vendored folder.
2. Review **every** change in the diff — vendored code runs in agent contexts and can prompt
   the agent to run scripts or install tooling, so track what the new body asks agents to do.
3. Bump the commit row in `THIRD-PARTY-NOTICES.md` (and `README.md` provenance table) in the
   same PR. PRs that change `references/**` without a provenance bump, or vice versa, are
   rejected by definition.
4. Prefer an upstream PR over a vendored patch when the problem is in the module itself —
   then re-vendor after it merges.

## PR checklist

- [ ] `python3 scripts/smoke-test.py` passes (frontmatter parse, `node --check`, python syntax, banned-pattern scan)
- [ ] No changes inside `skills/atelier/references/**` (or a provenance-row update accompanies one)
- [ ] `SKILL.md` frontmatter still parses (4 keys: `name`, `description`, `user-invocable`, `argument-hint`)
- [ ] The routing table in README.md and the module table in SKILL.md remain in sync
- [ ] Docs use the same module names as the folders
