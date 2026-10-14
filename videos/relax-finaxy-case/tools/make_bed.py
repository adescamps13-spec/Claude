"""Synthesize the music bed and the transition whooshes for the v2 cut (numpy + ffmpeg, no network).

bed.wav    — 100 BPM pulse (soft kick, shaker, plucked arpeggio, pad, sub) in B minor; it builds
             through the chain of decisions, thins out under the promise, is gone before the breath,
             and a single D major chord opens on the exhale under relax•.
whoosh.wav — air swells on the big moves (zoom-throughs, film glides, cuts).
Reads tools/timing.json (python3 tools/plan.py first).
    python3 tools/make_bed.py
"""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "tools/timing.json").read_text())
SR = 48000
TOTAL = T["total"]
CUE = T["cue"]
N = int(TOTAL * SR)
rng = np.random.default_rng(7)
t = np.arange(N) / SR

BPM = 100
BEAT = 60 / BPM
BAR = 4 * BEAT
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
# Bm – G – D – A, two bars each
PROG = [[47, 54, 59, 62, 66], [43, 50, 55, 59, 62], [50, 57, 62, 66, 69], [45, 52, 57, 61, 64]]


def env_curve(points):
    """piecewise-linear gain over time from [(sec, gain), ...]"""
    xs, ys = zip(*points)
    return np.interp(t, xs, ys)


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    # one-pole, vectorised in blocks via cumulative filter (scipy-free)
    from itertools import accumulate
    y[:] = list(accumulate(x * (1 - a), lambda p, v: p * a + v))
    return y


def place(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


breath, exhale = CUE["breath"], CUE["exhale"]
drums_out = CUE["5.12"] - 0.4          # "C'est ça, notre promesse" — the pulse lets go
pad_out = breath - 0.2                 # bed gone as the inhale starts
L = np.zeros(N)
R = np.zeros(N)

# --- pad (chord tones, slow swell per chord)
pad = np.zeros(N)
nbars = int(TOTAL / BAR) + 1
for b in range(0, nbars, 2):
    ch = PROG[(b // 2) % 4]
    st, ln = b * BAR, 2 * BAR + 0.6
    n = int(ln * SR)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / 1.2) * np.minimum(1, (ln - tt) / 1.0)
    s = sum(np.sin(2 * np.pi * hz(m + 12) * tt + k) * (0.5 if k == 0 else 0.3) for k, m in enumerate(ch[1:]))
    s += 0.25 * np.sin(2 * np.pi * hz(ch[0] + 12) * tt * 1.003)
    place(pad, st, s * e)
pad *= 0.10

# --- sub bass on each bar root
sub = np.zeros(N)
for b in range(nbars):
    root = PROG[(b // 2) % 4][0] - 12
    n = int(BAR * SR)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / 0.02) * np.exp(-tt * 0.9)
    place(sub, b * BAR, np.sin(2 * np.pi * hz(root) * tt) * e)
sub *= 0.22

# --- plucked arpeggio, 8th notes
arp = np.zeros(N)
arpR = np.zeros(N)
step = BEAT / 2
pattern = [0, 2, 3, 4, 3, 2, 1, 3]
for k in range(int(TOTAL / step)):
    st = k * step
    ch = PROG[int(st / (2 * BAR)) % 4]
    m = ch[1 + pattern[k % 8] % 4] + 12
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / 0.004) * np.exp(-tt * 9)
    s = (np.sin(2 * np.pi * hz(m) * tt) + 0.35 * np.sin(4 * np.pi * hz(m) * tt) * np.exp(-tt * 14)) * e
    place(arp if k % 2 == 0 else arpR, st, s)
arp *= 0.085
arpR *= 0.085

# --- soft kick on 1 and 3, shaker on the off-beats (16ths in the deploy act)
kick = np.zeros(N)
shk = np.zeros(N)
nk = int(0.35 * SR)
tk = np.arange(nk) / SR
freq = 45 + 75 * np.exp(-tk * 30)
kick_s = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tk * 11)
ns = int(0.08 * SR)
noise = rng.standard_normal(ns)
noise = noise - lowpass(noise, 5000)  # crude high-pass
shk_s = noise * np.exp(-np.arange(ns) / SR * 60)
for k in range(int(TOTAL / BEAT)):
    st = k * BEAT
    if k % 2 == 0:
        place(kick, st, kick_s)
    place(shk, st + BEAT / 2, shk_s)
    if CUE["4.0"] - 0.2 < st < CUE["5.0"]:
        place(shk, st + BEAT / 4, shk_s, 0.5)
        place(shk, st + 3 * BEAT / 4, shk_s, 0.5)
kick *= 0.30
shk *= 0.05

# --- arrangement (gain curves)
a1, b0, c0, d0, e0 = CUE["1.1"] - 0.2, CUE["2.0"] - 0.2, CUE["3.0"] - 0.2, CUE["4.0"] - 0.2, CUE["5.0"] - 0.2
g_drum = env_curve([(0, 0), (a1 - 0.01, 0), (a1, 0.8), (CUE["1.4"] - 0.2, 0.8), (CUE["1.4"], 0.0), (b0 - 0.01, 0), (b0, 0.85),
                    (d0, 0.9), (d0 + 0.01, 1.0), (e0, 1.0), (e0 + 0.01, 0.85), (drums_out, 0.85), (drums_out + 1.2, 0), (TOTAL, 0)])
g_arp = env_curve([(0, 0.6), (a1, 0.9), (CUE["1.4"], 0.6), (b0, 0.9), (d0, 1.0), (drums_out, 0.9), (pad_out, 0), (TOTAL, 0)])
g_pad = env_curve([(0, 0), (1.5, 1), (pad_out - 2.0, 1), (pad_out, 0), (TOTAL, 0)])
g_sub = env_curve([(0, 0), (a1, 0), (a1 + 0.01, 1), (drums_out, 1), (drums_out + 1.5, 0), (TOTAL, 0)])
mono = pad * g_pad + sub * g_sub + kick * g_drum + shk * g_drum
L = mono + arp * g_arp + 0.4 * arpR * g_arp
R = mono + arpR * g_arp + 0.4 * arp * g_arp

# --- the resolving chord on the exhale (D major, very soft, long tail)
st = exhale + 0.1
n = int((TOTAL - st) * SR)
tt = np.arange(n) / SR
e = np.minimum(1, tt / 1.6) * np.exp(-tt * 0.32)
chord = sum(np.sin(2 * np.pi * hz(m) * tt) * g for m, g in [(50, 0.5), (57, 0.4), (62, 0.32), (66, 0.22), (69, 0.12)]) * e * 0.12
place(L, st, chord)
place(R, st, chord * 0.97)

# --- whooshes: band-limited noise swells, peak at the given time
W = np.zeros(N)
def whoosh(at, ln=0.55, gain=1.0, bright=2400):
    n = int(ln * SR)
    x = rng.standard_normal(n)
    x = lowpass(x, bright) - lowpass(x, 300)
    tt = np.arange(n) / SR
    e = np.where(tt < ln * 0.65, (tt / (ln * 0.65)) ** 2, np.exp(-(tt - ln * 0.65) * 14))
    place(W, at - ln * 0.65, x * e * gain)

c = CUE
starts, _t = [], 0.0
for _sc in T["scenes"]:
    starts.append(_t)
    _t += _sc["dur"]
SW = [sc_start + (0.05 if k else 0) for k, sc_start in enumerate(starts)][1:-2]  # every cut but the promise and the breath
SW += [c["2.0"] + 0.85, c["2.0"] + 1.55, c["2.0"] + 2.25, c["4.3"] - 0.02, c["4.4"] - 0.02, c["4.5"] - 0.02, c["3.8"] + 0.2]
for i, at in enumerate(SW):
    whoosh(at, 0.5 + 0.1 * (i % 3), 1.0, 1800 + 400 * (i % 4))


def write(path, chans, target_peak):
    x = np.stack(chans, axis=1)
    x = x / (np.abs(x).max() + 1e-9) * target_peak
    pcm = (x * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def loudness_to(path, lufs):
    """static gain to an integrated loudness target (no dynamic normalisation, fades stay intact)"""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    cur = float(out.rsplit("I:", 1)[1].split("LUFS")[0])
    tmp = path.with_suffix(".tmp.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-af", f"volume={lufs - cur:.2f}dB,alimiter=limit=0.89", str(tmp)], check=True)
    tmp.replace(path)


write(ROOT / "assets/audio/bed.wav", [L, R], 0.8)
loudness_to(ROOT / "assets/audio/bed.wav", -29)
write(ROOT / "assets/audio/whoosh.wav", [W, W * 0.92], 0.5)
loudness_to(ROOT / "assets/audio/whoosh.wav", -36)
print(f"bed.wav + whoosh.wav {TOTAL:.1f}s — drums out {drums_out:.1f}s, pad out {pad_out:.1f}s, chord {exhale + 0.1:.1f}s, {len(SW)} whooshes")
