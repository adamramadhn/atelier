# design-skills

Satu skill gabungan bernama **`atelier`** yang menggabungkan 5 sumber upstream menjadi 1 kesatuan: satu `SKILL.md` entry point dengan routing internal, dan 5 modul vendored byte-per-byte di bawahnya sebagai `references/`.

Repo ini private, untuk konsumsi pribadi (attribution lisensi di tabel di bawah).

## Struktur

```
skills/atelier/
  SKILL.md                 ← entry point: routing 5 modul + guard anti-overlap + environment
  references/
    ui-ux-pro-max/         ← upstream body utuh (data CSV, scripts, SKILL.md)
    design-taste-frontend/ ← upstream body utuh (library, scripts, assets, SKILL.md)
    impeccable/            ← upstream body utuh (reference/, scripts/, SKILL.md)
    frontend-design/       ← upstream body utuh + LICENSE.txt Anthropic
    no-ai-slop/            ← upstream body utuh (SKILL, eval)
README.md                  ← dokumen ini (sumber provenance)
AGENTS.md                  ← pintu repo untuk agent generik → menunjuk SKILL.md
CLAUDE.md                  ← pintu repo untuk Claude Code → menunjuk SKILL.md
```

Skill yang terpasang adalah `atelier` saja — modulnya bukan skill terpisah, tapi dimuat on-demand dari `references/<modul>/SKILL.md` sesuai routing entry point.

## Provenance

| Module di `references/` | Upstream | Commit diambil | Lisensi |
|---|---|---|---|
| `design-taste-frontend` | github.com/Leonxlnx/taste-skill (`skills/taste-skill`) | `b9ca2fd` (2026-10-19) | MIT |
| `impeccable` | github.com/pbakaus/impeccable (`.claude/skills/impeccable`) | `0665bd8` (2026-10-19) | Apache-2.0 |
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill (`.claude/skills/ui-ux-pro-max`) | `56ea9cf` (2026-10-15) | MIT |
| `frontend-design` | github.com/anthropics/skills (`skills/frontend-design`) | `dbd4588` (2026-10-09) | Lisensi Anthropic (attribution; lihat LICENSE.txt di folder melalui referensi) |
| `no-ai-slop` | github.com/petergyang/no-ai-slop (`skills/no-ai-slop`) | `000650b` (2026-09-01) | MIT |

Yang sengaja TIDAK diambil:
- `taste-skill`: v1, v2-experimental, gpt-taste, stitch (deprecated/varian), style variants opt-in (soft/minimalist/brutalist), dan 4 skill pointer "moved" (brandkit, imagegen-web/mobile, image-to-code → repo `Leonxlnx/imagegen-skills`).
- `impeccable` & `ui-ux-pro-max-skill`: full repo tidak diambil, hanya folder skill (engine impeccable tetap di dalam folder modulnya).
- sisanya `anthropics/skills` (canvas-design, web-artifacts-builder, document-skills, dll) di luar scope.

## Instalasi

Salin seluruh `skills/atelier/` ke direktori skills harness (`~/.claude/skills/atelier/`, `.agents/skills/atelier/`, dll) — folder `references/` harus ikut karena modul dimuat dari sana. Untuk repositori konsumen yang ingin routing/panduan project-level, copy bagian ini:

```
AGENTS.md             → <project>/AGENTS.md
CLAUDE.md             → <project>/CLAUDE.md
skills/atelier/  → <project>/.claude/skills/atelier/
```

## Pemakaian

Pintu utama routing ada di `skills/atelier/SKILL.md`:
1. Visual vs teks — teks → `no-ai-slop`;
2. Greenfield page vs refine incumbent UI — baru → `design-taste-frontend`, existing → `impeccable`;
3. `ui-ux-pro-max` selalu sebagai lookup data di dalam pipeline manapun;
4. `frontend-design` sebagai lensa prinsip murah kapan saja.

Guard anti-overlap: 2 modul kreatif tidak boleh jadi owner artefak yang sama dalam satu sesi; yang lain boleh sebagai input read-only.

Kebijakan update: manual-review-only — tidak ada auto-update upstream; saat upgrade, diff folder modul vs commit provenance di atas dan review semua perubahan sebelum dipakai.
