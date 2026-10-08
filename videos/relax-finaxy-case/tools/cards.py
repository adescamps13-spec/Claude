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

cards["voeux"] = f"""<div class="card" style="background:#E6E1F1">
<div class="a sh" style="left:262px;top:96px;width:330px;height:236px;background:#EFEAE0;transform:rotate(7deg);border-radius:4px"></div>
<div class="a sh" style="left:300px;top:52px;width:250px;height:350px;background:#191853;transform:rotate(-6deg);border-radius:4px;overflow:hidden">
<div class="a" style="left:28px;top:30px">{NEW(96)}</div>
<div class="a serif" style="left:28px;top:150px;font-size:46px;line-height:1;color:#F4F1EB"><i>Meilleurs</i><br><i>vœux</i></div>
<div class="a serif" style="left:28px;top:262px;font-size:58px;color:#5A80D9">2026</div>
<div class="a" style="right:0;top:0;width:60px;height:350px;background:#9C0A3F"></div></div>
<div class="tag" style="color:#6955AA">CARTES DE VŒUX</div></div>"""

cards["masque"] = f"""<div class="card" style="background:#DCE3F5">
<div class="a sh" style="left:110px;top:66px;width:620px;height:349px;background:#F4F1EB;border-radius:6px;overflow:hidden">
<div class="a" style="left:0;top:0;width:200px;height:349px;background:#191853"></div>
<div class="a" style="left:30px;top:30px">{NEW(110)}</div>
<div class="a" style="left:30px;bottom:30px;font-size:13px;letter-spacing:.14em;color:#A9AFD6;font-weight:600">01 / 24</div>
<div class="a serif" style="left:238px;top:96px;width:350px;font-size:44px;line-height:1.05;color:#191853">Ensemble, protégeons ce qui compte.</div>
<div class="a" style="left:240px;top:230px;width:60px;height:4px;background:#9C0A3F"></div>
<div class="a" style="left:240px;top:256px;width:300px;font-size:14px;line-height:1.5;color:#4A5892">Réunir les meilleures expertises pour vous conseiller et bâtir, ensemble, des solutions d’assurance adaptées.</div></div>
<div class="tag" style="color:#4A5892">MASQUES DE PRÉSENTATION</div></div>"""

broch = lambda x, rot, bg, title, z: f"""<div class="a sh" style="left:{x}px;top:72px;width:230px;height:326px;background:{bg};transform:rotate({rot}deg);border-radius:3px;overflow:hidden;z-index:{z}">
<div class="a" style="left:22px;top:24px">{NEW(84)}</div>
<div class="a serif" style="left:22px;top:170px;font-size:31px;line-height:1.04;color:#F4F1EB">{title}</div>
<div class="a" style="left:22px;top:284px;width:40px;height:3px;background:#F4F1EB;opacity:.7"></div></div>"""
cards["plaquette"] = f"""<div class="card" style="background:#F1EEE6">
{broch(150, -8, '#4A5892', 'Clientèle<br>privée', 1)}{broch(310, -1, '#5A80D9', 'Affinitaire &amp;<br>partenariats', 2)}{broch(470, 6, '#191853', 'Entreprises &amp;<br>institutions', 3)}
<div class="tag" style="color:#4A5892">PLAQUETTES</div></div>"""

kak = lambda x, bg, fg, line, logo_svg: f"""<div class="a" style="left:{x}px;top:40px;width:150px;height:380px;background:{bg};box-shadow:0 24px 40px rgba(25,24,83,.25);overflow:hidden">
<div class="a" style="left:20px;top:26px">{logo_svg}</div>
<div class="a serif" style="left:20px;top:150px;width:116px;font-size:28px;line-height:1.05;color:{fg}">{line}</div>
<div class="a" style="left:0;bottom:0;width:150px;height:44px;background:#9C0A3F"></div></div>
<div class="a" style="left:{x - 14}px;top:420px;width:178px;height:14px;border-radius:7px;background:#B7B4C4"></div>"""
cards["kakemono"] = f"""<div class="card" style="background:#E6E1F1">
{kak(250, '#191853', '#F4F1EB', 'Ensemble, protégeons ce qui compte.', NEW(108))}{kak(440, '#F4F1EB', '#191853', 'Une intelligence collective du risque.', NEW(108, '#191853'))}
<div class="tag" style="color:#6955AA">KAKEMONOS</div></div>"""

cards["cartes"] = f"""<div class="card" style="background:#DCE3F5">
<div class="a sh" style="left:150px;top:118px;width:360px;height:206px;background:#191853;border-radius:8px;transform:rotate(-9deg)">
<div class="a" style="left:96px;top:72px">{NEW(170)}</div></div>
<div class="a sh" style="left:360px;top:176px;width:360px;height:206px;background:#F4F1EB;border-radius:8px;transform:rotate(5deg)">
<div class="a serif" style="left:28px;top:30px;font-size:34px;color:#191853">Prénom Nom</div>
<div class="a" style="left:28px;top:76px;font-size:14px;color:#4A5892">Fonction</div>
<div class="a" style="left:28px;bottom:26px;font-size:13px;color:#191853">finaxy.com</div>
<div class="a" style="right:24px;bottom:24px">{NEW(88, '#191853')}</div></div>
<div class="tag" style="color:#4A5892">CARTES DE VISITE</div></div>"""

cards["reseaux"] = f"""<div class="card" style="background:#F1EEE6">
<div class="a sh" style="left:300px;top:40px;width:500px;height:400px;background:#fff;border-radius:16px;overflow:hidden">
<div class="a" style="left:0;top:0;width:500px;height:120px;background:linear-gradient(120deg,#191853 0%,#262577 60%,#5A80D9 100%)"></div>
<div class="a" style="right:26px;top:36px">{NEW(120)}</div>
<div class="a serif" style="left:26px;top:76px;width:88px;height:88px;border-radius:44px;background:#191853;border:4px solid #fff;color:#F4F1EB;font-size:60px;line-height:78px;text-align:center">F</div>
<div class="a" style="left:26px;top:176px;font-weight:600;font-size:22px;color:#191853">Finaxy</div>
<div class="a" style="left:26px;top:206px;font-size:14px;color:#4A5892">Conseil et courtage en assurances</div>
<div class="a" style="right:26px;top:180px;padding:8px 22px;border-radius:20px;background:#191853;color:#F4F1EB;font-size:14px;font-weight:600">Suivre</div>
<div class="a" style="left:26px;top:246px;width:448px;height:130px;border-radius:12px;background:#F4F1EB;overflow:hidden">
<div class="a" style="left:0;top:0;width:130px;height:130px;background:#191853"><div class="a" style="left:22px;top:52px">{NEW(86)}</div></div>
<div class="a serif" style="left:150px;top:22px;width:280px;font-size:22px;line-height:1.12;color:#191853">La nouvelle identité de marque Finaxy, à l’image de ce que nous sommes devenus</div></div></div>
<div class="tag" style="color:#4A5892">PAGES RÉSEAUX SOCIAUX</div></div>"""

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
