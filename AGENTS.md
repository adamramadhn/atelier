# AGENTS.md

Agent-facing instructions for this repository: a single combined skill, **`skills/design-suite`**, that unifies five vendored upstream modules under one entry point.

**The routing source of truth is `skills/design-suite/SKILL.md`.** Read it first for any design/UI/copy request — it decides which module (under `references/<module>/SKILL.md`) governs the task. This file only covers repository-level hygiene.

- **Do not edit module bodies.** Everything under `skills/design-suite/references/` is an unedited upstream vendor copy with its own provenance commit (see README.md). Fix routing, docs, or this file only.
- **Do not promote a module back into a standalone skill.** The one-skill model is intentional; the entry point's anti-overlap guard depends on it.
- **Skill folder is self-contained.** It only needs its own directory tree; copy it whole (`references/` included) to install into any harness's skills directory.
- **Update policy:** manual-review-only upstream sync — diff each module folder against its upstream commit before merging; never auto-update.
