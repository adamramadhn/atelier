# CLAUDE.md

Claude Code entry point for this repository. Full skill routing lives in [AGENTS.md](AGENTS.md) — follow it for which skill to use for which request. This file only adds Claude Code–specific conventions.

Shortcuts for working inside this repo:

- Skill sources of truth: `skills/<name>/SKILL.md` (+ `references/`, `scripts/`, `library/` where present).
- Claude Code install for consumers: copy the skill folder into `.claude/skills/<name>/` of the consuming project. `skills/frontend-design/LICENSE.txt` must travel with its folder.
- Skill bodies are unedited upstream vendor copies; fix routing or docs only here, never inside a skill body. Provenance commits per skill are in `README.md`.
- Do not run `design-taste-frontend` and `impeccable`'s build/shape flow on the same artifact in one session (see anti-overlap guard in AGENTS.md).
