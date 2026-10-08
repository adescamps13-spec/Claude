"""Synthesize the ambient bed to the cut's real length (ffmpeg only, no network).

The pad fades out just before the final breath (scene s12) and a soft resolving chord
returns under the relax logo, on the exhale. Reads tools/timing.json.
    python3 tools/make_bed.py
"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "tools/timing.json").read_text())
start = 0.0
for sc in T["scenes"]:
    if sc["id"] == "s12-relax":
        s12, exhale = start, sc["vo"]["exhale"]
    start += sc["dur"]
total = start
pad_len = s12 + 0.6  # pad fully gone as the inhale begins
chord_at = s12 + exhale + 0.1

tmp = Path(tempfile.mkdtemp())
run = lambda *a: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
run("-f", "lavfi", "-i", f"sine=f=146.83:d={pad_len},volume=0.30", "-f", "lavfi", "-i", f"sine=f=220:d={pad_len}",
    "-f", "lavfi", "-i", f"sine=f=369.99:d={pad_len}", "-f", "lavfi", "-i", f"sine=f=554.37:d={pad_len}",
    "-f", "lavfi", "-i", f"anoisesrc=color=pink:amplitude=0.02:d={pad_len}:seed=9",
    "-filter_complex", "[1]volume=0.22,tremolo=f=0.11:d=0.5[b];[2]volume=0.12,tremolo=f=0.1:d=0.6[c];"
    "[3]volume=0.06,tremolo=f=0.13:d=0.7[d];[4]lowpass=f=900[n];[0][b][c][d][n]amix=inputs=5:normalize=0,"
    f"lowpass=f=2200,aecho=0.8:0.7:220|390:0.35|0.25,afade=t=in:d=3,afade=t=out:st={pad_len - 2.8:.2f}:d=2.6",
    "-ar", "48000", "-ac", "2", str(tmp / "a.wav"))
run("-f", "lavfi", "-i", "sine=f=146.83:d=5", "-f", "lavfi", "-i", "sine=f=220:d=5", "-f", "lavfi", "-i", "sine=f=293.66:d=5",
    "-f", "lavfi", "-i", "sine=f=440:d=5", "-filter_complex",
    "[0]volume=0.25[a];[1]volume=0.2[b];[2]volume=0.14[c];[3]volume=0.07[d];[a][b][c][d]amix=inputs=4:normalize=0,"
    "lowpass=f=1800,aecho=0.8:0.7:220|390:0.35|0.25,afade=t=in:d=0.9,afade=t=out:st=2.6:d=2.4",
    "-ar", "48000", "-ac", "2", str(tmp / "b.wav"))
ms = int(chord_at * 1000)
run("-i", str(tmp / "a.wav"), "-i", str(tmp / "b.wav"), "-filter_complex",
    f"[1]adelay={ms}|{ms}[b];[0][b]amix=inputs=2:duration=longest:normalize=0,volume=0.8,alimiter=limit=0.5,apad=whole_dur={total}",
    "-ar", "48000", str(ROOT / "assets/audio/bed.wav"))
print(f"bed.wav {total:.1f}s — pad out by {pad_len:.1f}s, chord at {chord_at:.1f}s")
