# frame.md — Relax × Finaxy case

Brand truth for every composition. Two layers, never mixed up:

- **The film is Relax's.** Canvas, typography, the thread, captions and every word Relax says use the
  Relax identity, captured from relax-agency.com (CSS custom properties + rendered homepage, 2026-10-08).
- **Finaxy's identity is the work being shown.** It appears as artefacts placed on the Relax canvas — the
  logo, the site, the supports, the platform's key lines — in Finaxy's own colors and serif.

## Concept

**Le fil.** One continuous ribbon — the lavender-to-pink ribbon of Relax's homepage, flattened into a
line — runs through the whole film without a cut. It enters scattered complexity, touches each element,
and every touch pulls the next one into place. Its head is the pink dot of the Relax logo (`relax•`); at
the end the thread relaxes, exhales, and comes to rest as that dot. The feeling is relief: motion slows
and settles as coherence grows.

## Relax palette (the film)

| Role              | Hex       | Source                                                     |
| ----------------- | --------- | ---------------------------------------------------------- |
| Canvas            | `#FFFFFF` | `--color-white`; every scene                               |
| Ink               | `#212C34` | `--color-black`; titles and text                           |
| Ink secondary     | `#6B7278` | `--color-text-review-type`; labels, secondary lines        |
| Lavender wash     | `#D4CCEE` | `--color-purple-tag`; radial washes, ribbon light side     |
| Purple            | `#6955AA` | `--color-purple`; the thread's core stroke                 |
| Pink dot          | `#FF0055` | relax logo dot (`fill="#FF0055"`); the thread's head, focal hits only |
| Cyan wash         | `#56A0AA` | `--color-cyan`; washes at ≤30%, discipline color           |
| Yellow wash       | `#ABA256` | `--color-yellow`; washes at ≤30%, discipline color         |
| Red (muted)       | `#AA5655` | `--color-red`; discipline color                            |
| Chaos grey        | `#A7AEB4` | Ink tinted to grey; the "avant" nodes and labels           |

Backgrounds are the site's soft multi-radial washes (cyan left, yellow right, purple center at ~30%) on
white — never a full-frame linear gradient.

## Finaxy palette (the work, artefacts only)

| Role        | Hex       | Source                                  |
| ----------- | --------- | --------------------------------------- |
| Navy        | `#191853` | finaxy.com hero and cards (sampled)     |
| Blue        | `#5A80D9` | finaxy.com "Affinitaire" card (sampled) |
| Slate blue  | `#4A5892` | finaxy.com "Clientèle privée" card      |
| Cream       | `#F4F1EB` | finaxy-new.svg logotype + site band     |
| Burgundy    | `#9C0A3F` | finaxy-new.svg accent + site CTA        |
| Old blue    | `#174A8C` | old platform deck — the "avant" logo only |

## Type

| Role              | Family           | Weights        | Video size                      |
| ----------------- | ---------------- | -------------- | ------------------------------- |
| Relax display     | Unbounded        | 400, 500       | 96–150px headlines (site `--font-title`) |
| Relax text        | DM Sans          | 300, 400, 500, 600 | 30–40px lines, 22–26px labels (site `--font-text`) |
| Finaxy artefacts  | Instrument Serif | 400, italic    | platform quotes and Finaxy-voice lines only |

Fonts are local woff2 in `assets/fonts/` (`fonts.css`).

## Motion

- Eases: `power3.out` entrances, `sine.inOut` ambient drift, `expo.inOut` thread travel, `power2.inOut`
  settles. Chaos runs fast and jittery; every later beat runs slower than the last.
- Direction rule: the thread travels left → right; the world drifts leftward at seams.
- First visible motion within 0.2s of every scene.

## Bans

- No catalogue cards (one deliverable per card, same size, in sequence).
- No English on screen except « naming » and « Team player ».
- No fake product UI: real captures (finaxy.com, supports, AI agent) or a labelled placeholder.
- Finaxy colors never become the film's canvas; Relax pink is never used for text.
- No glow on text, no gradient text, no left-edge accent stripes.
- Motion failures to avoid: the slideshow and the screensaver.
