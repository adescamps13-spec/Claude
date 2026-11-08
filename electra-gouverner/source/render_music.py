"""Render score.py with the MuseScore General soundfont, add trailer sound-design layers
(sub booms, low 'braam', reverse-noise riser) and master to a ~5 s stereo WAV.

Usage: python3 render_music.py <workdir> <out.wav>
Needs: fluidsynth, ffmpeg, numpy, mido, musescore-general-soundfont-lossless
"""
import os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SF = "/usr/share/sounds/sf2/MuseScore_General_Full.sf2"
SR = 48000
DUR = 5.04
work, out = sys.argv[1], sys.argv[2]
os.makedirs(work, exist_ok=True)
mid, orch = f"{work}/score.mid", f"{work}/orch.wav"

subprocess.run([sys.executable, f"{HERE}/score.py", mid], check=True)
subprocess.run(["fluidsynth", "-ni", "-g", "0.5", "-r", str(SR),
                "-o", "synth.reverb.room-size=0.88", "-o", "synth.reverb.level=0.6",
                "-o", "synth.reverb.damp=0.3", "-o", "synth.reverb.width=1",
                "-o", "synth.chorus.active=0", "-F", orch, SF, mid],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with wave.open(orch) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float64) / 32768
n = int(SR * DUR)
x = np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n]
t = np.arange(n) / SR
rng = np.random.default_rng(7)


def fft_filter(sig, lo=None, hi=None):
    S = np.fft.rfft(sig)
    f = np.fft.rfftfreq(len(sig), 1 / SR)
    m = np.ones_like(f)
    if lo: m *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    if hi: m *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(S * m, len(sig))


def sub_boom(at, f0=72, f1=32, decay=0.9):
    tt = np.clip(t - at, 0, None)
    f = f1 + (f0 - f1) * np.exp(-tt / 0.12)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = (t >= at) * np.exp(-tt / decay) * np.minimum(1, tt / 0.004)
    return np.sin(ph) * env


def braam(at, decay=1.1):
    tt = np.clip(t - at, 0, None)
    # additive brass-like tone: only partials that stay inside D minor
    # (a saw on D would put F# — its 5th harmonic — in the chord and make it sound major)
    sig = np.zeros(n)
    voices = ((36.71, 1.0, (1, 2, 3, 4, 6, 8, 12)),  # D1: D, D, A, D, A, D, A
              (87.31, 0.45, (1, 2, 4)),             # F2: minor third, octaves only
              (110.0, 0.35, (1, 2, 4)))             # A2
    for hz, a, partials in voices:
        for det in (-0.5, 0.5):
            for k in partials:
                sig += a / k ** 0.8 * np.sin(2 * np.pi * (hz + det) * k * t + k)
    sig = fft_filter(sig, hi=600)
    env = (t >= at) * np.exp(-tt / decay) * np.minimum(1, tt / 0.03)
    return sig * env


def riser(start, end):
    noise = fft_filter(rng.standard_normal(n), lo=2500, hi=11000)
    u = np.clip((t - start) / (end - start), 0, 1)
    env = (u ** 3) * (t < end) * (t >= start)
    return noise * env


sub = sub_boom(0.0, decay=0.7) * 0.32 + sub_boom(3.0, decay=1.0) * 0.5
br = braam(3.0) * 0.05 + braam(0.0, decay=0.5) * 0.025
rs = riser(2.2, 3.0) * 0.06
layers = sub + br
mix = x * 1.0
mix[:, 0] += layers + rs * 0.9
mix[:, 1] += layers + np.roll(rs, 90)  # slight stereo width on the riser

pre = f"{work}/premix.wav"
with wave.open(pre, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix / max(1e-9, np.abs(mix).max()) * 0.8, -1, 1) * 32767).astype(np.int16).tobytes())

# master: gentle EQ / glue compression, fade, peak at -1 dBFS (dynamics kept)
chain = ("highpass=f=25,equalizer=f=55:t=q:w=1:g=2,equalizer=f=300:t=q:w=1.2:g=-2,"
         "equalizer=f=3200:t=q:w=1.5:g=2.5,acompressor=threshold=-12dB:ratio=2:attack=25:release=250,"
         "afade=t=out:st=4.5:d=0.54")
tmp = f"{work}/pre2.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", chain, tmp], check=True)
r = subprocess.run(["ffmpeg", "-i", tmp, "-af", "volumedetect", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
peak = float(r.split("max_volume:")[1].split("dB")[0])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                f"volume={-1.0 - peak}dB,alimiter=limit=0.89:attack=2:release=60", out], check=True)
print("wrote", out)
