"""storyboard.html v4 — modern direction (isometric 3D, iridescent glass, colour blocks, HUD chrome).

Each cell is an inline SVG on the real 1920x1080 canvas. Deterministic.
Usage: python3 tools/storyboard_v4_gen.py <project_dir> <version>
"""
import json
import math
import random
import sys
from pathlib import Path

PROJECT = Path(sys.argv[1])
VERSION = sys.argv[2] if len(sys.argv) > 2 else "v4"

WHITE, OFF, INK, INK2, LAV, PURPLE, PINK, NIGHT = "#FFFFFF", "#F6F5F9", "#212C34", "#6B7278", "#D4CCEE", "#6955AA", "#FF0055", "#16131F"
CYAN, YEL, RED, GREY = "#56A0AA", "#ABA256", "#AA5655", "#A7AEB4"
NAVY, FBLUE, SLATE, CREAM, BURG, OLDBLUE = "#191853", "#5A80D9", "#4A5892", "#F4F1EB", "#9C0A3F", "#174A8C"
TITLE, TEXT, SERIF, MONO = "Unbounded, sans-serif", "'DM Sans', sans-serif", "'Instrument Serif', serif", "'JetBrains Mono', 'IBM Plex Mono', monospace"

new_logo = (PROJECT / "assets/brand/finaxy-new.svg").read_text()
old_logo = (PROJECT / "assets/brand/finaxy-old.svg").read_text().replace('fill="white"', f'fill="{OLDBLUE}"')
relax_logo = (PROJECT / "assets/brand/relax-logo.svg").read_text()
cues = json.loads((PROJECT / "tools/vo-cues.json").read_text())


def logo(svg, x, y, w, opacity=1.0, recolor=None):
    head, rest = svg.split(">", 1)
    inner = rest.rsplit("</svg>", 1)[0]
    if recolor:
        for a, b in recolor:
            inner = inner.replace(a, b)
    vb = head.split('viewBox="')[1].split('"')[0].split()
    h = w * float(vb[3]) / float(vb[2])
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{" ".join(vb)}" opacity="{opacity}">{inner}</svg>'


def t(x, y, s, size, fam=TEXT, fill=INK, weight=400, anchor="start", italic=False, ls=0, opacity=1, upper=False, extra=""):
    st = f"font-family:{fam};font-size:{size}px;font-weight:{weight};letter-spacing:{ls}em" + (";font-style:italic" if italic else "")
    return f'<text x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}" opacity="{opacity}" style="{st}" {extra}>{s.upper() if upper else s}</text>'


def hud(scene, label, dark=False):
    c = "#FFFFFF" if dark else INK
    o = 0.55
    s = ""
    for (x, y, dx, dy) in ((60, 60, 1, 1), (1860, 60, -1, 1), (60, 1020, 1, -1), (1860, 1020, -1, -1)):
        s += f'<path d="M {x} {y + 40 * dy} L {x} {y} L {x + 40 * dx} {y}" fill="none" stroke="{c}" stroke-width="3" opacity="{o}"/>'
    s += t(120, 92, "RELAX × FINAXY", 20, fam=MONO, fill=c, weight=700, ls=0.12, opacity=o)
    s += t(1800, 92, f"{scene} — {label}", 20, fam=MONO, fill=c, ls=0.12, opacity=o, anchor="end", upper=True)
    return s


def iso(x, y, z, cx=960, cy=560, s=1.0):
    return cx + (x - y) * 0.866 * s, cy + (x + y) * 0.5 * s - z * s


def box(x, y, w, d, h, col, cx=960, cy=560, s=1.0, top=None, right=None, stroke=None):
    P = lambda a, b, c: iso(a, b, c, cx, cy, s)
    def poly(pts, f):
        return f'<polygon points="{" ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)}" fill="{f}"' + (f' stroke="{stroke}" stroke-width="2"' if stroke else "") + "/>"
    tp = [P(x, y, h), P(x + w, y, h), P(x + w, y + d, h), P(x, y + d, h)]
    lf = [P(x, y + d, 0), P(x, y + d, h), P(x + w, y + d, h), P(x + w, y + d, 0)]
    rt = [P(x + w, y, 0), P(x + w, y, h), P(x + w, y + d, h), P(x + w, y + d, 0)]
    return poly(lf, col) + poly(rt, right or shade(col, 0.78)) + poly(tp, top or shade(col, 1.22))


def shade(hexc, k):
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda v: max(0, min(255, int(v * k if k < 1 else v + (255 - v) * (k - 1))))
    return f"#{f(r):02x}{f(g):02x}{f(b):02x}"


def glass(x, y, w, h, rx=26, label=None, lsize=26, inner=""):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#glass)" stroke="#FFFFFF" stroke-width="2" opacity=".96"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h * 0.45}" rx="{rx}" fill="#FFFFFF" opacity=".28"/>' + inner)
    if label:
        s += t(x + w / 2, y + h / 2 + lsize * 0.35, label, lsize, fam=TITLE, weight=500, anchor="middle", fill=INK)
    return s


def ribbon(d, w=46, op=1):
    return (f'<path d="{d}" fill="none" stroke="url(#irid)" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{w * 0.18}" stroke-linecap="round" opacity=".55" transform="translate(0,-{w * 0.18})"/>')


DEFS = (f'<defs>'
        f'<linearGradient id="irid" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#7FE3F0"/><stop offset=".35" stop-color="#B9A8F0"/><stop offset=".7" stop-color="#E9A6E0"/><stop offset="1" stop-color="#8FD9F5"/></linearGradient>'
        f'<linearGradient id="glass" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#E9FBFF"/><stop offset=".5" stop-color="#E6DEFF"/><stop offset="1" stop-color="#FBE3F4"/></linearGradient>'
        f'<radialGradient id="wash"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".22"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="floor" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/></linearGradient>'
        f'</defs>')


def bgw(extra=""):
    return f'<rect width="1920" height="1080" fill="{WHITE}"/><ellipse cx="960" cy="560" rx="900" ry="520" fill="url(#wash)"/>' + extra


rng = random.Random(4)


# ── Act A ───────────────────────────────────────────────────────────────
def c01():
    s = f'<rect width="1920" height="1080" fill="{PURPLE}"/>' + hud("01", "le constat", dark=True)
    s += t(120, 640, "11", 520, fam=TITLE, weight=600, fill=WHITE, ls=-0.04)
    s += t(820, 360, "e", 150, fam=TITLE, weight=600, fill=WHITE)
    s += t(820, 560, "courtier", 92, fam=TITLE, weight=500, fill=WHITE)
    s += t(820, 660, "français", 92, fam=TITLE, weight=500, fill=WHITE)
    s += f'<circle cx="1640" cy="300" r="36" fill="{PINK}"/>'
    s += t(120, 960, "FINAXY — CONSEIL ET COURTAGE EN ASSURANCES", 22, fam=MONO, fill=WHITE, ls=0.14, opacity=.75)
    return s


def c02():
    s = bgw() + hud("02", "un groupe qui a grandi vite")
    r = random.Random(9)
    labels = ["Cabinet", "Entreprise", "Marque", "Cabinet", "Marque", "Entreprise", "Cabinet", "Marque", "Entreprise"]
    cells = [(i % 6, i // 6) for i in range(30)]
    r.shuffle(cells)
    for k, (gx, gy) in enumerate(cells[:22]):
        h = 40 + r.random() * 180
        col = r.choice([GREY, "#C9CED3", OLDBLUE, "#8E9AA8", LAV, "#B8C2CC"])
        s += box(gx * 120 - 330 + r.random() * 30, gy * 120 - 240 + r.random() * 30, 80 + r.random() * 30, 80, h, col, cy=620)
    for i, (x, y, lab) in enumerate([(380, 300, "Cabinets"), (1500, 260, "Entreprises"), (1560, 760, "Marques"), (300, 820, "Acquisitions")]):
        s += glass(x - 150, y - 44, 300, 88, rx=44, label=lab, lsize=30)
    s += t(960, 1010, "+ acquisition  + acquisition  + acquisition", 24, fam=MONO, fill=INK2, anchor="middle", ls=0.08)
    return s


def c03():
    s = bgw() + hud("03", "une marque qui ne racontait plus")
    for k in range(5):
        s += logo(old_logo, 560 + k * 26, 380 + k * 18, 760, opacity=0.18 + k * 0.08)
    s += f'<rect x="520" y="560" width="900" height="16" fill="{WHITE}"/><rect x="520" y="430" width="900" height="10" fill="{WHITE}"/>'
    s += t(960, 820, "ne reflétait plus ce que l'entreprise était devenue", 40, anchor="middle", fill=INK2, weight=300)
    s += t(960, 880, "glitch · décalage · flou : le nom se désynchronise", 22, fam=MONO, anchor="middle", fill=GREY, ls=0.08)
    return s


def c04():
    s = f'<rect width="1920" height="1080" fill="{NIGHT}"/>' + hud("04", "un sujet de cohérence", dark=True)
    for k in range(-2, 3):
        s += t(960, 560 + k * 170, "COHÉRENCE", 190, fam=TITLE, weight=600, anchor="middle", fill="none",
               extra=f'stroke="{LAV}" stroke-width="2" opacity="{0.25 if k else 1}"')
    s += t(960, 590, "COHÉRENCE", 190, fam=TITLE, weight=600, anchor="middle", fill=WHITE)
    s += f'<rect x="560" y="930" width="800" height="70" fill="{NIGHT}"/>'
    s += t(880, 985, "pas juste un problème de", 38, fill="#B9B2C9", weight=300, anchor="end")
    s += t(900, 985, "logo", 38, fill="#B9B2C9", weight=600)
    s += f'<line x1="894" y1="972" x2="990" y2="972" stroke="{PINK}" stroke-width="5"/>'
    return s


# ── Act B ───────────────────────────────────────────────────────────────
def c05():
    s = bgw() + hud("05", "on a commencé par écouter")
    s += ribbon("M -40 640 C 300 520, 520 760, 800 600 S 1300 480, 1960 620", 52)
    for i, lab in enumerate(["dirigeants", "collaborateurs", "métiers", "marché"]):
        x = 180 + i * 420
        s += glass(x, 300 - (i % 2) * 40, 340, 420, inner=t(x + 170, 300 - (i % 2) * 40 + 380, lab, 34, fam=TITLE, weight=500, anchor="middle"))
        s += f'<circle cx="{x + 170}" cy="{420 - (i % 2) * 40}" r="56" fill="{WHITE}" stroke="{LAV}" stroke-width="3"/>'
        for k in range(3):
            s += f'<rect x="{x + 140 + k * 22}" y="{405 - (i % 2) * 40 - k * 8}" width="10" height="{30 + k * 16}" rx="5" fill="{PURPLE}"/>'
    s += t(960, 960, "{ écouter }", 30, fam=MONO, anchor="middle", fill=INK2, ls=0.1)
    return s


def c06():
    s = bgw() + hud("06", "ce que Finaxy était vraiment")
    s += glass(160, 300, 520, 300, label="La force d'un groupe", lsize=34)
    s += glass(1240, 300, 520, 300, label="L'esprit d'un cabinet", lsize=34)
    s += f'<path d="M 690 450 C 820 450, 820 520, 960 520 C 1100 520, 1100 450, 1230 450" fill="none" stroke="{PINK}" stroke-width="5"/>'
    s += f'<rect x="520" y="560" width="880" height="380" rx="28" fill="{NAVY}"/>'
    s += t(960, 720, "Une intelligence collective", 72, fam=SERIF, fill=CREAM, anchor="middle")
    s += t(960, 810, "du risque.", 72, fam=SERIF, fill=CREAM, anchor="middle", italic=True)
    s += f'<rect x="900" y="850" width="120" height="6" rx="3" fill="{BURG}"/>'
    s += t(960, 1000, "plateforme de marque Finaxy", 20, fam=MONO, anchor="middle", fill=INK2, ls=0.12, upper=True)
    return s


def c07():
    s = f'<rect width="1920" height="1080" fill="{OFF}"/>' + hud("07", "proposition de valeur")
    r = random.Random(3)
    for i in range(16):
        a, rad = i / 16 * 6.283, 250 + r.random() * 120
        x, y = 560 + math.cos(a) * rad, 520 + math.sin(a) * rad * 0.8
        s += f'<polygon points="{x},{y - 22} {x + 20},{y + 14} {x - 20},{y + 14}" fill="{RED if i % 3 else YEL}" opacity=".9"/>'
    s += f'<circle cx="560" cy="520" r="22" fill="{GREY}"/>' + t(560, 590, "une expertise isolée", 26, anchor="middle", fill=INK2)
    s += f'<line x1="960" y1="250" x2="960" y2="830" stroke="{LAV}" stroke-width="3"/>'
    pts = [(1360 + math.cos(i / 7 * 6.283) * 170, 520 + math.sin(i / 7 * 6.283) * 150) for i in range(7)]
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            s += f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="{PURPLE}" stroke-width="2" opacity=".5"/>'
        s += f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="18" fill="{PURPLE}"/>'
    s += f'<circle cx="1360" cy="520" r="26" fill="{PINK}"/>'
    s += t(960, 960, "Le risque est devenu multiple.", 54, fam=TITLE, weight=500, anchor="middle")
    s += t(960, 1020, "aucune expertise isolée ne suffit", 28, anchor="middle", fill=INK2, weight=300)
    return s


# ── Act C ───────────────────────────────────────────────────────────────
def c08():
    s = bgw() + hud("08", "rendre le groupe lisible")
    cols = [NAVY, FBLUE, SLATE]
    for k in range(3):
        for j in range(4):
            s += box(-260 + k * 200, -120, 140, 140, 70 + j * 70 - (j * 70 - 0), cols[k], cy=700, s=1.0) if j == 0 else ""
        s += box(-260 + k * 200, -120, 140, 140, 300 - k * 40, cols[k], cy=700)
    for k, lab in enumerate(["Entreprises & institutions", "Affinitaire & partenariats", "Clientèle privée"]):
        x, y = iso(-190 + k * 200, -50, 330 - k * 40, cy=700)
        s += t(x, y - 30, lab, 28, fam=SERIF, anchor="middle", fill=NAVY)
    # the domino chain: each act ends by tipping the next piece
    for i in range(5):
        ang = 0 if i > 1 else (55 if i == 0 else 25)
        x0, y0 = 1260 + i * 110, 800
        s += f'<g transform="rotate({ang} {x0} {y0})"><rect x="{x0 - 22}" y="{y0 - 170}" width="44" height="170" rx="6" fill="{PURPLE if i else PINK}"/><rect x="{x0 - 22}" y="{y0 - 170}" width="14" height="170" rx="6" fill="#FFFFFF" opacity=".25"/></g>'
    s += t(1480, 860, "effet domino → acte suivant", 22, fam=MONO, fill=INK2, anchor="middle", ls=0.06)
    s += t(1500, 330, "architecture", 30, fam=MONO, fill=INK2, ls=0.08) + t(1500, 380, "catégories", 30, fam=MONO, fill=INK2, ls=0.08)
    s += t(1500, 430, "naming", 30, fam=MONO, fill=INK2, ls=0.08) + t(1500, 480, "place des marques", 30, fam=MONO, fill=INK2, ls=0.08)
    s += t(960, 990, "Une idée : rendre le groupe lisible.", 56, fam=TITLE, weight=500, anchor="middle")
    return s


def c09():
    s = bgw() + hud("09", "lui donner du corps")
    s += f'<rect x="560" y="250" width="800" height="400" rx="30" fill="{NAVY}"/>'
    s += logo(new_logo, 640, 350, 640)
    for i, (col, lab) in enumerate([(NAVY, "#191853"), (FBLUE, "#5A80D9"), (CREAM, "#F4F1EB"), (BURG, "#9C0A3F")]):
        x = 380 + i * 300
        s += f'<rect x="{x}" y="720" width="240" height="150" rx="16" fill="{col}" stroke="#E6E1D8" stroke-width="2"/>'
        s += t(x + 20, 850, lab, 20, fam=MONO, fill=WHITE if col not in (CREAM,) else NAVY)
    s += t(160, 320, "logo", 34, fam=MONO, fill=INK2) + t(160, 380, "identité", 34, fam=MONO, fill=INK2) + t(160, 440, "voix", 34, fam=MONO, fill=INK2)
    s += t(1500, 330, "Ancré", 46, fam=SERIF, italic=True, fill=NAVY) + t(1500, 400, "Architecte", 46, fam=SERIF, italic=True, fill=NAVY)
    s += t(1500, 470, "Team player", 46, fam=SERIF, italic=True, fill=NAVY) + t(1500, 540, "Pédagogue", 46, fam=SERIF, italic=True, fill=NAVY)
    s += t(960, 990, "relief · lumière balayée · cartes d'identité qui se déploient en éventail", 22, fam=MONO, anchor="middle", fill=GREY, ls=0.06)
    return s


def c10():
    s = f'<rect width="1920" height="1080" fill="{PINK}"/>' + hud("10", "notre ambition", dark=True)
    s += t(120, 460, "STATURE", 300, fam=TITLE, weight=600, fill=WHITE, ls=-0.03)
    s += t(1800, 860, "humain", 300, fam=TITLE, weight=500, fill=NIGHT, anchor="end", ls=-0.03)
    s += t(120, 560, "valoriser la", 40, fill=WHITE, weight=300) + t(1800, 940, "mettre en avant l'", 40, fill=NIGHT, weight=300, anchor="end")
    return s


# ── Act D ───────────────────────────────────────────────────────────────
def c11():
    s = bgw() + hud("11", "les supports")
    s += ribbon("M -40 520 C 260 380, 380 700, 640 540 S 1100 380, 1300 560 S 1700 700, 1960 500", 70, .9)
    cards = [(120, 300, 300, 420, NAVY, "Plaquettes"), (470, 260, 200, 520, CREAM, "Kakemonos"), (720, 380, 260, 160, NAVY, "Cartes de visite"),
             (1030, 300, 330, 340, FBLUE, "Réseaux sociaux")]
    for x, y, w, h, col, lab in cards:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{col}" stroke="#E6E1D8" stroke-width="2"/>'
        s += logo(new_logo if col != CREAM else new_logo, x + w * 0.2, y + h * 0.42, w * 0.6, recolor=[('fill="#F4F1EB"', f'fill="{NAVY}"')] if col == CREAM else None)
        s += t(x + w / 2, y + h + 40, lab, 24, anchor="middle", fill=INK2, weight=500)
        s += f'<rect x="{x}" y="{y + h + 54}" width="{w}" height="{h * 0.35}" rx="14" fill="{col}" opacity=".12"/>'
    s += f'<rect x="1420" y="250" width="420" height="560" rx="18" fill="#FFFFFF" stroke="#DCD8E6" stroke-width="2"/>'
    s += f'<image href="assets/captures/finaxy-site-cartes.jpg" x="1430" y="320" width="400" height="171"/>'
    s += f'<rect x="1430" y="262" width="400" height="44" rx="10" fill="{NAVY}"/>' + t(1630, 292, "finaxy.com", 22, fam=MONO, fill=WHITE, anchor="middle")
    s += t(1630, 860, "le nouveau site", 26, anchor="middle", fill=INK, weight=600)
    s += t(960, 1000, "{ carrousel — plis de verre irisé entre chaque support }", 22, fam=MONO, anchor="middle", fill=GREY, ls=0.06)
    return s


def c12():
    s = f'<rect width="1920" height="1080" fill="{OFF}"/>' + hud("12", "la cerise sur le gâteau")
    s += glass(360, 200, 1200, 640, rx=36)
    s += t(420, 280, "Agent éditorial IA · Finaxy", 28, fam=TITLE, weight=500, fill=PURPLE)
    s += f'<rect x="420" y="330" width="760" height="90" rx="45" fill="#FFFFFF"/>' + t(460, 386, "Écris un post LinkedIn sur la cyber pour les PME", 26, fill=INK2)
    s += f'<rect x="700" y="460" width="800" height="250" rx="30" fill="{NAVY}"/>'
    s += t(740, 530, "« Un dirigeant de PME n'a pas le temps", 30, fam=SERIF, fill=CREAM)
    s += t(740, 580, "de devenir expert du risque.", 30, fam=SERIF, fill=CREAM)
    s += t(740, 630, "C'est exactement pour ça qu'on est là. »", 30, fam=SERIF, fill=CREAM, italic=True)
    s += f'<circle cx="1520" cy="230" r="44" fill="{PINK}"/><path d="M 1520 186 C 1530 150, 1560 140, 1580 130" stroke="#3E7C3E" stroke-width="6" fill="none"/>'
    s += t(960, 960, "pour que chacun puisse écrire comme Finaxy", 34, anchor="middle", fill=INK2, weight=300)
    return s


# ── Act E ───────────────────────────────────────────────────────────────
DISC = [("Stratégie", PURPLE), ("Naming", RED), ("Design", PURPLE), ("Édito", YEL), ("Développement", CYAN), ("Production", RED)]


def pill(cx, cy, lab, col, size=30):
    w = len(lab) * size * 0.6 + 60
    return (f'<rect x="{cx - w / 2:.0f}" y="{cy - size:.0f}" width="{w:.0f}" height="{size * 2}" rx="{size}" fill="{col}"/>'
            + t(cx, cy + size * 0.36, lab, size, anchor="middle", fill=WHITE if col != YEL else "#2B2A14", weight=500))


def c13():
    s = f'<rect width="1920" height="1080" fill="{NIGHT}"/>' + hud("13", "notre rôle", dark=True)
    for i, (lab, col) in enumerate(DISC):
        a = i / 6 * 6.283 - 1.57
        s += f'<line x1="960" y1="500" x2="{960 + math.cos(a) * 330:.0f}" y2="{500 + math.sin(a) * 260:.0f}" stroke="{LAV}" stroke-width="2" opacity=".5"/>'
        s += pill(960 + math.cos(a) * 330, 500 + math.sin(a) * 260, lab, col)
    s += f'<circle cx="960" cy="500" r="70" fill="{PINK}"/>' + t(960, 512, "projet", 30, fam=TITLE, weight=500, anchor="middle", fill=WHITE)
    s += t(960, 930, "Les bons talents, à chaque étape.", 58, fam=TITLE, weight=500, anchor="middle", fill=WHITE)
    s += t(960, 1000, "comme une seule équipe", 30, anchor="middle", fill="#B9B2C9", weight=300)
    return s


def c14():
    s = bgw() + hud("14", "l'équipe autour du projet")
    # rejected: the rigid agency cube (wireframe)
    P = lambda a, b, c: iso(a, b, c, 520, 640)
    pts = [P(x, y, z) for x in (0, 220) for y in (0, 220) for z in (0, 220)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 7), (6, 7), (0, 4), (1, 5), (2, 6), (3, 7)]
    for a, b in edges:
        s += f'<line x1="{pts[a][0]:.0f}" y1="{pts[a][1]:.0f}" x2="{pts[b][0]:.0f}" y2="{pts[b][1]:.0f}" stroke="{INK}" stroke-width="3" stroke-dasharray="10 8"/>'
    s += t(520, 340, "une agence", 28, fam=MONO, anchor="middle", fill=INK2, ls=0.08)
    s += f'<circle cx="800" cy="520" r="54" fill="{LAV}"/><path d="M 760 470 L 720 430" stroke="{PINK}" stroke-width="5"/>'
    s += f'<line x1="900" y1="250" x2="900" y2="860" stroke="{LAV}" stroke-width="3"/>'
    # built around: experts locked around the project
    s += box(-60, -60, 120, 120, 120, LAV, cx=1380, cy=600, top="#EFEAFF")
    s += t(1380, 470, "votre projet", 28, fam=TITLE, weight=500, anchor="middle")
    for i, (lab, col) in enumerate(DISC):
        a = i / 6 * 6.283
        x, y = 1380 + math.cos(a) * 330, 600 + math.sin(a) * 190
        s += box(-30, -30, 60, 60, 60, col, cx=x, cy=y + 40, s=0.9)
        s += t(x, y + 110, lab, 22, anchor="middle", fill=INK, weight=500)
    s += t(960, 1010, "On construit l'équipe autour de votre projet.", 50, fam=TITLE, weight=500, anchor="middle")
    return s


def c15():
    s = f'<rect width="1920" height="1080" fill="{WHITE}"/>' + f'<rect width="1920" height="540" fill="{PURPLE}"/>' + hud("15", "notre promesse")
    r = random.Random(8)
    for i in range(60):
        x, y, a, L = 100 + r.random() * 1720, 140 + r.random() * 360, r.random() * 6.28, 30 + r.random() * 70
        col = [LAV, "#FFFFFF", PINK, "#7FE3F0"][i % 4]
        s += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + math.cos(a) * L:.0f}" y2="{y + math.sin(a) * L:.0f}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>'
    s += t(120, 200, "Côté Relax", 64, fam=TITLE, weight=600, fill=WHITE) + t(1800, 480, "du mouvement.", 44, anchor="end", fill=WHITE, weight=300)
    s += t(120, 650, "Côté client", 64, fam=TITLE, weight=600, fill=INK) + t(1800, 650, "un seul fil, zéro couture.", 44, anchor="end", fill=INK2, weight=300)
    s += ribbon("M -40 820 L 1960 820", 30)
    s += t(960, 990, "C'est ça, notre promesse.", 46, fam=TITLE, weight=500, anchor="middle", fill=PURPLE)
    return s


def c16():
    s = bgw() + hud("16", "respiration")
    for r_, o in ((780, .06), (520, .09), (300, .13)):
        s += f'<circle cx="960" cy="520" r="{r_}" fill="none" stroke="{PURPLE}" stroke-width="2" opacity="{o}"/>'
    s += logo(relax_logo, 610, 400, 700)
    s += t(960, 760, "Relax, on s'occupe de tout.", 46, anchor="middle", fill=INK, weight=400)
    return s


ACTS = [
    ("A — Le constat", [("01", "11ᵉ courtier", c01, "cut", "<b>Aplat violet, typo géante.</b> « 11 » claque plein cadre, l'habillage interface s'allume ; le point rose apparaît."),
                        ("02", "A grandi vite", c02, "cut", "<b>Ville isométrique qui pousse.</b> Des blocs jaillissent en rafale (acquisitions) ; pastilles de verre « Cabinets · Entreprises · Marques »."),
                        ("03", "Ne racontait plus", c03, "glitch", "<b>L'ancien logo se dédouble</b> et se désynchronise (glitch, flou) : la marque ne suit plus."),
                        ("04", "Cohérence", c04, "cut", "<b>Coupe au noir.</b> « logo » barré ; « COHÉRENCE » en contours répétés, puis plein.")]),
    ("B — Écouter, comprendre", [("05", "Écouter", c05, "ruban", "<b>Le ruban irisé entre</b> et traverse 4 cartes de verre : dirigeants, collaborateurs, métiers, marché."),
                                 ("06", "Intelligence collective", c06, "fusion", "<b>Deux cartes fusionnent</b> (groupe + cabinet) et donnent le panneau Finaxy de la plateforme."),
                                 ("07", "Proposition de valeur", c07, "morph", "<b>Les risques se multiplient</b> autour d'un point isolé ; à droite, le réseau d'experts tient.")]),
    ("C — Organiser, exprimer", [("08", "Rendre lisible", c08, "iso", "<b>La ville du début se range</b> en 3 tours isométriques — les vraies verticales ; marques autonomes à côté."),
                                 ("09", "Du corps", c09, "relief", "<b>Logo en relief + balayage de lumière</b> ; les couleurs et les 4 traits se déploient en éventail."),
                                 ("10", "Stature · humain", c10, "cut", "<b>Aplat rose.</b> « STATURE » / « humain » : deux mots, deux coupes.")]),
    ("D — Déployer", [("11", "Les supports", c11, "carrousel", "<b>Carrousel façon Jerry</b> : plis de verre irisé entre plaquettes, kakemonos, cartes, réseaux sociaux, puis le vrai site."),
                      ("12", "Agent IA", c12, "zoom", "<b>La cerise (le point rose) tombe</b> sur l'interface : l'agent écrit une ligne dans la voix Finaxy.")]),
    ("E — Le rôle de Relax", [("13", "Notre rôle", c13, "cut", "<b>Coupe au noir.</b> Les talents se verrouillent autour du projet, comme une seule équipe."),
                              ("14", "Autour du projet", c14, "iso", "<b>La séquence que tu aimes, en 3D</b> : le cube « agence » rejette le projet ; les experts se placent autour."),
                              ("15", "La promesse", c15, "split", "<b>Écran partagé</b> : du mouvement en haut ; un seul fil, zéro couture en bas.")]),
    ("Final", [("16", "Respiration", c16, "souffle", "<b>Une respiration calme</b> ; les ondes s'ouvrent, relax• se pose. « Relax, on s'occupe de tout. »")]),
]


def cell(num, name, fn, seam, note):
    svg = f'<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">{DEFS}{fn()}</svg>'
    return f'<article class="cell" id="frame-{num}"><div class="canvas">{svg}</div><div class="label"><span>{num} · {name}</span></div><p class="note">{note}</p><span class="chip">→ {seam}</span></article>'


cells = "".join(f'<div class="act">{a}</div>' + "".join(cell(*f) for f in frs) for a, frs in ACTS)
fonts = (PROJECT / "assets/fonts/fonts.css").read_text()
html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storyboard — Relax × Finaxy ({VERSION})</title><style>{fonts}
*{{box-sizing:border-box;margin:0}}body{{background:#EFEDF5;color:{INK};font-family:'DM Sans',sans-serif;padding:48px 40px 80px}}
header{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-bottom:1px solid #DCDAE3;padding-bottom:24px;flex-wrap:wrap}}
h1{{font-family:Unbounded,sans-serif;font-weight:500;font-size:44px}}h1 .d{{color:{PINK}}}
.dek{{color:{INK2};font-size:16px;max-width:820px;margin-top:12px;line-height:1.55}}
.tag{{font-size:13px;font-weight:500;background:{INK};color:#fff;padding:10px 16px;border-radius:99px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 22px}}@media (max-width:1100px){{.grid{{grid-template-columns:1fr}}}}
.act{{grid-column:1/-1;margin-top:30px;padding-top:12px;border-top:2px solid {LAV};font-family:Unbounded,sans-serif;font-size:13px;font-weight:500;color:{PURPLE}}}
.cell{{position:relative}}.canvas{{aspect-ratio:16/9;border-radius:14px;overflow:hidden;box-shadow:0 2px 14px rgba(31,20,67,.1)}}.canvas>svg{{display:block;width:100%;height:100%}}
.label{{font-family:Unbounded,sans-serif;font-size:12px;font-weight:500;margin-top:12px}}
.note{{font-size:14px;line-height:1.5;color:#3d474f;margin-top:6px;padding-right:96px}}.note b{{color:{INK}}}
.chip{{position:absolute;right:0;bottom:2px;font-size:11px;font-weight:600;background:{LAV};color:#2a2244;padding:4px 10px;border-radius:99px}}
.info{{background:#fff;border-radius:14px;padding:22px;font-size:14px;line-height:1.6}}.info h3{{font-family:Unbounded,sans-serif;font-size:13px;font-weight:500;margin-bottom:10px;color:{PURPLE}}}
</style></head><body>
<header><div><h1>Relax × Finaxy — l'effet domino<span class="d">.</span> <span style="font-size:20px;color:{INK2}">{VERSION}</span></h1>
<p class="dek">Direction v2 : constat rapide, chaîne de décisions, puis la force de Relax. Le film parle en Relax (blanc, verre irisé, aplats violet/rose, typo géante, habillage interface) ; Finaxy n'illustre que les moments clés : plateforme, architecture, logo, site, supports, agent IA. Texte : ton script, voix Sulafat.</p></div>
<span class="tag">1920×1080 · ~100 s · 16 plans · VO Sulafat</span></header>
<div class="grid">{cells}
<div class="act">Repères</div>
<article class="cell info"><h3>Langage visuel</h3><p>Références : carrousel à plis de verre irisé (Jerry) · aplats plein cadre coupés au rythme, typo géante, contours répétés, formes qui se transforment, habillage interface en mono (Stephan) · 3D isométrique pour la ville, l'architecture et l'équipe.</p></article>
<article class="cell info"><h3>Rythme</h3><p><b>L'effet domino relie les actes</b> : chaque acte se termine en faisant basculer une pièce isométrique qui lance le suivant (Comprendre → Révéler → Organiser → Exprimer → Déployer → Relax). Coupes franches sur les temps forts de la voix (A, C, E), mouvements fluides portés par le ruban (B, D). Musique recomposée plus rythmée, retrait avant la respiration.</p></article>
<article class="cell info"><h3>Interdits</h3><p>Pas d'effet catalogue · pas d'anglais à l'écran (sauf naming, Team player) · pas de fausse interface Finaxy : vrais visuels ou supports stylisés étiquetés · le rose Relax jamais en texte.</p></article>
</div></body></html>'''
(PROJECT / "storyboard.html").write_text(html)
print("wrote storyboard.html", len(html))
