"""Assemble index.html + compositions/*.html from tools/scenes/*.html and tools/timing.json.

Retiming to the real voiceover = edit tools/timing.json (scene durations, VO offsets), rerun:
    python3 tools/build.py
Scene templates use placeholders: {{ID}} {{D}} {{FINAXY_NEW}} {{FINAXY_OLD}} {{RELAX}}
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
#root .wash{position:absolute;inset:-10%;background:
  radial-gradient(42% 46% at 14% 62%, rgba(86,160,170,.30) 0%, rgba(255,255,255,0) 100%),
  radial-gradient(36% 40% at 84% 58%, rgba(171,162,86,.28) 0%, rgba(255,255,255,0) 100%),
  radial-gradient(28% 30% at 50% 52%, rgba(105,85,170,.20) 0%, rgba(255,255,255,0) 100%)}
#root svg.stage{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
#root .t-title{font-family:Unbounded,sans-serif;font-weight:400;letter-spacing:-.01em}
#root .t-serif{font-family:'Instrument Serif',serif;font-weight:400}
#root .abs{position:absolute}
#root .rail{position:absolute;left:120px;top:78px;display:flex;gap:56px;font-size:22px;font-weight:600;color:#747779}
#root .rail .n{font-family:Unbounded,sans-serif;font-weight:500;margin-right:14px}
#root .rail .on{color:#212C34}
#root .rail .on .n{color:#6955AA}
#root .rail .done{color:#4F575D}
#root .rail-bar{position:absolute;left:120px;top:126px;height:3px;background:#6955AA;transform-origin:left center}
"""

RAIL_STEPS = ["Comprendre", "Révéler", "Organiser", "Exprimer", "Déployer"]
RAIL_W = [262, 196, 236, 214, 214]  # measured text widths at 22px + gap, for the bar length


def rail_html(active):
    items = []
    for i, s in enumerate(RAIL_STEPS, 1):
        cls = "on" if i == active else ("done" if i < active else "")
        items.append(f'<div class="{cls}"><span class="n">0{i}</span>{s}</div>')
    bar = sum(RAIL_W[: active - 1]) + (active - 1) * 56 + RAIL_W[active - 1] - 30
    return f'<div class="rail">{"".join(items)}</div><div class="rail-bar" style="width:{bar}px"></div>'


def build_scene(sc):
    src = (ROOT / "tools/scenes" / f'{sc["id"]}.html').read_text()
    rail = re.search(r"\{\{RAIL:(\d)\}\}", src)
    if rail:
        src = src.replace(rail.group(0), rail_html(int(rail.group(1))))
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
        dur = f' data-duration="{a["dur"]}"' if "dur" in a else ""
        audio.append(f'      <audio id="{a["id"]}" src="{a["src"]}" data-start="{round(start, 3)}"{dur} data-track-index="{a.get("track", 1)}"{vol}></audio>')
    html = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Relax × Finaxy — case</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/fil.js"></script>
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
    for sc in T["scenes"]:
        if (ROOT / "tools/scenes" / f'{sc["id"]}.html').exists():
            build_scene(sc)
    total = build_index()
    print(f"built {len(T['scenes'])} scenes, total {total}s")
