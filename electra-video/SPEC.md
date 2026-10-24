# SPEC: Electra, 30 s motion design (vertical)

GOAL:    the viewer remembers "Electra = cheap, fast charging, the right station on the first try" and downloads the app.
OUTPUT:  HyperFrames, 1080 x 1920 (9:16, social), 30 fps
TIME:    30 s x 30 fps = 900 frames. No music bed (no source available), sound effects only.
LOOK:    brand palette taken from the supplied visuals: teal #0E8585 (brand #0F8A8A darkened 3% so the mint passes AA 3:1),
         mint #45F5B9 (one highlighted word per shot), pale mint #E8FFFC, navy #0F2A3A, white.
         Display face Outfit 700, 116-132 px, tracking -3%; body Outfit 500, 42-46 px (closest bundled face to the brand's geometric grotesk).
         Medium: flat-shaded isometric 3D (top +18% light, right face -22%), true iso projection (30°), no gradients, no glow.
         Worlds alternate between the teal ground and the pale ground, linked by colour floods.
OBJECTS: Electra charger (teal body, dark canopy, screen, wordmark on the side), car, cable with energy flowing, Electra+ coins,
         network tiles, isometric city, recommendation pillars, Electra card, charge-point grid, route with stops, station with 4 chargers.
MOTION:  arrivals expo.out / power4.out; camera power2/power3.inOut; exits and dives power3.in.
         Springs: damping 0.45-0.62 on position/height, never on opacity. Titles: blur 10 -> 0 in 0.18 s, no translate.
SHOTS:
  0.0-3.6   HOOK     the car parks, the cable plugs in, the sign counts up to "56% · 78kW"; dive into the charger screen.
  3.6-7.4   ELECTRA+ coins drop onto the 4 networks (Electra, Atlante, Fastned, Ionity); teal flood.
  7.4-12.2  RECO     the tiles become a city; the pillars re-rank on each criterion; Electra wins; "Station recommandée" card; card flips.
  12.2-16.2 PARTOUT  the Electra card flips, lies down in iso, a wave of charge points; counter "800 000+".
  16.2-21.6 TRAJET   the route draws, the car drives with 2 charging stops; "4 h 10 · 540 km · 40 €" card; tap "C'est parti"; iris.
  21.6-25.4 DIRECT   a car reverses into a bay, the light turns orange, availability goes from 4/4 to 3/4 live.
  25.4-30.0 END      4,8 Trustpilot, 5 stars; the mark rises in extrusion, ELECTRA wipes in, CTA "Téléchargez l'app Electra".
BANNED:  dark void, glow/particles, purple/blue gradients, everything fading/sliding in, docked logo, three cards in a row,
         a title that moves after it lands, invented product UI (the cards reproduce the app's labels from the screenshots).
QA:      0 s (thumbnail: title + charger), 3.5 s (dive), 11 s (card, no collisions), 14.5 s (grid), 20.7 s (tap), 29 s (lockup).
