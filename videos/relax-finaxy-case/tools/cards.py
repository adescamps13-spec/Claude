"""Pre-render the Finaxy deliverable cards (840x480 PNG) that ride the film strips, plus the
site and photo crops. Writes tools/cards/cards.html, then shoots each #id with tools/cardshot.mjs.
    python3 tools/cards.py
"""
import re
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/cards"
OUT.mkdir(exist_ok=True)
FONTS = ROOT / "assets/fonts"


def logo(name, w, fill, accent=None):
    s = (ROOT / "assets/brand" / name).read_text()
    s = re.sub(r'<svg[^>]*?(viewBox="[^"]+")[^>]*>', rf'<svg width="{w}" \1 xmlns="http://www.w3.org/2000/svg" style="display:block">', s, count=1)
    s = s.replace('fill="#F4F1EB"', f'fill="{fill}"').replace('fill="white"', f'fill="{fill}"')
    if accent:
        s = s.replace('fill="#9C0A3F"', f'fill="{accent}"')
    return s


NEW = lambda w, fill="#F4F1EB", acc=None: logo("finaxy-new.svg", w, fill, acc)
OLD = lambda w, fill="#174A8C": logo("finaxy-old.svg", w, fill)
BARS = [26, 103, 148, 147, 107, 54, 33, 36, 42, 72, 79, 49, 64, 131, 171, 164, 112, 36, 81, 111, 100, 64, 32, 27, 55, 97, 127, 119, 68, 61, 133, 168, 155, 103]

CSS = f"""
@font-face{{font-family:Unbounded;font-weight:500;src:url('file://{FONTS}/Unbounded-500-normal.woff2')}}
@font-face{{font-family:'DM Sans';font-weight:400;src:url('file://{FONTS}/DMSans-400-normal.woff2')}}
@font-face{{font-family:'DM Sans';font-weight:500;src:url('file://{FONTS}/DMSans-500-normal.woff2')}}
@font-face{{font-family:'DM Sans';font-weight:600;src:url('file://{FONTS}/DMSans-600-normal.woff2')}}
@font-face{{font-family:'Instrument Serif';src:url('file://{FONTS}/InstrumentSerif-400-normal.woff2')}}
@font-face{{font-family:'Instrument Serif';font-style:italic;src:url('file://{FONTS}/InstrumentSerif-400-italic.woff2')}}
*{{margin:0;box-sizing:border-box}}body{{background:transparent;width:840px}}
.card{{position:relative;width:840px;height:480px;border-radius:26px;overflow:hidden;margin-bottom:10px;font-family:'DM Sans'}}
.a{{position:absolute}}.serif{{font-family:'Instrument Serif'}}
.tag{{position:absolute;left:40px;top:34px;font-weight:600;font-size:17px;letter-spacing:.16em;color:#6B7278}}
.sh{{box-shadow:0 30px 60px rgba(25,24,83,.28),0 6px 14px rgba(25,24,83,.16)}}
.pill{{display:inline-block;border:1.5px solid rgba(244,241,235,.8);border-radius:20px;padding:6px 14px;font-size:13px;color:#F4F1EB;margin:0 6px 8px 0}}
"""

cards = {}
cards["ecouter"] = f"""<div class="card" style="background:#fff">
<div class="tag">ÉCOUTER</div>
<div class="a" style="left:70px;right:70px;top:110px;height:200px;display:flex;align-items:center;justify-content:space-between">
{''.join(f'<i style="display:block;width:14px;border-radius:7px;background:#6955AA;height:{h}px"></i>' for h in BARS)}</div>
<div class="a" style="left:60px;right:60px;bottom:60px;display:flex;justify-content:space-between;font-family:Unbounded;font-weight:500;font-size:26px;color:#212C34">
<span>dirigeants</span><span>collaborateurs</span><span>métiers</span><span>marché</span></div></div>"""

cards["comprendre"] = f"""<div class="card" style="background:#F4F1EB">
<div class="a" style="left:0;top:0;width:420px;height:480px;background:#191853"></div>
<div class="a serif" style="left:56px;top:150px;font-size:66px;line-height:1.02;color:#F4F1EB">La force<br>d’un groupe</div>
<div class="a serif" style="left:476px;top:150px;font-size:66px;line-height:1.02;color:#191853"><i>L’esprit</i><br><i>d’un cabinet</i></div>
<div class="a" style="left:56px;bottom:56px;font-weight:600;font-size:15px;letter-spacing:.16em;color:#A9AFD6">PUISSANCE</div>
<div class="a" style="left:476px;bottom:56px;font-weight:600;font-size:15px;letter-spacing:.16em;color:#4A5892">PROXIMITÉ</div>
<div class="a" style="left:384px;top:204px;width:72px;height:72px;border-radius:36px;background:#9C0A3F;color:#F4F1EB;font-family:Unbounded;font-size:40px;line-height:70px;text-align:center">+</div></div>"""

cards["intel"] = f"""<div class="card" style="background:radial-gradient(80% 90% at 30% 20%,#262577 0%,#191853 60%,#121142 100%)">
<div class="a serif" style="left:0;right:0;top:118px;text-align:center;font-size:80px;line-height:1.02;color:#F4F1EB">Une intelligence<br>collective du risque.</div>
<div class="a" style="left:380px;top:332px;width:80px;height:5px;border-radius:3px;background:#9C0A3F"></div>
<div class="a" style="left:345px;top:384px">{NEW(150)}</div></div>"""

# Relax-charter listening panels (relax-agency.com service cards: pastel card, tag pill, Unbounded title)
LISTEN = [("dirigeants", "#CAC3E1", "#6955AA", "#2A2244"), ("collaborateurs", "#C3DDE1", "#56A0AA", "#224044"),
          ("métiers", "#E0DEC3", "#8C853F", "#3B3818"), ("marché", "#E1C3C3", "#AA5655", "#432222")]
for i, (word, bg, tagc, ink) in enumerate(LISTEN):
    hs = [abs(((j * 37 + i * 11) % 23) - 11) * 9 + 22 for j in range(30)]
    bars = "".join(f'<i style="display:block;width:12px;border-radius:6px;height:{h}px;background:linear-gradient(180deg,{tagc},{tagc}99)"></i>' for h in hs)
    cards[f"ecoute{i}"] = f"""<div class="card" style="background:{bg}">
<div class="a" style="left:44px;top:40px;padding:0 22px;height:44px;line-height:44px;border-radius:22px;background:{tagc};color:#fff;font-weight:500;font-size:20px">On écoute</div>
<div class="a" style="left:44px;top:112px;font-family:Unbounded;font-weight:500;font-size:64px;color:{ink};letter-spacing:-.01em">{word}</div>
<div class="a" style="left:44px;right:44px;bottom:70px;height:190px;display:flex;align-items:center;justify-content:space-between">{bars}</div></div>"""

# real Finaxy deliverables (files supplied by the client / Relax, assets/real/), never mock-ups:
# each is laid on an 840x480 card, full bleed when the ratio allows, otherwise contained on its own edge colour
REAL = {"voeux": ("voeux-2026.jpg", "contain"), "enseigne": ("enseigne.jpg", "cover"), "affiches": ("affiches.jpg", "cover"), "plaquette": ("plaquette.jpg", "contain"),
        "kakemono": ("kakemono.jpg", "contain"), "cartes": ("cartes-visite.jpg", "contain"), "reseaux": ("linkedin.jpg", "contain")}


def edge_colour(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = [im.getpixel((x, y)) for x in (2, w // 2, w - 3) for y in (2, h - 3)]
    return "#%02X%02X%02X" % tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))


for k, (fn, mode) in REAL.items():
    src = ROOT / "assets/real" / fn
    if mode == "cover":
        cards[k] = f'''<div class="card" style="background:url('file://{src}') center/cover"></div>'''
    else:
        cards[k] = f'''<div class="card" style="background:{edge_colour(src)} url('file://{src}') center/contain no-repeat"></div>'''

cards["oldlogo"] = f"""<div class="card" style="background:#FFFFFF;width:520px;height:330px">
<div class="a" style="left:110px;top:115px">{OLD(300)}</div></div>"""
cards["newlogo"] = f"""<div class="card" style="background:linear-gradient(135deg,#22216A 0%,#191853 60%,#10103E 100%);width:520px;height:330px">
<div class="a" style="left:90px;top:112px">{NEW(340)}</div></div>"""

html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" + "".join(
    c.replace('<div class="card"', f'<div id="{k}" class="card"', 1) for k, c in cards.items()) + "</body></html>"
(ROOT / "tools/cards").mkdir(exist_ok=True)
(ROOT / "tools/cards/cards.html").write_text(html)
subprocess.run(["node", str(ROOT / "tools/cardshot.mjs"), str(ROOT / "tools/cards/cards.html"), str(OUT), *cards], check=True)

# real site: header + the content below the (empty, carousel) hero, as one long page
site = Image.open(ROOT / "assets/captures/finaxy-site-2026-full.png").convert("RGB")
w, h = site.size
nav = site.crop((0, 0, w, 128))
body = site.crop((0, 900, w, h))
long = Image.new("RGB", (w, 128 + body.size[1]))
long.paste(nav, (0, 0))
long.paste(body, (0, 128))
long.save(OUT / "site-long.jpg", quality=88)
# the people photo from the site's contact band
site.crop((760, 3353, 1440, 3700)).save(OUT / "humain.jpg", quality=90)
print("cards:", ", ".join(cards), "+ site-long.jpg, humain.jpg")
