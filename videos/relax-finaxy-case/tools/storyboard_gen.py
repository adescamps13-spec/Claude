"""Generate storyboard.html (review sheet) for the Relax x Finaxy case.

Each cell is an inline SVG on the real 1920x1080 canvas, so placement and type
sizes read exactly as they will in the build. Deterministic (seeded) layout.
"""
import math
import random
import sys
from pathlib import Path

PROJECT = Path(sys.argv[1])
VERSION = sys.argv[2] if len(sys.argv) > 2 else "v1"

INK, CREAM, BURG, BURG_LIT, BEFORE, MUTED = "#14110F", "#F4F1EB", "#9C0A3F", "#C2185B", "#5E7891", "#B9B2A6"
SERIF, SANS = "Instrument Serif, Georgia, serif", "Manrope, Helvetica, Arial, sans-serif"

new_logo = (PROJECT / "assets/brand/finaxy-new.svg").read_text()
old_logo = (PROJECT / "assets/brand/finaxy-old.svg").read_text()


def logo(svg, x, y, w, opacity=1.0):
    """Embed a logo svg at x,y with width w (keeps its own viewBox)."""
    inner = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    head = svg.split(">", 1)[0]
    vb = head.split('viewBox="')[1].split('"')[0].split()
    vw, vh = float(vb[2]), float(vb[3])
    h = w * vh / vw
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{" ".join(vb)}" '
            f'opacity="{opacity}">{inner}</svg>')


def t(x, y, s, size, fam=SANS, fill=CREAM, weight=400, anchor="start", italic=False, ls=0, opacity=1, upper=False):
    style = f'font-family:{fam};font-size:{size}px;font-weight:{weight};letter-spacing:{ls}em'
    if italic:
        style += ";font-style:italic"
    if upper:
        s = s.upper()
    return (f'<text x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}" opacity="{opacity}" '
            f'style="{style}">{s}</text>')


def rail(active):
    steps = ["Comprendre", "Révéler", "Organiser", "Exprimer", "Déployer"]
    out, x = [], 120
    for i, s in enumerate(steps, 1):
        on = i == active
        done = i < active
        col = CREAM if on else (MUTED if done else "#5a524a")
        out.append(t(x, 112, f"0{i}", 22, weight=800, fill=BURG_LIT if on else col, ls=0.1))
        out.append(t(x + 40, 112, s, 22, weight=600, fill=col, ls=0.16, upper=True))
        x += 300
    out.append(f'<line x1="120" y1="136" x2="{120 + 300 * (active - 1) + 250}" y2="136" stroke="{BURG}" stroke-width="3"/>')
    return "".join(out)


def bg(glow_x=1400, glow_y=300, extra=""):
    return (f'<rect width="1920" height="1080" fill="{INK}"/>'
            f'<circle cx="{glow_x}" cy="{glow_y}" r="700" fill="url(#glow)"/>{extra}')


def thread(d, w=5, opacity=1):
    return f'<path d="{d}" fill="none" stroke="{BURG_LIT}" stroke-width="{w}" stroke-linecap="round" opacity="{opacity}"/>'


def node(x, y, r=9, fill=BEFORE, label=None, lsize=24, lfill=None, ring=False):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
    if ring:
        s += f'<circle cx="{x}" cy="{y}" r="{r + 14}" fill="none" stroke="{BURG_LIT}" stroke-width="3"/>'
    if label:
        s += t(x + r + 12, y + lsize * 0.35, label, lsize, fill=lfill or MUTED, weight=600)
    return s


def placeholder(x, y, w, h, label, fill="#221d1a", stroke="#3a332d", lsize=22, rx=10):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y + h}" stroke="{stroke}" stroke-width="2"/>'
            f'<line x1="{x + w}" y1="{y}" x2="{x}" y2="{y + h}" stroke="{stroke}" stroke-width="2"/>'
            + t(x + w / 2, y + h + lsize + 10, label, lsize, anchor="middle", fill=MUTED, weight=600))


DEFS = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{BURG}" stop-opacity=".28"/>'
        f'<stop offset="1" stop-color="{BURG}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="glowc"><stop offset="0" stop-color="{CREAM}" stop-opacity=".10"/>'
        f'<stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient></defs>')

CHAOS_LABELS = ["IARD", "Santé", "Prévoyance", "Cyber", "Flottes", "Construction", "RC Pro", "Crédit",
                "Voyage", "Collection", "Cabinet", "Cabinet", "Marque acquise", "Marque acquise",
                "Transport", "Agricole", "Expertise", "Interlocuteur", "Interlocuteur", "Héritage"]

rng = random.Random(7)
CHAOS = [(rng.uniform(140, 1780), rng.uniform(200, 960)) for _ in CHAOS_LABELS]


def f01():
    s = bg(400, 800, '<circle cx="1500" cy="250" r="600" fill="url(#glowc)"/>')
    for (x, y), lab in zip(CHAOS, CHAOS_LABELS):
        if 640 < x < 1300 and 380 < y < 700:
            continue
        s += node(x, y, r=rng.choice([6, 8, 11]), label=lab, lsize=22, lfill="#7d8a96")
    s += logo(old_logo, 760, 430, 400, opacity=0.9)
    s += t(120, 990, "+ 12 000", 150, fam=SERIF, fill=CREAM)
    s += t(640, 990, "entreprises clientes", 40, fill=MUTED, weight=300)
    return s


def f02():
    s = bg(1500, 700)
    s += t(120, 380, "Pas un problème de", 64, fill=MUTED, weight=300)
    s += t(120, 520, "logo.", 150, fam=SERIF, fill=MUTED, opacity=0.55)
    s += f'<line x1="110" y1="478" x2="440" y2="478" stroke="{BURG_LIT}" stroke-width="7"/>'
    s += t(120, 650, "Un problème de", 64, fill=CREAM, weight=300)
    s += t(120, 820, "cohérence.", 190, fam=SERIF, fill=CREAM, italic=True)
    pts = [(1280, 300), (1460, 420), (1620, 280), (1350, 600), (1560, 700), (1740, 540), (1420, 860), (1700, 880)]
    for i, (x, y) in enumerate(pts):
        s += node(x, y, r=10, fill=CREAM if i == 0 else BEFORE, ring=i == 0)
    s += thread("M0 1010 C 980 1010, 1080 330, 1280 300", 5)
    s += t(1800, 1000, "simplifier, sans appauvrir", 34, fam=SERIF, italic=True, anchor="end", fill=MUTED)
    return s


def f03():
    s = bg(900, 600) + rail(1)
    pts = [(260, 640, "dirigeants"), (640, 440, "collaborateurs"), (1040, 700, "métiers"), (1440, 460, "marché")]
    d = "M0 820 " + " ".join(f"S {x - 120} {y + 160}, {x} {y}" for x, y, _ in pts) + " S 1760 760, 1920 700"
    s += thread(d, 5)
    for x, y, lab in pts:
        s += node(x, y, r=12, fill=CREAM, ring=True)
        s += t(x, y - 50, lab, 60, fam=SERIF, anchor="middle", fill=CREAM)
    s += t(120, 990, "Comprendre ce que Finaxy était vraiment.", 40, fill=MUTED, weight=300)
    for x, y in [(380, 300), (860, 900), (1260, 260), (1700, 940), (1650, 300)]:
        s += node(x, y, r=7, fill=BEFORE)
    return s


def f04():
    s = bg(960, 560) + rail(2)
    rng2 = random.Random(3)
    left = [(rng2.uniform(200, 760), rng2.uniform(320, 860)) for _ in range(12)]
    right = [(rng2.uniform(1160, 1720), rng2.uniform(320, 860)) for _ in range(12)]
    for grp in (left, right):
        for i, (x, y) in enumerate(grp):
            for (x2, y2) in grp[i + 1:i + 3]:
                s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#5a524a" stroke-width="2"/>'
        for x, y in grp:
            s += node(x, y, r=8, fill=CREAM)
    s += thread("M480 590 C 760 420, 1160 760, 1440 590", 6)
    s += t(480, 980, "La force d'un groupe.", 64, fam=SERIF, anchor="middle")
    s += t(1440, 980, "L'esprit d'un cabinet.", 64, fam=SERIF, anchor="middle", italic=True)
    return s


def f05():
    s = bg(960, 540)
    rng3 = random.Random(5)
    pts = [(rng3.uniform(60, 1860), rng3.uniform(60, 1020)) for _ in range(40)]
    for i, (x, y) in enumerate(pts):
        for (x2, y2) in pts[i + 1:i + 3]:
            s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#2c2622" stroke-width="2"/>'
        s += f'<circle cx="{x}" cy="{y}" r="5" fill="#3a332d"/>'
    s += f'<rect x="200" y="380" width="1520" height="330" fill="{INK}" opacity=".85"/>'
    s += t(960, 520, "L'intelligence collective", 150, fam=SERIF, anchor="middle")
    s += t(960, 670, "du risque.", 150, fam=SERIF, anchor="middle", italic=True)
    s += thread("M0 790 L 1920 790", 4)
    return s


def f06():
    s = bg(960, 300) + rail(3)
    s += node(960, 260, r=14, fill=CREAM, ring=True)
    s += t(990, 272, "Finaxy", 52, fam=SERIF)
    cats = [(360, "Entreprises"), (760, "Dirigeants"), (1160, "Particuliers"), (1560, "Affinitaires")]
    for x, lab in cats:
        s += f'<path d="M960 290 C 960 380, {x} 380, {x} 470" fill="none" stroke="{BURG_LIT}" stroke-width="4"/>'
        s += node(x, 480, r=11, fill=CREAM)
        s += t(x, 540, lab, 40, fam=SERIF, anchor="middle")
        for j in range(3):
            yy = 620 + j * 70
            s += f'<line x1="{x}" y1="560" x2="{x}" y2="{yy}" stroke="#5a524a" stroke-width="2"/>'
            s += node(x, yy, r=6, fill=MUTED, label="offre", lsize=22)
    for x, y in [(160, 860), (1760, 860)]:
        s += f'<line x1="{x}" y1="{y}" x2="{960}" y2="290" stroke="{MUTED}" stroke-width="2" stroke-dasharray="8 10" opacity=".5"/>'
        s += node(x, y, r=10, fill=BEFORE, label="marque autonome" if x < 900 else None, lsize=22)
    s += t(1700, 900, "marque autonome", 22, fill=MUTED, weight=600, anchor="end")
    s += t(120, 1010, "architecture · verticales · naming · place de chaque marque", 32, fill=MUTED, weight=300)
    return s


def f07():
    s = bg(960, 520) + rail(4)
    s += logo(old_logo, 140, 220, 260, opacity=0.25)
    s += t(270, 330, "avant", 22, fill=MUTED, weight=600, anchor="middle", upper=True, ls=0.18)
    s += logo(new_logo, 520, 330, 880)
    s += thread("M0 700 C 600 700, 1300 640, 1340 345", 5, 0.9)
    traits = [(250, 860, "Ancré"), (740, 940, "Architecte"), (1200, 940, "Team player"), (1680, 860, "Pédagogue")]
    for x, y, lab in traits:
        s += t(x, y, lab, 56, fam=SERIF, anchor="middle", italic=True)
    s += t(1800, 230, "un logo · une identité · une voix", 30, fill=MUTED, weight=300, anchor="end")
    return s


def f08():
    s = bg(1500, 500) + rail(5)
    labels = ["Plaquettes B2B", "Kakemonos", "Cartes de visite", "Masques de présentation",
              "Cartes de vœux", "LinkedIn", "Nouveau site", "Agent IA"]
    # exponential wall: big first card, then progressively smaller ones
    x0, y0 = 120, 240
    s += placeholder(x0, y0, 420, 560, labels[0], lsize=26)
    sizes = [(600, 240, 300, 380), (960, 240, 300, 380), (600, 700, 140, 120), (780, 700, 140, 120),
             (960, 700, 140, 120), (1140, 700, 140, 120)]
    for i, (x, y, w, h) in enumerate(sizes):
        s += placeholder(x, y, w, h, labels[1 + i % 6] if i < 2 else "", lsize=22)
    gx, gy = 1340, 240
    for r in range(8):
        for c in range(8):
            s += f'<rect x="{gx + c * 62}" y="{gy + r * 62}" width="50" height="50" rx="4" fill="#221d1a" stroke="#3a332d" stroke-width="2"/>'
    s += t(1340 + 248, 790, "×2 ×2 ×2 …", 36, fam=SERIF, italic=True, anchor="middle", fill=CREAM)
    s += thread("M330 520 C 520 520, 600 430, 750 430 S 1000 430, 1110 430 S 1300 300, 1590 360", 4)
    s += f'<rect x="600" y="880" width="1200" height="110" rx="55" fill="#221d1a" stroke="{BURG}" stroke-width="3"/>'
    s += t(650, 948, "Agent IA ·", 30, fill=BURG_LIT, weight=800)
    s += t(820, 948, "« On réunit les bonnes expertises pour construire une réponse adaptée… »", 28, fill=CREAM, weight=300)
    s += t(120, 1000, "visuels réels à fournir", 22, fill=MUTED, weight=600, upper=True, ls=0.16)
    return s


DISC = ["Stratégie", "Architecture de marque", "Naming", "Design", "Éditorial", "Production", "IA"]


def f09():
    s = bg(960, 330)
    rng4 = random.Random(11)
    pos = [(260, 260), (620, 380), (900, 220), (1180, 400), (1440, 250), (1700, 380), (980, 470)]
    for i, (x, y) in enumerate(pos):
        for (x2, y2) in pos[i + 1:i + 3]:
            s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{BURG}" stroke-width="2" opacity=".7"/>'
    for (x, y), lab in zip(pos, DISC):
        s += node(x, y, r=12, fill=CREAM)
        s += t(x, y - 34, lab, 44, fam=SERIF, anchor="middle")
        for k in range(4):
            a = rng4.uniform(0, 6.28)
            s += f'<circle cx="{x + 46 * math.cos(a):.0f}" cy="{y + 46 * math.sin(a):.0f}" r="4" fill="{MUTED}"/>'
    for x, y in pos:
        s += f'<path d="M{x} {y + 14} C {x} 640, 960 600, 960 760" fill="none" stroke="{BURG}" stroke-width="2" opacity=".55"/>'
    s += thread("M0 760 L 1920 760", 6)
    s += t(960, 900, "Pour chaque enjeu, la bonne équipe.", 64, fam=SERIF, anchor="middle")
    s += t(960, 980, "Et elle joue comme une seule.", 40, fill=MUTED, weight=300, anchor="middle")
    return s


def f10():
    s = f'<rect width="1920" height="1080" fill="{INK}"/>'
    s += f'<rect width="1920" height="520" fill="#1b1714"/>'
    rng5 = random.Random(2)
    for _ in range(46):
        x, y = rng5.uniform(140, 1800), rng5.uniform(120, 460)
        a, L = rng5.uniform(0, 6.28), rng5.uniform(30, 90)
        s += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + L * math.cos(a):.0f}" y2="{y + L * math.sin(a):.0f}" stroke="{MUTED}" stroke-width="2" opacity=".55"/>'
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{CREAM}" opacity=".8"/>'
    s += t(120, 100, "Côté Relax", 26, weight=800, upper=True, ls=0.18, fill=CREAM)
    s += t(1800, 100, "beaucoup de mouvement", 30, fam=SERIF, italic=True, anchor="end", fill=MUTED)
    s += t(120, 600, "Côté client", 26, weight=800, upper=True, ls=0.18, fill=CREAM)
    s += t(1800, 600, "un seul fil", 30, fam=SERIF, italic=True, anchor="end", fill=MUTED)
    s += thread("M0 760 L 1920 760", 6)
    s += t(960, 900, "On construit l'équipe autour du projet.", 72, fam=SERIF, anchor="middle")
    s += t(960, 990, "Aucune couture.", 44, fam=SERIF, italic=True, anchor="middle", fill=BURG_LIT)
    return s


def f11():
    s = bg(960, 540)
    words = ["IARD", "Ancré", "Kakemonos", "cohérence", "Naming", "Design", "dirigeants", "Cartes de vœux",
             "LinkedIn", "Architecte", "Agent IA", "Stratégie", "Pédagogue", "marché", "Plaquettes B2B",
             "Éditorial", "Team player", "Cabinet", "Production", "verticales"]
    for i, w in enumerate(words):
        a = i * 0.62
        r = 160 + i * 21
        x, y = 960 + r * math.cos(a), 540 + r * 0.55 * math.sin(a)
        s += t(f"{x:.0f}", f"{y:.0f}", w, 20 + i * 1.3, fam=SERIF if i % 2 else SANS, anchor="middle",
               fill=CREAM if i % 3 else MUTED, opacity=max(0.25, 1 - i * 0.035))
    sp = "M960 540 " + " ".join(
        f"L {960 + (8 + k * 9) * math.cos(k * 0.35):.0f} {540 + (8 + k * 9) * 0.55 * math.sin(k * 0.35):.0f}"
        for k in range(1, 90))
    s += thread(sp, 3, 0.8)
    s += f'<circle cx="960" cy="540" r="16" fill="{CREAM}"/>'
    s += t(960, 930, "Les meilleurs experts pour votre projet.", 70, fam=SERIF, anchor="middle")
    s += t(960, 1010, "Coordonnés par un partenaire de confiance.", 44, fam=SERIF, italic=True, anchor="middle", fill=MUTED)
    return s


def f12():
    s = f'<rect width="1920" height="1080" fill="{CREAM}"/>'
    s += f'<circle cx="960" cy="540" r="900" fill="none" stroke="{INK}" stroke-width="2" opacity=".06"/>'
    s += f'<circle cx="960" cy="540" r="620" fill="none" stroke="{INK}" stroke-width="2" opacity=".08"/>'
    s += t(960, 590, "relax", 180, fam=SERIF, anchor="middle", fill=INK)
    s += t(960, 680, "logo Relax — à récupérer", 22, anchor="middle", fill="#6b625a", weight=600, upper=True, ls=0.18)
    s += f'<line x1="760" y1="760" x2="1160" y2="760" stroke="{BURG}" stroke-width="4"/>'
    return s


FRAMES = [
    ("01", "Chaos hérité", "0:00–0:09", f01, "cut",
     "<b>Ça part vite.</b> Les nœuds dérivent et tremblent, l'ancien logo flotte sans hiérarchie, « + 12 000 » se compte. Pas encore de fil."),
    ("02", "Le vrai sujet", "0:09–0:18", f02, "cut",
     "<b>« logo » se barre</b>, « cohérence » s'écrit en serif ; le fil rouge entre par la bas-gauche et touche le premier nœud, qui cesse de trembler."),
    ("03", "Comprendre", "0:18–0:26", f03, "fil",
     "<b>Le fil court de nœud en nœud</b> ; chaque contact fait naître un mot d'enquête. Le rail des 5 étapes s'installe en haut."),
    ("04", "Révéler", "0:26–0:35", f04, "fil",
     "<b>Les nœuds passent du bleu au crème</b> et se maillent en deux pôles que le fil relie : groupe / cabinet."),
    ("05", "L'intelligence collective", "0:35–0:39.5", f05, "fondu",
     "<b>Plan tenu.</b> Le texte monte par masque (0,8 s), puis plus rien ne bouge. Le réseau reste en fond, éteint."),
    ("06", "Organiser", "0:39.5–0:50", f06, "fil",
     "<b>Les mêmes nœuds qu'au début se rangent</b> en arborescence (callback F01). Certaines marques restent autonomes, en pointillé."),
    ("07", "Exprimer", "0:50–0:58", f07, "fil",
     "<b>Le fil rouge devient la virgule du logo</b> : l'ancien logo se dissout, le nouveau se dessine. Les 4 traits se posent dessous."),
    ("08", "Déployer", "0:58–1:10", f08, "fil",
     "<b>1 → 2 → 4 → 8 → 64</b> : les supports se démultiplient, reliés par le fil. L'agent IA écrit la dernière ligne, dans la voix Finaxy."),
    ("09", "La bonne équipe", "1:10–1:19", f09, "recul",
     "<b>Recul</b> : au-dessus, les disciplines s'allument dans l'ordre de la VO et se relient ; tout converge vers une seule ligne."),
    ("10", "Sans couture", "1:19–1:29.5", f10, "fil",
     "<b>Deux tempos</b> : en haut l'agitation des experts, en bas un seul fil immobile. « Aucune couture. » se pose en bordeaux."),
    ("11", "Tourbillon", "1:29.5–1:35.5", f11, "fil",
     "<b>Tout le film tourbillonne</b> — mots, supports, disciplines — et s'agrège vers un point qui ralentit."),
    ("12", "Respiration → Relax", "1:35.5–1:42.5", f12, "souffle",
     "<b>Inspiration</b> : le point se dilate, tout se suspend. <b>Expiration</b> relâchée : le cadre s'ouvre en crème, le logo Relax se pose."),
]


def cell(num, name, span, fn, seam, note):
    svg = f'<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">{DEFS}{fn()}</svg>'
    return f'''<article class="cell" id="frame-{num}">
  <div class="canvas">{svg}</div>
  <div class="label"><span>{num} · {name.upper()}</span><span>{span}</span></div>
  <p class="note">{note}</p>
  <span class="chip">→ {seam}</span>
</article>'''


acts = [("Avant — la complexité héritée", FRAMES[0:2]),
        ("La chaîne de décisions — Comprendre → Révéler → Organiser → Exprimer → Déployer", FRAMES[2:8]),
        ("La méthode Relax — et le soulagement", FRAMES[8:12])]

cells = ""
for act, frs in acts:
    cells += f'<div class="act">{act}</div>'
    cells += "".join(cell(*f) for f in frs)

seams = " ".join(f'<span><b>{f[0]}</b> {f[4]}</span>' for f in FRAMES)

html = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storyboard — Relax × Finaxy ({VERSION})</title>
<style>
{(PROJECT / "assets/fonts/fonts.css").read_text()}
:root{{--ink:{INK};--cream:{CREAM};--burg:{BURG};--muted:{MUTED}}}
*{{box-sizing:border-box;margin:0}}
body{{background:#0d0b0a;color:var(--cream);font-family:Manrope,Helvetica,Arial,sans-serif;padding:48px 40px 80px}}
header{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-bottom:1px solid #3a332d;padding-bottom:24px;margin-bottom:8px;flex-wrap:wrap}}
h1{{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:56px;line-height:1}}
h1 em{{color:#C2185B}}
.dek{{color:var(--muted);font-size:16px;max-width:760px;margin-top:10px;line-height:1.5}}
.tag{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;border:1px solid #3a332d;padding:8px 12px;border-radius:99px;white-space:nowrap}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 22px}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr}}}}
.act{{grid-column:1/-1;margin-top:28px;padding:10px 0;border-top:2px solid var(--burg);font-size:12px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}}
.cell{{position:relative}}
.canvas{{aspect-ratio:16/9;container-type:inline-size;border-radius:6px;overflow:hidden;outline:1px solid #2a2420}}
.canvas > svg{{display:block;width:100%;height:100%}}
.label{{display:flex;justify-content:space-between;font-size:12px;font-weight:800;letter-spacing:.14em;margin-top:12px}}
.label span:last-child{{color:var(--muted);font-weight:600}}
.note{{font-size:14px;line-height:1.5;color:#d8d2c8;margin-top:6px;padding-right:86px}}
.note b{{color:var(--cream)}}
.chip{{position:absolute;right:0;bottom:2px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--burg);color:#e9a3bd;padding:4px 9px;border-radius:99px}}
.vo{{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:15px;color:var(--muted);margin-top:6px}}
.info{{background:#171311;border-radius:6px;padding:26px;outline:1px solid #2a2420;font-size:14px;line-height:1.6}}
.info h3{{font-size:12px;letter-spacing:.18em;text-transform:uppercase;margin-bottom:12px;color:var(--muted)}}
.seams{{display:flex;flex-wrap:wrap;gap:8px}}
.seams span{{border:1px solid #3a332d;border-radius:99px;padding:4px 10px;font-size:12px}}
.sw{{display:inline-flex;align-items:center;gap:8px;margin:0 14px 8px 0;font-size:12px}}
.sw i{{width:22px;height:22px;border-radius:4px;display:inline-block;outline:1px solid #3a332d}}
</style></head><body>
<header>
  <div><h1>Relax × Finaxy — <em>le fil rouge</em> <span style="font-size:24px;color:var(--muted)">{VERSION}</span></h1>
  <p class="dek">Case agence : Relax réunit et coordonne, sans couture, les meilleurs experts autour du projet — le client, lui, ne voit qu'un seul fil. Une ligne bordeaux traverse tout le film ; chaque contact aligne l'élément suivant.</p></div>
  <span class="tag">1920×1080 · ~100 s · 12 scènes · VO Algieba</span>
</header>
<div class="grid">
{cells}
<div class="act">Repères</div>
<article class="cell info"><h3>Carte des transitions</h3><div class="seams">{seams}</div>
<p style="margin-top:14px;color:var(--muted)">Règle de direction unique : le fil avance vers la droite, le monde glisse vers la gauche. Le fil n'est jamais coupé, sauf en 01→02 (il naît) et 11→12 (il devient souffle).</p></article>
<article class="cell info"><h3>Tokens</h3>
<span class="sw"><i style="background:{INK}"></i>Encre #14110F</span><span class="sw"><i style="background:{CREAM}"></i>Crème #F4F1EB</span>
<span class="sw"><i style="background:{BURG}"></i>Bordeaux #9C0A3F</span><span class="sw"><i style="background:{BEFORE}"></i>Avant #5E7891</span>
<span class="sw"><i style="background:{MUTED}"></i>Secondaire #B9B2A6</span>
<p style="margin-top:10px"><span style="font-family:'Instrument Serif';font-size:30px">Instrument Serif</span> — titres, citations<br>
<span style="font-weight:600">Manrope</span> — textes, libellés en capitales espacées</p></article>
<article class="cell info"><h3>Interdits</h3>
<p>Pas d'effet catalogue · pas d'anglais à l'écran (sauf « naming », « Team player ») · pas de faux site ni de fausse interface : placeholders étiquetés jusqu'aux visuels réels · pas de glow sur le texte · ni diaporama, ni écran de veille.</p></article>
</div></body></html>'''

(PROJECT / "storyboard.html").write_text(html)
print("wrote", PROJECT / "storyboard.html", len(html))
