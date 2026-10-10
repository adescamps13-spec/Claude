"""Phrase-level timing for each voiceover take, from its real pauses.

No ASR model is reachable in the cloud container, so each take is split on silences
(ffmpeg silencedetect) and the speech segments are matched to the script's phrases
(split on . , : ; … ?). When the counts differ, adjacent phrases are merged into the
segment their character share fits best. Output: tools/vo-cues.json
    python3 tools/vo_cues.py
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
man = json.loads((ROOT / "assets/voice/vo-manifest.json").read_text())


def speech_segments(wav, noise="-38dB", dur=0.22):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", f"silencedetect=n={noise}:d={dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)], capture_output=True, text=True).stdout)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    segs, t = [], 0.0
    for s, e in zip(starts, ends + [total] * (len(starts) - len(ends))):
        if s - t > 0.12:
            segs.append([round(t, 2), round(s, 2)])
        t = e
    if total - t > 0.12:
        segs.append([round(t, 2), round(total, 2)])
    return segs, total


def phrases(text):
    parts = [p.strip() for p in re.split(r"(?<=[.,:;…?])\s+", text) if p.strip()]
    return parts


def align(ph, segs):
    """Greedy: give each segment consecutive phrases until its share of characters is used."""
    if len(segs) >= len(ph):
        # more segments than phrases: merge the shortest gaps first
        while len(segs) > len(ph):
            gaps = [(segs[i + 1][0] - segs[i][1], i) for i in range(len(segs) - 1)]
            _, i = min(gaps)
            segs[i:i + 2] = [[segs[i][0], segs[i + 1][1]]]
        return [{"text": p, "start": s[0], "end": s[1]} for p, s in zip(ph, segs)]
    out, j = [], 0
    speech = sum(e - s for s, e in segs)
    chars = sum(len(p) for p in ph)
    for k, (s, e) in enumerate(segs):
        take = []
        quota = (e - s) / speech * chars
        while j < len(ph) and (not take or sum(len(x) for x in take) + len(ph[j]) / 2 <= quota) and (len(ph) - j > len(segs) - k - 1 or not take):
            take.append(ph[j])
            j += 1
        # spread the segment over its phrases by character share
        t = s
        for p in take:
            d = (e - s) * len(p) / sum(len(x) for x in take)
            out.append({"text": p, "start": round(t, 2), "end": round(t + d, 2)})
            t += d
    return out


# Phrase starts read by hand from fine silences (silencedetect -36dB / 80 ms) where the greedy
# alignment drifts (micro-pauses inside long phrases). One start per script phrase.
MANUAL = {
    "1": [0.33, 3.19, 4.98, 7.60, 11.32, 13.21],
    "2": [0.28, 2.53, 5.42, 7.43, 9.62, 11.22, 12.30, 14.22, 14.70, 17.18, 21.66, 23.72, 26.38],
    "3": [0.28, 1.27, 3.02, 4.16, 5.11, 6.08, 7.44, 8.16, 9.99, 11.12, 14.56, 15.67, 17.47],
    "4": [0.38, 2.56, 4.06, 4.87, 5.83, 7.08, 8.22, 10.89, 12.41, 13.89],
    "5": [0.32, 1.87, 4.64, 5.44, 8.39, 9.60, 12.94, 16.11, 17.15, 18.48, 19.42, 20.39, 21.91, 22.68],
}

res = {}
for k in sorted(man, key=int):
    m = man[k]
    segs, total = speech_segments(ROOT / m["file"])
    ph = phrases(m["text"])
    if k in MANUAL and len(MANUAL[k]) == len(ph):
        st = MANUAL[k] + [segs[-1][1]]
        al = [{"text": p, "start": st[i], "end": round(st[i + 1] - 0.05, 2)} for i, p in enumerate(ph)]
    else:
        al = align(ph, segs)
    res[k] = {"frame": m["frame"], "seconds": round(total, 2), "phrases": al}
(ROOT / "tools/vo-cues.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
for k, v in res.items():
    print(f"line {k} ({v['seconds']}s)")
    for p in v["phrases"]:
        print(f"   {p['start']:6.2f}–{p['end']:6.2f}  {p['text']}")
