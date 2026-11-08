"""Electra — orchestral sting for the animated visual (~5 s), written from scratch.

Direction: grandiose orchestral opening, dramatic (minor) from 0:03, one continuous phrase.
Video cues: headline at 0.25 s, body copy at 0.95 s.

  0.00  opening impact on D (taiko, timpani, low brass)
  0.50  horn theme climbs over a driving low-string ostinato
        Dm (0-1.5) -> Bb (1.5-2.0) -> Gm (2.0-2.5) -> A (2.5-3.0, dominant, timpani roll)
  3.00  dramatic D-minor hit (low brass, choir, taiko)
  3.0+  everything stays on D minor: tremolo strings, receding ostinato, heartbeat taiko

Usage: python3 score.py out.mid   (rendered + layered by render_music.py)
"""
import sys
import mido

TPB = 480
DUR = 5.04
OUT = sys.argv[1]

# section -> GM program; MIDI channel = position in this dict (index 9 = drums)
CH = {
    "vln": 48, "low": 48, "horns": 60, "trb": 57, "tuba": 58,
    "choir": 52, "timp": 47, "taiko": 116, "trem": 44, "drums": None, "oohs": 53,
}
CHAN = {name: i for i, name in enumerate(CH)}
ev = []


def note(ch, n, t, d, v):
    c = CHAN[ch]
    ev.append((t, mido.Message("note_on", channel=c, note=n, velocity=max(1, min(127, int(v))))))
    ev.append((t + d, mido.Message("note_off", channel=c, note=n, velocity=0)))


def chord(ch, ns, t, d, v):
    for n in ns:
        note(ch, n, t, d, v)


def cc(ch, num, val, t):
    ev.append((t, mido.Message("control_change", channel=CHAN[ch], control=num, value=int(val))))


# harmony: (start, end, bass root, triad octave 3, triad octave 4)
H = [
    (0.0, 1.5, 38, [50, 53, 57], [62, 65, 69]),  # Dm
    (1.5, 2.0, 34, [50, 53, 58], [62, 65, 70]),  # Bb
    (2.0, 2.5, 43, [50, 55, 58], [62, 67, 70]),  # Gm
    (2.5, 3.0, 45, [49, 52, 57], [61, 64, 69]),  # A (dominant)
    (3.0, DUR, 38, [50, 53, 57], [62, 65, 69]),  # Dm to the end
]


def harm(t):
    return next(h for h in H if h[0] <= t < h[1])


for ch in CH:
    if ch != "drums":
        cc(ch, 91, 100, 0)  # reverb send
        cc(ch, 7, 112, 0)

# ---------------- 0.00 opening impact ----------------
# low brass kept at D2 and above: on D1 their strong 5th harmonic (F#) colours the chord major
chord("trb", [38, 45, 50, 53], 0.0, 0.9, 118)
note("tuba", 38, 0.0, 0.9, 120)
chord("low", [26, 38], 0.0, 0.6, 120)
note("timp", 38, 0.0, 1.0, 127)
note("taiko", 38, 0.0, 1.0, 127)
note("taiko", 31, 0.0, 1.0, 120)
note("drums", 35, 0.0, 0.5, 127)

# ---------------- low-string ostinato (eighths, accented) ----------------
t, i = 0.5, 0
while t < 4.5:
    s, e, root, mid, hi = harm(t)
    base = root if root >= 38 else root + 12
    step = [0, 0, 12, 0, mid[1] - base, 0, 12, 0][i % 8]
    acc = 1.0 if i % 4 == 0 else 0.82
    v = (92 + 30 * (t - 0.5) / 2.5) * acc if t < 3.0 else (100 - 45 * (t - 3.0) / 1.5) * acc
    note("low", base + step, t, 0.2, v)
    t += 0.25
    i += 1

# violins: 16th-note ostinato in the last two bars before the hit
t = 2.0
while t < 3.0 - 1e-6:
    s, e, root, mid, hi = harm(t)
    k = int(round((t - 2.0) / 0.125))
    note("vln", [hi[0], hi[1], hi[2], hi[1]][k % 4], t, 0.11, 88 + 35 * (t - 2.0))
    t += 0.125

# ---------------- horn theme (legato, climbing to the dominant) ----------------
theme = [(0.5, 0.5, 62), (1.0, 0.25, 65), (1.25, 0.25, 64), (1.5, 0.5, 62),
         (2.0, 0.5, 67), (2.5, 0.25, 69), (2.75, 0.25, 70)]  # D F E D | G | A Bb -> (D hit)
for t, d, n in theme:
    v = 100 + 22 * t / 3
    note("horns", n, t, d * 0.98, v)
    note("horns", n - 12, t, d * 0.98, v - 10)
# trombones / tuba carry the harmony underneath
for s, e, root, mid, hi in H[:4]:
    s0 = max(s, 0.5)
    chord("trb", [root if root >= 38 else root + 12, mid[0]], s0, e - s0, 84 + 14 * s)
    note("tuba", root, s0, e - s0, 86 + 12 * s)
# choir oohs underneath the build
for s, e, root, mid, hi in H[:4]:
    s0 = max(s, 1.0)
    chord("oohs", mid, s0, e - s0, 72 + 18 * s)
for k in range(31):  # expression crescendo into the hit
    tt = k * 0.1
    for ch in ("trb", "tuba", "oohs", "low", "horns"):
        cc(ch, 11, 96 + 31 * (tt / 3.0) ** 1.3, tt)

# ---------------- 2.5 - 3.0 build: timpani roll on A, cymbal swell ----------------
t = 2.5
while t < 2.98:
    note("timp", 45, t, 0.05, 70 + 57 * (t - 2.5) / 0.48)
    note("drums", 51, t, 0.05, 25 + 55 * (t - 2.5) / 0.48)
    t += 0.04

# ---------------- 3.00 dramatic hit on D minor ----------------
for ch in ("trb", "tuba", "oohs", "low", "horns", "choir", "trem"):
    cc(ch, 11, 127, 3.0)
chord("trb", [38, 45, 50, 53], 3.0, 0.75, 127)
note("tuba", 38, 3.0, 0.85, 127)
chord("horns", [57, 62, 65], 3.0, 0.9, 120)
chord("choir", [57, 62, 65, 69], 3.0, DUR - 3.0, 112)
chord("trem", [38, 50, 53, 57], 3.0, DUR - 3.0, 100)
note("timp", 38, 3.0, 1.0, 127)
note("timp", 45, 3.0, 1.0, 118)
note("taiko", 38, 3.0, 1.0, 127)
note("taiko", 31, 3.0, 1.0, 127)
note("drums", 35, 3.0, 0.8, 127)
note("drums", 49, 3.0, 1.5, 80)

# tail: horns sigh D -> A (inside D minor), taiko heartbeat
note("horns", 62, 3.9, 0.5, 100)
note("horns", 57, 4.4, DUR - 4.4, 92)
note("horns", 50, 3.9, DUR - 3.9, 85)
for t, v in [(3.75, 100), (3.95, 78), (4.5, 88), (4.7, 66)]:
    note("taiko", 38, t, 0.4, v)

mf = mido.MidiFile(ticks_per_beat=TPB)
tr = mido.MidiTrack()
mf.tracks.append(tr)
tr.append(mido.MetaMessage("set_tempo", tempo=1_000_000))  # 1 beat = 1 s for easy timing
for name, prog in CH.items():
    if prog is not None:
        tr.append(mido.Message("program_change", channel=CHAN[name], program=prog))
ev.sort(key=lambda e: (e[0], e[1].type == "note_on"))
last = 0
for t, m in ev:
    tick = int(round(t * TPB))
    tr.append(m.copy(time=tick - last))
    last = tick
mf.save(OUT)
print("wrote", OUT)
