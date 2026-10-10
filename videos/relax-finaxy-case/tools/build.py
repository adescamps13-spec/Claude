"""Assemble index.html + compositions/*.html from tools/scenes/*.html and tools/timing.json.

Retiming to the real voiceover = edit tools/timing.json (scene durations, VO offsets), rerun:
    python3 tools/build.py
Scene templates use placeholders: {{ID}} {{D}} {{VO}} {{HUD:color|label}} {{FINAXY_NEW}} {{FINAXY_OLD}} {{RELAX}};
"§" is replaced by "<scene id>-" everywhere (ids, classes, selectors) to keep scenes isolated.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "tools/timing.json").read_text())
W, H = 1920, 1080


def inner_svg(name, **attrs):
    svg = (ROOT / "assets/brand" / name).read_text()
    svg = re.sub(r"<svg[^>]*>", lambda m: "<svg" + "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
                 + ' ' + re.search(r'viewBox="[^"]+"', m.group(0)).group(0) + ' xmlns="http://www.w3.org/2000/svg">', svg, count=1)
    return svg


FONT_FILES = sorted(p.name for p in (ROOT / "assets/fonts").glob("*.woff2"))


def font_faces(prefix):
    out = []
    for fn in FONT_FILES:
        fam, w, st = fn[:-6].split("-")
        fam = {"DMSans": "DM Sans", "InstrumentSerif": "Instrument Serif"}.get(fam, fam)
        out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:block;src:url('{prefix}assets/fonts/{fn}') format('woff2');}}")
    return "\n".join(out)


BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:#FFFFFF;color:#212C34;font-family:'DM Sans',sans-serif}
#root .abs{position:absolute}
#root .full{position:absolute;left:0;top:0;width:1920px;height:1080px}
#root .uni{font-family:Unbounded,sans-serif}
#root .serif{font-family:'Instrument Serif',serif;font-weight:400}
#root .hud{position:absolute;top:60px;font-weight:600;font-size:17px;letter-spacing:.16em;white-space:nowrap}
#root .studio{background:radial-gradient(60% 55% at 50% 44%,#FFFFFF 0%,#F0F0F4 55%,#E3E3EA 100%)}
#root .night{background:#0E0C14}
/* Relax charter (relax-agency.com): white + pastel washes, tinted cards, tag pills, dark gradient pills, cursor */
#root .wash{background:radial-gradient(54.61% 40.94% at 15.14% 59.45%,rgba(85,160,170,.30) 0%,rgba(255,255,255,0) 100%),radial-gradient(40.42% 36.99% at 82.26% 59.45%,rgba(170,162,85,.30) 0%,rgba(255,255,255,.3) 100%),radial-gradient(25.33% 25.33% at 50% 62.91%,rgba(105,85,170,.30) 0%,rgba(255,255,255,.3) 100%),#FFFFFF}
#root .wash-lav{background:linear-gradient(180deg,#FFFFFF 0%,#F4F1FB 40%,#E5E0F5 100%)}
#root .card{position:absolute;border-radius:28px;overflow:hidden}
#root .card-p{background:#CAC3E1;color:#2A2244}#root .card-c{background:#C3DDE1;color:#224044}
#root .card-y{background:#E0DEC3;color:#3B3818}#root .card-r{background:#E1C3C3;color:#432222}
#root .tag{display:inline-block;padding:0 22px;height:44px;line-height:44px;border-radius:22px;font-weight:500;font-size:20px;color:#FFFFFF;white-space:nowrap}
#root .tag-p{background:#6955AA}#root .tag-c{background:#56A0AA}#root .tag-y{background:#8C853F}#root .tag-r{background:#AA5655}
#root .btn{position:absolute;border-radius:999px;background:linear-gradient(90deg,#1F1F1F,#5D5D5D);color:#FFFFFF;font-weight:500;white-space:nowrap;text-align:center}
#root .h-uni{font-family:Unbounded,sans-serif;font-weight:500;letter-spacing:-.01em}
#root .cursor{position:absolute;width:44px;height:44px;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='44' height='44' viewBox='0 0 44 44'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%238e899e'/><stop offset='1' stop-color='%23292438'/></linearGradient></defs><path d='M4 3 L40 17 L23 22 L17 40 Z' fill='url(%23g)' stroke='white' stroke-width='2' stroke-linejoin='round'/></svg>") 0 0/44px 44px no-repeat;z-index:20}
#root .guide-v{position:absolute;width:0;border-left:2px dashed #8E899E}#root .guide-h{position:absolute;height:0;border-top:2px dashed #8E899E}
"""


def hud_html(spec):
    # the per-scene HUD gave way to one interface frame over the whole film (tools/overlays/zz-hud.html)
    return ""


def build_scene(sc, folder="tools/scenes"):
    src = (ROOT / folder / f'{sc["id"]}.html').read_text()
    if "{{SCENES}}" in src:
        starts, t = [], 0.0
        for x in T["scenes"]:
            starts.append([x["id"], round(t, 3), x["dur"]])
            t += x["dur"]
        src = src.replace("{{SCENES}}", json.dumps(starts))
    src = re.sub(r"\{\{HUD:([^}]+)\}\}", lambda m: hud_html(m.group(1)), src)
    src = src.replace("§", sc["id"] + "-")
    src = src.replace("{{THREE}}", '<script src="assets/vendor/three.global.js"></script>\n<script src="assets/vendor/three-addons.js"></script>\n<script src="assets/t3.js"></script>')
    src = (src.replace("{{ID}}", sc["id"]).replace("{{D}}", str(sc["dur"]))
           .replace("{{FINAXY_NEW}}", inner_svg("finaxy-new.svg", id=f'{sc["id"]}-fxnew', class_="fxnew"))
           .replace("{{FINAXY_NEW_NAVY}}", inner_svg("finaxy-new.svg", id=f'{sc["id"]}-fxnavy', class_="fxnew").replace('fill="#F4F1EB"', 'fill="#191853"'))
           .replace("{{FINAXY_OLD}}", inner_svg("finaxy-old.svg", id=f'{sc["id"]}-fxold', class_="fxold").replace('fill="white"', 'fill="#174A8C"'))
           .replace("{{RELAX}}", inner_svg("relax-logo.svg", id=f'{sc["id"]}-relax', class_="relaxlogo")))
    vo = sc.get("vo", {})
    src = src.replace("{{VO}}", json.dumps(vo, ensure_ascii=False))
    doc = f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template>
      <style>
{font_faces("")}
{BASE_CSS}
      </style>
      <div id="root"{' style="background:transparent"' if folder != "tools/scenes" else ""} data-composition-id="{sc["id"]}" data-width="{W}" data-height="{H}" data-duration="{sc["dur"]}">
{src}
      </div>
    </template>
  </body>
</html>
"""
    (ROOT / "compositions" / f'{sc["id"]}.html').write_text(doc)


def build_index():
    t, hosts = 0.0, []
    for i, sc in enumerate(T["scenes"]):
        sc["start"] = round(t, 3)
        if (ROOT / "compositions" / f'{sc["id"]}.html').exists():
            hosts.append(f'''      <div id="host-{sc["id"]}" class="clip" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html"
        data-start="{sc["start"]}" data-duration="{sc["dur"]}" data-track-index="0" data-width="{W}" data-height="{H}"></div>''')
        t += sc["dur"]
    total = round(t, 3)
    # overlays across the whole film: interface frame + cut transitions
    for k, ov in enumerate(OVERLAYS):
        hosts.append(f'''      <div id="host-{ov}" class="clip" data-composition-id="{ov}" data-composition-src="compositions/{ov}.html"
        data-start="0" data-duration="{total}" data-track-index="{5 + k}" data-width="{W}" data-height="{H}"></div>''')
    # a living camera: every shot drifts in slowly (alternating direction)
    cam = []
    for i, sc in enumerate(T["scenes"]):
        if sc["id"] in ("f-relax",):
            continue
        dx = 14 if i % 2 else -14
        cam.append(f'      tl.fromTo("#host-{sc["id"]}", {{ scale: 1, x: 0 }}, {{ scale: 1.03, x: {dx}, duration: {sc["dur"]}, ease: "none", immediateRender: false }}, {sc["start"]});')
    audio = []
    for a in T.get("audio", []):
        start = a["start"] if "start" in a else T["scenes"][a["scene"]]["start"] + a.get("offset", 0)
        if not (ROOT / a["src"]).exists():
            continue
        vol = f' data-volume="{a["volume"]}"' if "volume" in a else ""
        if "dur" not in a:
            import wave
            with wave.open(str(ROOT / a["src"])) as w:
                a["dur"] = round(w.getnframes() / w.getframerate(), 2)
        a["dur"] = min(a["dur"], round(total - start, 3))
        dur = f' data-duration="{a["dur"]}"'
        grp = f' data-audio-group="{a["group"]}"' if "group" in a else ""
        fx = ""
        carve = ROOT / "tools" / f'{a["id"]}-carve.attrs'
        if carve.exists():  # voiceover carve written by hyperframes-audio/scripts/carve.mjs, kept across rebuilds
            fx = " " + carve.read_text().strip()
        audio.append(f'      <audio id="{a["id"]}" src="{a["src"]}" data-start="{round(start, 3)}"{dur} data-track-index="{a.get("track", 1)}"{vol}{grp}{fx}></audio>')
    html = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Relax × Finaxy — case</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/kit.js"></script>
    <style>
{font_faces("")}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #FFFFFF; }}
      #main-root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #FFFFFF; }}
    </style>
  </head>
  <body>
    <div id="main-root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}" data-fps="30">
{chr(10).join(hosts)}
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cam)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    return total


OVERLAYS = ["zz-trans", "zz-hud"]

if __name__ == "__main__":
    (ROOT / "compositions").mkdir(exist_ok=True)
    _total = round(sum(x["dur"] for x in T["scenes"]), 3)
    for ov in OVERLAYS:
        build_scene({"id": ov, "dur": _total, "vo": {}}, "tools/overlays")
    for sc in T["scenes"]:
        if (ROOT / "tools/scenes" / f'{sc["id"]}.html').exists():
            build_scene(sc)
    total = build_index()
    print(f"built {len(T['scenes'])} scenes, total {total}s")
