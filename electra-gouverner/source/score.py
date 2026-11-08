"""Short epic orchestral sting (~5 s) for the animated visual.
Dm -> Bb -> C -> dark D-minor hit at 3.0 s held to the end; the string ostinato carries on
and the horns echo the opening D-A call, so the ending continues the intro instead of starting a new piece.
Writes a MIDI file; render with fluidsynth + an orchestral/GM soundfont."""
import sys
import mido

TPB = 480  # ticks per beat, tempo = 60 BPM -> 1 beat = 1 second
OUT = sys.argv[1]
DUR = 5.1

# section -> GM program; MIDI channel = position in this dict (drums land on channel 9)
CH = {
    "strings": 48, "lowstr": 48, "horns": 60, "trumpets": 56, "trombones": 57,
    "tuba": 58, "choir": 52, "timp": 47, "trem": 44, "drums": None,
}
events = []  # (time_s, msg)


def note(ch, n, t, d, v):
    chan = list(CH).index(ch) if ch != "drums" else 9
    events.append((t, mido.Message("note_on", channel=chan, note=n, velocity=max(1, min(127, int(v))))))
    events.append((t + d, mido.Message("note_off", channel=chan, note=n, velocity=0)))


def chord(ch, notes, t, d, v):
    for n in notes:
        note(ch, n, t, d, v)


def cc(ch, num, val, t):
    chan = list(CH).index(ch)
    events.append((t, mido.Message("control_change", channel=chan, control=num, value=int(val))))


D2, A2, D3, F3, A3, D4 = 38, 45, 50, 53, 57, 62
# progression (start, end, bass, triad mid, triad high)
prog = [
    (0.0, 1.5, 38, [50, 53, 57], [62, 65, 69]),   # Dm
    (1.5, 2.25, 34, [46, 50, 53], [58, 62, 65]),  # Bb
    (2.25, 3.0, 36, [48, 52, 55], [60, 64, 67]),  # C
    (3.0, DUR, 38, [50, 53, 57], [62, 65, 69]),   # Dm hit, held
]

# --- low strings + tuba/trombones: sustained bass, swelling ---
for s, e, b, mid, hi in prog:
    v = 70 if s < 3 else 112
    note("lowstr", b, s, e - s, v)
    note("lowstr", b - 12, s, e - s, v)
    note("tuba", b - 12 if b > 36 else b, s, e - s, v - 5)
    chord("trombones", [b, b + 7], s, e - s, v - 10 if s < 3 else v)

# expression swell on brass/strings before the climax
for i in range(31):
    t = i * 0.1
    for ch in ("lowstr", "tuba", "trombones", "choir", "strings"):
        cc(ch, 11, 70 + 57 * (t / 3.0) ** 1.6, t)
for ch in ("lowstr", "tuba", "trombones", "choir", "strings", "horns", "trumpets", "trem"):
    cc(ch, 11, 127, 3.0)
    cc(ch, 91, 110, 0)   # reverb send
    cc(ch, 7, 110, 0)

# --- string ostinato (eighths at 0.25 s), accelerating feel into the hit ---
ost = [0, 0, 3, 0, 5, 0, 3, 7]  # relative to chord root in minor-ish pattern
step = 0.25
t = 0.0
i = 0
while t < DUR - 0.5:
    s, e, b, mid, hi = next(p for p in prog if p[0] <= t < p[1])
    root = mid[0]
    vel = 70 + 40 * t / 3 if t < 3.0 else 105 - 35 * (t - 3.0) / 1.6  # ostinato keeps going, receding
    note("strings", root + [0, 0, 7, 0, 12, 0, 7, 3][i % 8], t, step * 0.9, vel)
    if 2.25 <= t < 3.0:  # double-time in the last bar
        note("strings", root + 12, t + step / 2, step * 0.45, 95 + 20 * (t - 2.25) / 0.75)
    t += step
    i += 1

# --- tremolo strings + choir pads following the chords ---
for s, e, b, mid, hi in prog:
    chord("trem", mid + hi[:1], s, e - s, 60 if s < 3 else 85)
    chord("choir", hi, max(s, 0.4), e - max(s, 0.4), 55 if s < 3 else 95)

# --- heroic horn motif (enters with the headline at 0.25 s) ---
motif = [(0.25, 0.5, 62), (0.75, 0.75, 69), (1.5, 0.4, 70), (1.9, 0.35, 69),
         (2.25, 0.4, 67), (2.65, 0.35, 64)]
for t, d, n in motif:
    note("horns", n, t, d * 0.97, 92 + 15 * t / 3)
    note("horns", n - 12, t, d * 0.97, 80 + 15 * t / 3)
# trumpet pickup into the hit (part of the 0-3 s intro, unchanged)
for t, n in [(2.75, 69), (2.875, 69), (2.9375, 72)]:  # A A C -> D (no B natural)
    note("trumpets", n, t, 0.06, 105)
# climax: dark D-minor hit, horns mid register, no bright trumpets
chord("horns", [57, 62, 65], 3.0, 0.7, 120)
# horns echo the opening call (D -> A) to close the phrase
for t, d, n in [(3.75, 0.5, 62), (4.25, DUR - 4.25, 69)]:
    note("horns", n, t, d * 0.97, 112)
    note("horns", n - 12, t, d * 0.97, 100)

# --- timpani ---
note("timp", 38, 0.0, 1.2, 120)
note("timp", 45, 0.0, 1.2, 100)
note("timp", 38, 1.5, 0.6, 100)
note("timp", 36, 2.25, 0.4, 100)
t = 2.35
while t < 2.98:  # crescendo roll
    note("timp", 38, t, 0.05, 70 + 55 * (t - 2.35) / 0.63)
    t += 0.045
note("timp", 38, 3.0, 0.7, 127)
note("timp", 45, 3.0, 0.7, 120)
# heartbeat pulses after the hit
for t, v in [(3.75, 95), (4.25, 85)]:
    note("timp", 38, t, 0.3, v)

# --- percussion: bass drum, crash ---
note("drums", 35, 0.0, 0.5, 120)
note("drums", 36, 0.0, 0.5, 110)
note("drums", 35, 3.0, 1.0, 127)
note("drums", 36, 3.0, 1.0, 127)
note("drums", 49, 3.0, 1.5, 85)  # restrained crash, darker impact
t = 2.25
while t < 2.97:  # suspended-cymbal swell via soft rolls
    note("drums", 51, t, 0.05, 30 + 60 * (t - 2.25) / 0.72)
    t += 0.06

mid_file = mido.MidiFile(ticks_per_beat=TPB)
tr = mido.MidiTrack()
mid_file.tracks.append(tr)
tr.append(mido.MetaMessage("set_tempo", tempo=1_000_000))
for name, prog_no in CH.items():
    if prog_no is not None:
        tr.append(mido.Message("program_change", channel=list(CH).index(name), program=prog_no))
events.sort(key=lambda e: (e[0], e[1].type == "note_on"))
last = 0
for t, m in events:
    tick = int(round(t * TPB))
    tr.append(m.copy(time=tick - last))
    last = tick
mid_file.save(OUT)
print("wrote", OUT)
