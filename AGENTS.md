# AGENTS.md

Agent-facing instructions for this repository: a single combined skill, **`skills/atelier`**, that unifies six vendored upstream modules under one entry point.

**The routing source of truth is `skills/atelier/SKILL.md`.** Read it first for any design/UI/copy request — it decides which module (under `references/<module>/SKILL.md`) governs the task. This file only covers repository-level hygiene.

- **Do not edit module bodies.** Everything under `skills/atelier/references/` is an unedited upstream vendor copy with its own provenance commit (see README.md). Fix routing, docs, or this file only.
- **Do not promote a module back into a standalone skill.** The one-skill model is intentional; the entry point's anti-overlap guard depends on it.
- **Skill folder is self-contained.** It only needs its own directory tree; copy it whole (`references/` included) to install into any harness's skills directory.
- **Update policy:** manual-review-only upstream sync — diff each module folder against its upstream commit before merging; never auto-update.
- **Auto-trigger in consuming projects:** add this line to the consumer project's `AGENTS.md`/`CLAUDE.md` so UI work routes here even in agents without a skill loader: `Any UI/front-end task (pages, components, styling, layouts, UI copy): read .claude/skills/atelier/SKILL.md and follow its routing before editing.`
