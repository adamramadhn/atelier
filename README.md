<div align="center">

# ✦ ATELIER

**Satu skill, semua yang dibutuhkan UI.**
Art direction, polish, data desain, prinsip estetika, dan copy editing — satu pintu, tanpa overlap.

![Atelier banner](assets/banner.png)

![Format](https://img.shields.io/badge/format-agent--standard--skills-blue)
![Lisensi modul](https://img.shields.io/badge/lisensi-MIT%20%2F%20Apache--2.0%20%2F%20Anthropic-green)
![Status](https://img.shields.io/badge/status-private--use-orange)

</div>

---

**Atelier** adalah satu skill gabungan (single SKILL.md entry point) yang menyatukan lima skill UI/UX & writing terbaik dari sumber open-source, di bawah satu routing anti-overlap. Bukan 5 skill terpisah — agent hanya mengenali **satu** nama: `atelier`. Body tiap modul tetap byte-per-byte dari upstream (mudah di-diff saat update), tapi tidak pernah dibenarkan jadi skill mandiri.

## Isi (5 modul, 1 routing)

| # | Modul | Untuk apa | Kredit |
|---|-------|-----------|--------|
| 1 | `ui-ux-pro-max` | Lookup konvensi desain: 79 styles, 192 palettes, 74 font pairing, 119 UX guidelines, 22 stacks | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (MIT) |
| 2 | `design-taste-frontend` | Art direction dari nol & build landing/marketing/portfolio: deal arah visual dari studi 247 situs gallery, house style anti-slop, validasi browser asli + screenshot loop | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT) |
| 3 | `impeccable` | Refine/audit/polish UI **existing**: 24 command (critique, audit, polish, harden, animate, live, …) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) |
| 4 | `frontend-design` | Lensa prinsip estetika universal — tipografi, motion restraint, copy UI — prosa murah tanpa runtime | [anthropics/skills · frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Anthropic) |
| 5 | `no-ai-slop` | Editor teks: hapus/deteksi pola AI-slop di copy, README, docs — tanpa merusak voice | [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (MIT) |

## Cara kerjanya

```
              permintaan user (UI / copy)
                        ↓
              ┌── SKILL.md (atelier) ──┐
              │  teks / docs      → no-ai-slop
              │  UI existing      → impeccable
              │  UI baru/landing  → design-taste-frontend
              │  lookup data      → ui-ux-pro-max
              │  prinsip          → frontend-design
              └────────────────────────┘
```

Anti-overlap guard: dua modul kreatif(`design-taste-frontend` & `impeccable`) tidak pernah jadi owner artefak yang sama dalam satu sesi; modul lain bekerja sebagai input read-only. Trigger-nya sengaja pas kata real-user ("perbaiki layout", "UI-nya jelek", "feels AI-made"), bukan cuma kata "design".

## Pakai link referensi style

Kasih URL di prompt — skill mengukurnya, bukan menebak dari ingatan:

> *"Bikin landing page kopi, style-nya mirip termul.dev"*

Yang terjadi di dalam:
1. **Ukur referensi** — `inspect.mjs <url>` buka halaman referensi via browser asli (1440/768/390), simpan screenshot 3 viewport, dan auto baca token: warna nyata, font yang ter-loaded, type sizes, spasi, radius, shadow, gradient → `.taste-skill/reference/`;
2. **Token jadi `REFERENCE.md`** (project root) sebagai *pinned brief*: grammar style (hierarki, tone, rhythm) — bukan pixel-clone konten/aset milik orang;
3. **Routing biasa lanjut**: build dari nol → taste run dengan brief pinned (kalau referensi sudah memfiksasi brand color/type: `draw.mjs --keep palette,type`); polish UI existing → impeccable dengan `DESIGN.md` seeded dari `REFERENCE.md`.

Screenshot tanpa Chrome/Node juga bisa: berikan screenshot referensi di prompt, agent baca computed styles-nya manual. Situs dari library riset 247 situs juga bisa dijadikan arah: `node <skill>/scripts/draw.mjs --site <id>`.


## Instalasi

```bash
git clone git@github.com:adamramadhn/atelier.git
cp -r atelier/skills/atelier ~/.claude/skills/atelier   # atau .agents/skills/, dst
```

Folder `references/` harus ikut — modul dimuat on-demand dari sana. Slash-invocable: `/atelier`; tanpa slash pun model memanggil otomatis saat ada pekerjaan UI. Untuk project konsumen yang mau routing dipaksakan level-project, tambahkan baris ini ke `AGENTS.md`/`CLAUDE.md`:

```
Any UI/front-end task (pages, components, styling, layouts, UI copy): read
.claude/skills/atelier/SKILL.md and follow its routing before editing.
```

## Uji cepat

Setelah install, sesi Claude Code baru: *"bikin landing page buat brand kopi"* — skill harus ter-trigger sendiri dan membaca modul `design-taste-frontend` (deal + build + screenshot loop). Tampilan akhir diverifikasi via browser; `.taste-skill/` adalah working files lokal.

## Environment & dependensi

| Modul | Butuh |
|---|---|
| `design-taste-frontend` | Node 22+, Chrome/Edge/Chromium; `assets.mjs` butuh jaringan (tanpa API key) |
| `impeccable` | Self-contained binary auto-download ke `~/.impeccable/bin/` |
| `ui-ux-pro-max` | Offline penuh (data CSV bundled) |
| `frontend-design`, `no-ai-slop` | Tanpa runtime |

## Provenance & update

Update upstream **manual-review-only**: diff folder modul vs commit provenance, review semua perubahan, baru merge.

| Modul | Commit upstream dipilih | Lisensi |
|---|---|---|
| `design-taste-frontend` | `b9ca2fd` (2026-10-19) | MIT |
| `impeccable` | `0665bd8` (2026-10-19) | Apache-2.0 |
| `ui-ux-pro-max` | `56ea9cf` (2026-10-15) | MIT |
| `frontend-design` | `dbd4588` (2026-10-09) | Anthropic |
| `no-ai-slop` | `000650b` (2026-09-01) | MIT |

Yang sengaja TIDAK diambil:
- varian deprecated/pointer "moved" di `taste-skill` (v1, v2-experimental, gpt-taste, stitch, soft/minimalist/brutalist, brandkit, imagegen, image-to-code);
- full repo `impeccable` & `ui-ux-pro-max-skill` (hanya folder skill-nya);
- sisanya `anthropics/skills` (canvas-design, web-artifacts-builder, document-skills, dll).

---

<div align="center">

**Kurasi pribadi.** Repo privat — tidak untuk disebarkan setelah refactor kecil.

</div>
