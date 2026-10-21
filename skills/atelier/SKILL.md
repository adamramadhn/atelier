---
name: atelier
description: "One entry point for all UI and copy work. Six internally-vendored modules, routed by task: (1) ui-ux-pro-max — searchable design conventions (79 styles, 192 palettes, 74 font pairings, 119 UX guidelines, 22 stacks); (2) design-taste-frontend (taste-skill v2) — greenfield art direction and building landing pages, marketing sites, portfolios, one-pagers and app screens, anti-slop house style with real-browser inspection and screenshot loops; (3) impeccable — refine, critique, audit, polish, harden, or otherwise improve an EXISTING UI, including native (iOS/Android) surfaces. (4) frontend-design — inexpensive principles for distinctive, intentional design on any fresh UI. (5) no-ai-slop — edit or detect AI-slop patterns in any copy or documentation. (6) motion-design — motion-first work: timing, easing, choreography, micro-interactions, transitions, loading states, scroll-driven motion, brand motion identity (CSS, GSAP, Framer Motion, Lottie, springs). Trigger on ANY UI/front-end work — pages, components, dashboards, forms, settings, modals, styling, layout, responsive, dark mode, typography, charts, Tailwind/shadcn/CSS, animation — even when the user never says 'design': building, editing, fixing, or reviewing a visual surface is the trigger. Also for copy editing and the accusation that something looks generic / AI-made."
user-invocable: true
argument-hint: "[lookup|taste|impeccable|motion|principles|slop] <module-args> [target]"
---

# atelier

One skill, six vendored modules loaded on demand. This SKILL.md decides **which** module runs; the module's own SKILL.md under `references/` then governs how. Module bodies are unedited upstream vendor copies — always execute/trust them as-is; never paraphrase them into this file or vice versa.

## Modules

| Module | Trigger | Entry point to read |
|---|---|---|
| `ui-ux-pro-max` | Look up design conventions, styles, type, colors, guidelines, or a platform/stack's UI expectations — before or while doing any other UI task | `references/ui-ux-pro-max/SKILL.md` |
| `design-taste-frontend` | Build or restyle a **new** landing page, marketing/portfolio/product site, one-pager, or app screen; "looks generic, AI-made, not premium" on a public page | `references/design-taste-frontend/SKILL.md` |
| `impeccable` | Improve, critique, audit, polish, harden, or iterate an **existing** UI (product screens, dashboards, settings, components); holistic polish that may touch motion lightly | `references/impeccable/SKILL.md` |
| `motion-design` | **Motion-first** work: new or revised animations, transitions, micro-interactions, choreographed sequences, loading/success/error motion, scroll/progress effects, Lottie/GSAP/Framer/CSS springs, or establishing motion personality — even on greenfield pages | `references/motion-design/SKILL.md` |
| `frontend-design` | Universal aesthetic principles for any form of fresh UI art-direction — read as a lens in parallel with the above, never as a substitute for them | `references/frontend-design/SKILL.md` |
| `no-ai-slop` | Any copy, README, docs, or drafted text editing/detection anywhere in the flow | `references/no-ai-slop/SKILL.md` |

## Routing

Resolve intent before opening a module SKILL.md:

1. **Is the work visual or text?** Copy/docs/draft → `no-ai-slop` (terminates: return edited text or detection verdict). UI → step 2.
2. **Motion-first or general UI?** The primary deliverable is animation choreography, timing/easing, transitions, micro-interactions, motion identity, or Lottie/GSAP/Framer implementation → `motion-design` (owner for that motion scope). Layout/typography/color polish without a motion-led brief → step 3. For motion snippets or stack-specific motion lookup only, use `ui-ux-pro-max` inside the active pipeline instead of opening `motion-design`.
3. **Greenfield art direction or incumbent refinement?** New page/site/screen to conceptualize and build, or a "make this look designed" restyle that discards the current look → `design-taste-frontend`. Improving/hardening an existing implementation while preserving its identity → `impeccable`.
4. **Data lookup needed?** (naive question of what a category's conventions are, plausible palette/typography options, etc.) → run `ui-ux-pro-max` searches as a step inside whichever pipeline, not a separate creative read.
5. **Native iOS/Android surface?** → relevant native flows: `impeccable` has native references; `design-taste-frontend`'s app-screens doc has its own mobile rules; motion-heavy native transitions → `motion-design` with platform APIs as implementation detail.
6. **Every module's run benefits from `frontend-design`** principles — it's cheap prose; skim before final visual decisions.

Anti-overlap guard: never run two before/after-equivalent modules on the same artifact in one session. `design-taste-frontend` full run + `impeccable` shape/build on one page is redundant — pick one owner per artifact; the others may contribute as read-only inputs (e.g. `ui-ux-pro-max` data lookup during taste's run). **`motion-design` vs `impeccable animate`:** if the session is motion-led (step 2), `motion-design` owns the animation work; do not also run `impeccable animate` on the same components. If the session is a broad incumbent polish and motion is incidental, `impeccable` owns the page and may skim `motion-design` or `ui-ux-pro-max` motion data as read-only input.

The user's pinned brief always wins over module defaults — including the brief that asks for one of the "tells" a module catalogs.

### Reference-URL intake (user supplies a style reference)

When the user seeds the task with a URL (or screenshots) whose look they want imitated, capture the reference before dealing any direction:

1. **Extract, don't eyeball.** Measure the reference page with the taste module's inspector: `node references/design-taste-frontend/scripts/inspect.mjs <url> --out .taste-skill/reference` — it saves real screenshots (desktop/tablet/mobile) and prints measured colors, fonts actually loaded, type sizes, radii, shadows, gradients. Working offline or without Chrome: screenshot via any browser tool and read computed styles by hand.
2. **Store as a pinned brief** — write the tokens (palette hex, type stack + weights, spacing/rhythm, radius, shadow, motion character, layout signature, and what the page does NOT do) into `REFERENCE.md` in the project root. A copy is not a target: name the style's grammar and the feel, not pixel values to clone. **This does not license cloning someone else's work: replicate the system (spacing, hierarchy, tone), keep the content original, and don't copy trademarked imagery or custom artwork.**
3. **Route exactly as before.** Greenfield landing work → taste run, with `REFERENCE.md` as the pinned brief; if the reference fixes brand colors/type, pass taste's deal `--keep palette,type` (or a named `--direction`) and skip brand re-dealing. Existing-UI polish → impeccable, with `DESIGN.md` seeded from `REFERENCE.md`. Lookup helpers (`ui-ux-pro-max`) carry the same tokens through either pipeline.

## Environment

- `design-taste-frontend` scripts: Node 22+, Chrome/Edge/Chromium; run from the project root so working files land in `.taste-skill/` there. `assets.mjs` needs network; nothing else does.
- `impeccable` engine: a self-contained binary auto-downloaded to `~/.impeccable/bin/` on first run via the module's own launcher (`scripts/impeccable`). If the launcher fails, say so to the user, read the project's `PRODUCT.md`/`DESIGN.md` directly and continue without inventing missing context.
- `ui-ux-pro-max` search scripts are fully offline against bundled CSV data.
- `frontend-design` carries its own `LICENSE.txt` — keep it when copying the skill folder.
- `motion-design` is prose + reference docs only; no runtime.

## Update policy

Upstream sync is manual-review-only. Provenance (upstream repo + commit picked per module) is in the repo's `README.md`; when upgrading, diff the vendored module folder against the upstream commit and review every change before merging. Never update these folders automatically.

## Update notice (installed copy)

At most once per session, before heavy work begins: run `sh scripts/check-update.sh` from this skill's root (one 4s network call, always exit 0, prints `no-info` silently when offline). If it prints `UPDATE AVAILABLE`, pause and tell the user: "Skill atelier installed `<installed>`, latest `<latest>` — update now?" If they confirm, run `sh <(curl -s https://raw.githubusercontent.com/adamramadhn/atelier/main/install.sh)`, then re-read `SKILL.md` and any module files before continuing. Ignore `update-notified` (repeated within 24h) and skip the check entirely when the user wants a short/fast operation.
