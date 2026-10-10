"""Generate a Relax-style 3D illustration with a Gemini image model (no key sent: the
egress proxy adds it). Illustrations only — never used to fake a Finaxy deliverable.
    python3 tools/gemini-img.py <out.png> "<subject>" [--model nano-banana-pro-preview] [--ref img.png]
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

args = sys.argv[1:]
model = "nano-banana-pro-preview"
refs = []
if "--model" in args:
    i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
while "--ref" in args:
    i = args.index("--ref"); refs.append(args[i + 1]); del args[i:i + 2]
out, subject = args[0], args[1]
STYLE = ("Soft 3D render in the style of a modern design-agency website: smooth glossy clay-and-glass material, "
         "pastel palette of lavender #D4CCEE, periwinkle #A99CF0, soft pink #F4C6E6 and pale cyan #CCEAEE with a subtle "
         "iridescent sheen, gentle studio lighting from the top left, soft contact shadow, isolated object centred on a "
         "pure flat white background (#FFFFFF), lots of empty margin, no text, no letters, no logo, no watermark, "
         "high detail, minimalist, premium.")
parts = [{"text": f"{subject}\n\n{STYLE}"}]
for r in refs:
    parts.append({"inline_data": {"mime_type": "image/png", "data": base64.b64encode(Path(r).read_bytes()).decode()}})
body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
r = json.load(urllib.request.urlopen(req, timeout=300))
for p in r["candidates"][0]["content"]["parts"]:
    if "inlineData" in p or "inline_data" in p:
        d = p.get("inlineData") or p.get("inline_data")
        Path(out).write_bytes(base64.b64decode(d["data"]))
        print("wrote", out, d.get("mimeType"))
        break
else:
    print("no image:", json.dumps(r)[:500])
