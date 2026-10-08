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
"""


def hud_html(spec):
    color, label = spec.split("|", 1)
    return (f'<div class="hud" style="left:70px;color:{color}">RELAX × FINAXY</div>'
            f'<div class="hud" style="right:70px;color:{color}">{label}</div>')


def build_scene(sc):
    src = (ROOT / "tools/scenes" / f'{sc["id"]}.html').read_text()
    src = re.sub(r"\{\{HUD:([^}]+)\}\}", lambda m: hud_html(m.group(1)), src)
    src = src.replace("§", sc["id"] + "-")
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
      <div id="root" data-composition-id="{sc["id"]}" data-width="{W}" data-height="{H}" data-duration="{sc["dur"]}">
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
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    return total


if __name__ == "__main__":
    (ROOT / "compositions").mkdir(exist_ok=True)
    for sc in T["scenes"]:
        if (ROOT / "tools/scenes" / f'{sc["id"]}.html').exists():
            build_scene(sc)
    total = build_index()
    print(f"built {len(T['scenes'])} scenes, total {total}s")
