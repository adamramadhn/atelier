# design-skills

Kurasi private gabungan skill UI/UX & writing dari 5 sumber upstream. Setiap skill disalin byte-per-byte dari upstream (body tidak diedit), dipilih dengan analisa overlap sehingga tiap skill meng-cover fungsi yang berbeda.

## Komposisi & partisi (anti-overlap)

| Skill | Kapan dipakai | Tidak dipakai untuk |
|---|---|---|
| `skills/design-taste-frontend` (taste-skill v2) | Greenfield art direction & build landing page / marketing / portfolio / one-pager: deal arah visual dari library 247 situs, house style anti-slop, inspector browser + screenshot loop | Refine UI produk existing (→ impeccable); lookup data desain (→ ui-ux-pro-max); UI non-landing (→ frontend-design) |
| `skills/impeccable` | Refine/iterate UI **existing** produk & app: 24 commands (critique, audit, polish, harden, bolder/quieter, live, generate, dll) + engine detector 61 aturan. Butuh engine binary yang auto-download on first run (`scripts/impeccable`) | Art direction dari nol untuk landing baru (→ design-taste-frontend) |
| `skills/ui-ux-pro-max` | Knowledge base lookup: styles (79), palettes (192), font pairings (74), UX guidelines (119), stacks (22) via script pencarian; verifikasi konvensi platform/stack | Proses/taste: gunakan menjelaskan pilihan desain, bukan menentukannya |
| `skills/frontend-design` (anthropics) | Prinsip estetika universal (prosa, tanpa runtime): membuat UI baru tidak templated, tipografi, motion, copywriting UI | Prosedur bertahap & validasi browser (→ design-taste-frontend / impeccable) |
| `skills/no-ai-slop` | Editor tulisan: hapus pola AI-slop dari copy/teks apa pun tanpa merusak voice; atau deteksi slop | UI/visual sama sekali — domain murni teks |

Aturan pakai (urutan praktis ketika membangun halaman baru dari 0):
1. `ui-ux-pro-max` untuk riset konvensi & data desain;
2. `design-taste-frontend` untuk arah & build halaman marketing;
3. `impeccable` untuk polish/audit iterasi di UI produk;
4. `frontend-design` sebagai lensa prinsip kapan saja;
5. `no-ai-slop` untuk semua copy/teks terakhir.

## Sumber & provenance

| Skill di repo ini | Upstream | Commit diambil | Lisensi |
|---|---|---|---|
| `design-taste-frontend` | github.com/Leonxlnx/taste-skill (`skills/taste-skill`) | `b9ca2fd` (2026-10-19) | MIT |
| `impeccable` | github.com/pbakaus/impeccable (`.claude/skills/impeccable`) | `0665bd8` (2026-10-19) | Apache-2.0 |
| `ui-ux-pro-max` | github.com/nextlevelbuilder/ui-ux-pro-max-skill (`.claude/skills/ui-ux-pro-max`) | `56ea9cf` (2026-10-15) | MIT |
| `frontend-design` | github.com/anthropics/skills (`skills/frontend-design`) | `dbd4588` (2026-10-09) | Lisensi Anthropic (attribution; lihat LICENSE.txt di folder skill) |
| `no-ai-slop` | github.com/petergyang/no-ai-slop (`skills/no-ai-slop`) | `000650b` (2026-09-01) | MIT |

Yang sengaja TIDAK diambil:
- `taste-skill`: v1, v2-experimental, gpt-taste, stitch (deprecated/varian), style variants opt-in (soft/minimalist/brutalist), dan 4 skill pointer "moved" (brandkit, imagegen-web/mobile, image-to-code → repo `Leonxlnx/imagegen-skills`).
- `impeccable` & `ui-ux-pro-max-skill`: full repo tidak diambil, hanya folder skill (engine impeccable tetap di dalam folder skill-nya).
- sisanya `anthropics/skills` (canvas-design, web-artifacts-builder, document-skills, dll) di luar scope.

## Pemakaian

Format agent-standard (`skills/<nama>/SKILL.md` + folder pendukung). Salin folder skill yang dibutuhkan ke direktori skills harness masing-masing (`.claude/skills/`, `.agents/skills/`, dll.)

**Routing dipakai jangan diganti-ganti**: [AGENTS.md](AGENTS.md) adalah sumber kebenaran soal skill mana untuk permintaan mana — aturan routing, guard anti-overlap, dan catatan environment (Node 22+/Chromium untuk taste scripts, engine binary impeccable, sebagainya) ada di sana. [CLAUDE.md](CLAUDE.md) menambahkan konvensi khusus Claude Code dan menunjuk ke AGENTS.md. `skills/frontend-design/LICENSE.txt` harus ikut kalau folder skill-nya disalin.

Kebijakan update: manual-review-only — tidak ada auto-update dari upstream; tiap skill punya commit provenance di atas. Saat upgrade, diff folder skill lama vs upstream dan review perubahan sebelum dipakai.
