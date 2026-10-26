# Third-party notices

`atelier` unifies six open-source skills, vendored and kept byte-for-byte at a recorded
upstream commit. Each module keeps its upstream license and copyright; this notice maps
every vendored folder to its source.

| Module (`skills/atelier/references/…`) | Upstream | Vendored at | License |
|---|---|---|---|
| `design-taste-frontend` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (`skills/taste-skill`) | commit `12af471`, 2026-10-26 | MIT |
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (`.claude/skills/impeccable`) | commit `3671d50`, 2026-10-26 | Apache-2.0 |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (`.claude/skills/ui-ux-pro-max`) | commit `d14efff`, 2026-10-26 | MIT |
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills) (`skills/frontend-design`) | commit `dbd4588`, 2026-10-09 | Apache-2.0 (verbatim `LICENSE.txt` inside the folder) |
| `no-ai-slop` | [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (`skills/no-ai-slop`) | commit `000650b`, 2026-09-01 | MIT |
| `motion-design` | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) (`skills/motion-design`) | commit `f9a8a04`, 2026-10-21 | MIT |

Notes:

- Upstream repositories are the source of truth for their licensing terms; the files above
  are unmodified copies and any dispute over terms resolves against the upstream text.
- Full upstream repositories other than the listed skill folders are **not** included here
  (including the impeccable engine source outside its skill folder, and other skills in
  `anthropics/skills`). Upstream commits recorded above serve provenance/audit purposes.
- This repository's own contribution — the routing entry point, module packaging, and
  documentation — is MIT licensed (see `LICENSE`), and does not relicense any module above.
