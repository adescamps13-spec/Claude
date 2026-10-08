# frame.md — Relax × Finaxy case

Brand truth for every composition. Colors and fonts are strict; sizes are video sizes.

## Concept

**Le fil rouge.** One continuous burgundy line — Relax's thread — runs through the whole film. It enters
scattered complexity, touches each element, and every touch pulls the next element into place. Nothing
cuts; the thread carries each seam. The feeling is relief: motion slows and settles as coherence grows.

## Palette (by role)

| Role            | Hex       | Source / use                                                                 |
| --------------- | --------- | ---------------------------------------------------------------------------- |
| Background ink  | `#14110F` | Warm near-black, tinted toward the burgundy; every scene except the finale    |
| Foreground      | `#F4F1EB` | Finaxy new logotype cream (finaxy-new.svg); all primary text                  |
| Accent / fil    | `#9C0A3F` | Finaxy new logotype burgundy; the thread, focal hits only                     |
| Accent lit      | `#C2185B` | Burgundy lifted for glows/line highlights on ink (never text on ink)          |
| Before / chaos  | `#5E7891` | Desaturated old Finaxy blue (old deck #174A8C / charte #3B6EA5); "avant" only |
| Muted text      | `#B9B2A6` | Cream at reduced value for labels, secondary lines (AA on ink)                |
| Finale canvas   | `#F4F1EB` | Cream field after the exhale; ink text on it                                  |

One accent hue. No gradients across full frame (radial glows only). No neon, no cyan.

## Type

| Role    | Family           | Weights      | Video size                     |
| ------- | ---------------- | ------------ | ------------------------------ |
| Display | Instrument Serif | 400, italic  | 120–190px headlines, 72px quotes |
| Text    | Manrope          | 300, 600, 800 | 30–40px lines, 22–26px labels |
| Labels  | Manrope 600      | uppercase, letter-spacing .18em | 20–24px          |

Fonts are local woff2 in `assets/fonts/` (`fonts.css`). Serif + sans only — no second sans.

## Motion

- Eases: `power3.out` for entrances, `sine.inOut` for ambient drift, `expo.inOut` for the thread's travel,
  `power2.inOut` for settles. Chaos beats run fast and jittery; every later beat runs slower than the last.
- Direction rule: the thread travels left → right; the camera follows, so the world drifts leftward at seams.
- First visible motion within 0.2s of every scene.

## Bans

- No catalogue cards (one deliverable per card, same size, in sequence).
- No English words on screen except « naming » and « Team player ».
- No fake product UI: real captures of the sites, supports and AI agent, or a labelled placeholder.
- No glow on text, no gradient text, no left-edge accent stripes.
- Motion failures to avoid: the slideshow (every beat a fresh card) and the screensaver (motion that says nothing).
