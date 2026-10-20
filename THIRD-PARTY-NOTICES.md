# Third-party notices

`atelier` unifies five open-source skills, vendored and kept byte-for-byte at a recorded
upstream commit. Each module keeps its upstream license and copyright; this notice maps
every vendored folder to its source.

| Module (`skills/atelier/references/…`) | Upstream | Vendored at | License |
|---|---|---|---|
| `design-taste-frontend` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (`skills/taste-skill`) | commit `63aba5f`, 2026-10-20 | MIT |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (`.claude/skills/impeccable`) | commit `e7d0f58`, 2026-10-20 | Apache-2.0 |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (`.claude/skills/ui-ux-pro-max`) | commit `56ea9cf`, 2026-10-15 | MIT |
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) (`skills/frontend-design`) | commit `dbd4588`, 2026-10-09 | Apache-2.0 (verbatim `LICENSE.txt` inside the folder) |
| `no-ai-slop` | [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (`skills/no-ai-slop`) | commit `000650b`, 2026-09-01 | MIT |

Notes:

- Upstream repositories are the source of truth for their licensing terms; the files above
  are unmodified copies and any dispute over terms resolves against the upstream text.
- Full upstream repositories other than the listed skill folders are **not** included here
  (including the impeccable engine source outside its skill folder, and other skills in
  `anthropics/skills`). Upstream commits recorded above serve provenance/audit purposes.
- This repository's own contribution — the routing entry point, module packaging, and
  documentation — is MIT licensed (see `LICENSE`), and does not relicense any module above.
