# REVIEW (delivery note)

**Render**: `renders/electra-30s.mp4`, 30.0 s, 1080x1920, 30 fps, H.264 + AAC, 6.1 MB.
`hyperframes check`: ok (0 errors). Audio measured on the file: -16.9 LUFS integrated, true peak -1.3 dBTP, no clipping;
hits measured at 1.11 / 4.30 / 10.19 / 13.45 / 18.01 / 19.01 / 20.73 / 23.01 / 25.64 s, synced with the picture. **Measured, not heard.**

## Creative calls
- Vertical format (the source is social stories), "isometric world" storyline (see STORYLINES.md for the 2 not built).
- Logo and wordmark **vectorised from the supplied screenshots** (the brand site is blocked from this environment): check against the official SVG files.
- Font: Outfit (bundled) instead of the brand's typeface (unknown, files unavailable).
- Teal ground #0E8585 instead of #0F8A8A: the brand mint on the brand teal falls just under the AA contrast ratio (2.99:1).
- Network names (Atlante, Fastned, Ionity) set as plain text, not logos (no official files). Their tile colours are illustrative.
- On-screen figures all come from the visuals: 0,49€/kWh, 3 min · 300 kW, 99%, 4/5, 800 000+, 4 h 10, 540 km, 40 €, 20/15 min, 4,8 and 1 505 reviews.
  Illustrative: the 18% -> 56% count-up, the pillar heights, 4/4 -> 3/4, the kW counter at the busy charger.

## Weakest shot / with more time
- No music bed: no music source (HeyGen catalogue not connected). Add a ~120 bpm track and realign the cuts on its beats.
- The car in the "trajet" scene is small; a punch-in on the charging stops would make them more legible.

## Warnings kept on purpose
- `line_unread` on the labels drawn in the SVG worlds: false positives (the SVG is redrawn every frame, so the checker sees "new" texts every 0.13 s).
