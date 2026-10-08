"""Generate storyboard.html (review sheet) for the Relax x Finaxy case — v2, Relax identity.

Each cell is an inline SVG on the real 1920x1080 canvas, so placement and type sizes read
exactly as they will in the build. Deterministic (seeded) layout.
Usage: python3 tools/storyboard_gen.py <project_dir> <version>
"""
import math
import random
import sys
from pathlib import Path

PROJECT = Path(sys.argv[1])
VERSION = sys.argv[2] if len(sys.argv) > 2 else "v2"

# Relax (the film)
WHITE, INK, INK2, LAV, PURPLE, PINK = "#FFFFFF", "#212C34", "#6B7278", "#D4CCEE", "#6955AA", "#FF0055"
CYAN, YELLOW, RED, GREY = "#56A0AA", "#ABA256", "#AA5655", "#A7AEB4"
# Finaxy (the work)
NAVY, FBLUE, SLATE, CREAM, BURG, OLDBLUE = "#191853", "#5A80D9", "#4A5892", "#F4F1EB", "#9C0A3F", "#174A8C"

TITLE, TEXT, SERIF = "Unbounded, Helvetica, sans-serif", "'DM Sans', Helvetica, Arial, sans-serif", "'Instrument Serif', Georgia, serif"

new_logo = (PROJECT / "assets/brand/finaxy-new.svg").read_text()
old_logo = (PROJECT / "assets/brand/finaxy-old.svg").read_text().replace('fill="white"', f'fill="{OLDBLUE}"')
relax_logo = (PROJECT / "assets/brand/relax-logo.svg").read_text()


def logo(svg, x, y, w, opacity=1.0):
    head, rest = svg.split(">", 1)
    inner = rest.rsplit("</svg>", 1)[0]
    vb = head.split('viewBox="')[1].split('"')[0].split()
    h = w * float(vb[3]) / float(vb[2])
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h:.1f}" viewBox="{" ".join(vb)}" opacity="{opacity}">{inner}</svg>'


def t(x, y, s, size, fam=TEXT, fill=INK, weight=400, anchor="start", italic=False, ls=0, opacity=1, upper=False):
    style = f"font-family:{fam};font-size:{size}px;font-weight:{weight};letter-spacing:{ls}em"
    if italic:
        style += ";font-style:italic"
    return (f'<text x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}" opacity="{opacity}" '
            f'style="{style}">{s.upper() if upper else s}</text>')


def washes(cx=(250, 700), yx=(1650, 640), px=(960, 560), k=1.0):
    """The relax-agency.com review-section washes: cyan left, yellow right, purple centre."""
    return (f'<rect width="1920" height="1080" fill="{WHITE}"/>'
            f'<ellipse cx="{cx[0]}" cy="{cx[1]}" rx="900" ry="620" fill="url(#wc)" opacity="{k}"/>'
            f'<ellipse cx="{yx[0]}" cy="{yx[1]}" rx="760" ry="560" fill="url(#wy)" opacity="{k}"/>'
            f'<ellipse cx="{px[0]}" cy="{px[1]}" rx="560" ry="460" fill="url(#wp)" opacity="{k}"/>')


def thread(d, w=6, head=None):
    s = (f'<path d="{d}" fill="none" stroke="{LAV}" stroke-width="{w * 4}" stroke-linecap="round" opacity=".55"/>'
         f'<path d="{d}" fill="none" stroke="url(#rib)" stroke-width="{w}" stroke-linecap="round"/>')
    if head:
        s += f'<circle cx="{head[0]}" cy="{head[1]}" r="{w * 2.2}" fill="{PINK}"/>'
    return s


def rail(active):
    steps = ["Comprendre", "Révéler", "Organiser", "Exprimer", "Déployer"]
    out, x = [], 120
    for i, s in enumerate(steps, 1):
        col = INK if i == active else (INK2 if i < active else "#C3C7CB")
        out.append(t(x, 110, f"0{i}", 22, fam=TITLE, weight=500, fill=PURPLE if i == active else col))
        out.append(t(x + 44, 110, s, 22, weight=600, fill=col, ls=0.04))
        x += 300
    out.append(f'<line x1="120" y1="134" x2="{120 + 300 * (active - 1) + 250}" y2="134" stroke="{PURPLE}" stroke-width="3"/>')
    return "".join(out)


def node(x, y, r=9, fill=GREY, label=None, lsize=24, lfill=None, ring=False):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
    if ring:
        s += f'<circle cx="{x}" cy="{y}" r="{r + 14}" fill="none" stroke="{PINK}" stroke-width="3"/>'
    if label:
        s += t(x + r + 12, y + lsize * 0.35, label, lsize, fill=lfill or INK2, weight=500)
    return s


def tag(x, y, label, color, size=24, fill_bg=None):
    w = len(label) * size * 0.56 + 44
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size * 1.9:.0f}" rx="{size:.0f}" fill="{fill_bg or color}"/>'
            + t(x + w / 2, y + size * 1.28, label, size, anchor="middle", fill=WHITE, weight=500))


def fx_panel(x, y, w, h, color=NAVY, rx=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{color}"/>'


DEFS = (f'<defs>'
        f'<radialGradient id="wc"><stop offset="0" stop-color="{CYAN}" stop-opacity=".30"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="wy"><stop offset="0" stop-color="{YELLOW}" stop-opacity=".30"/><stop offset="1" stop-color="{YELLOW}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="wp"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".22"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="rib" x1="0" x2="1"><stop offset="0" stop-color="{LAV}"/><stop offset=".55" stop-color="{PURPLE}"/><stop offset="1" stop-color="#C77DDB"/></linearGradient>'
        f'</defs>')

CHAOS_LABELS = ["IARD", "Santé", "Prévoyance", "Cyber", "Flottes", "Construction", "RC Pro", "Crédit",
                "Voyage", "Collection", "Cabinet", "Cabinet", "Marque acquise", "Marque acquise",
                "Équin", "Plaisance", "Expertise", "Interlocuteur", "Interlocuteur", "Héritage"]
rng = random.Random(7)
CHAOS = [(rng.uniform(140, 1780), rng.uniform(200, 900)) for _ in CHAOS_LABELS]


def f01():
    s = washes(k=0.5)
    for (x, y), lab in zip(CHAOS, CHAOS_LABELS):
        if 640 < x < 1300 and 380 < y < 700:
            continue
        s += node(x, y, r=rng.choice([6, 8, 11]), label=lab, lsize=22, lfill=GREY)
    s += logo(old_logo, 790, 450, 340, opacity=0.85)
    s += t(120, 1000, "+ 12 000", 120, fam=TITLE, weight=500)
    s += t(800, 1000, "entreprises clientes", 40, fill=INK2, weight=300)
    return s


def f02():
    s = washes()
    s += t(120, 330, "Bien au-delà d'un simple", 54, fill=INK2, weight=300)
    s += t(120, 460, "problème de logo.", 96, fam=TITLE, fill=GREY, weight=400)
    s += f'<line x1="110" y1="428" x2="1150" y2="428" stroke="{PINK}" stroke-width="6"/>'
    s += t(120, 600, "Un problème de", 54, weight=300)
    s += t(120, 740, "cohérence globale.", 110, fam=TITLE, weight=500)
    pts = [(1360, 260), (1520, 400), (1700, 250), (1420, 860), (1640, 880), (1760, 620)]
    for i, (x, y) in enumerate(pts):
        s += node(x, y, r=10, fill=PURPLE if i == 0 else GREY, ring=i == 0)
    s += thread("M0 1010 C 1250 1010, 1230 330, 1336 266", 6)
    s += t(1800, 1010, "simplifier, sans appauvrir", 34, anchor="end", fill=INK2, italic=True)
    return s


def f03():
    s = washes(k=0.8) + rail(1)
    pts = [(280, 640, "dirigeants"), (660, 440, "collaborateurs"), (1060, 700, "métiers"), (1460, 460, "marché")]
    d = "M0 820 " + " ".join(f"S {x - 120} {y + 160}, {x} {y}" for x, y, _ in pts) + " S 1700 700, 1780 640"
    s += thread(d, 6, head=(1780, 640))
    for x, y, lab in pts:
        s += node(x, y, r=12, fill=PURPLE)
        s += t(x, y - 50, lab, 44, fam=TITLE, anchor="middle", weight=400)
    s += t(120, 1000, "Comprendre ce que Finaxy était vraiment.", 40, fill=INK2, weight=300)
    return s


def f04():
    s = washes(k=0.8) + rail(2)
    rng2 = random.Random(3)
    left = [(rng2.uniform(200, 760), rng2.uniform(320, 820)) for _ in range(12)]
    right = [(rng2.uniform(1160, 1720), rng2.uniform(320, 820)) for _ in range(12)]
    for grp, col in ((left, FBLUE), (right, BURG)):
        for i, (x, y) in enumerate(grp):
            for (x2, y2) in grp[i + 1:i + 3]:
                s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2" opacity=".35"/>'
        for x, y in grp:
            s += node(x, y, r=8, fill=col)
    s += thread("M0 600 C 300 600, 300 570, 480 570 C 760 400, 1160 760, 1440 570 S 1800 560, 1920 560", 6)
    s += t(480, 960, "La force d'un groupe.", 66, fam=SERIF, anchor="middle", fill=NAVY)
    s += t(1440, 960, "L'esprit d'un cabinet.", 66, fam=SERIF, anchor="middle", italic=True, fill=BURG)
    s += t(960, 1040, "plateforme de marque Finaxy", 22, anchor="middle", fill=INK2, weight=600, upper=True, ls=0.14)
    return s


def f05():
    s = f'<rect width="1920" height="1080" fill="{WHITE}"/>'
    s += fx_panel(160, 170, 1600, 640, NAVY, 28)
    rng3 = random.Random(5)
    pts = [(rng3.uniform(200, 1720), rng3.uniform(210, 770)) for _ in range(34)]
    for i, (x, y) in enumerate(pts):
        for (x2, y2) in pts[i + 1:i + 3]:
            s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{CREAM}" stroke-width="1.5" opacity=".14"/>'
    s += t(960, 460, "L'intelligence collective", 132, fam=SERIF, anchor="middle", fill=CREAM)
    s += t(960, 610, "du risque.", 132, fam=SERIF, anchor="middle", italic=True, fill=CREAM)
    s += f'<rect x="900" y="660" width="120" height="6" rx="3" fill="{BURG}"/>'
    s += thread("M0 900 L 1920 900", 6)
    s += t(160, 980, "Le principe qui organise tout le reste.", 36, weight=300, fill=INK2)
    return s


ARCH = [("Entreprises & institutions", NAVY, ["Protégez votre activité", "vos collaborateurs", "vos actifs"]),
        ("Affinitaire & partenariats", FBLUE, ["Affinitaire voyage", "Multi-secteurs", "Banque et assurance"]),
        ("Clientèle privée", SLATE, ["Prestige & collection", "Univers équin", "Plaisance · Forêts"])]


def f06():
    s = washes(k=0.6) + rail(3)
    s += logo(new_logo.replace('fill="#F4F1EB"', f'fill="{NAVY}"'), 840, 180, 240)
    for i, (lab, col, subs) in enumerate(ARCH):
        x = 160 + i * 560
        s += f'<path d="M960 260 C 960 330, {x + 240} 320, {x + 240} 390" fill="none" stroke="{PURPLE}" stroke-width="4"/>'
        s += fx_panel(x, 390, 480, 470, col, 18)
        s += t(x + 36, 470, lab.split(" & ")[0] + (" &" if "&" in lab else ""), 40, fam=SERIF, fill=CREAM)
        if "&" in lab:
            s += t(x + 36, 520, lab.split(" & ")[1], 40, fam=SERIF, fill=CREAM)
        for j, sub in enumerate(subs):
            w = len(sub) * 12.5 + 40
            s += (f'<rect x="{x + 36}" y="{600 + j * 66}" width="{w:.0f}" height="46" rx="23" fill="none" stroke="{CREAM}" stroke-width="2" opacity=".8"/>'
                  + t(x + 56, 631 + j * 66, sub, 22, fill=CREAM))
    s += node(120, 940, r=10, fill=GREY, label="marques autonomes conservées", lsize=24)
    s += f'<line x1="130" y1="930" x2="420" y2="860" stroke="{GREY}" stroke-width="2" stroke-dasharray="8 10"/>'
    s += t(1800, 950, "architecture · verticales · naming", 30, anchor="end", fill=INK2, weight=300)
    s += t(1800, 1000, "architecture réelle (finaxy.com)", 20, anchor="end", fill=INK2, weight=600, upper=True, ls=0.14)
    return s


def f07():
    s = washes(k=0.6) + rail(4)
    s += logo(old_logo, 140, 230, 250, opacity=0.35)
    s += t(265, 330, "avant", 22, fill=INK2, weight=600, anchor="middle", upper=True, ls=0.18)
    s += fx_panel(470, 200, 1300, 560, NAVY, 28)
    s += logo(new_logo, 640, 330, 960)
    s += thread("M0 840 C 700 840, 1500 820, 1620 360", 6, head=(1620, 360))
    traits = [(250, 920, "Ancré"), (740, 960, "Architecte"), (1200, 960, "Team player"), (1680, 920, "Pédagogue")]
    for x, y, lab in traits:
        s += t(x, y, lab, 54, fam=SERIF, anchor="middle", italic=True, fill=NAVY)
    s += t(1770, 190, "un logo · une identité · une voix", 28, fill=INK2, weight=300, anchor="end")
    return s


def support(x, y, w, h, kind, label):
    s = fx_panel(x, y, w, h, kind, 10)
    lw = min(w * 0.6, 260)
    s += logo(new_logo if kind != CREAM else new_logo.replace('fill="#F4F1EB"', f'fill="{NAVY}"'),
              x + (w - lw) / 2, y + h * 0.38, lw)
    if label:
        s += t(x + w / 2, y + h + 34, label, 22, anchor="middle", fill=INK2, weight=500)
    return s


def f08():
    s = washes(k=0.6) + rail(5)
    s += support(120, 230, 330, 560, CREAM, "Kakemonos")
    s += support(500, 230, 460, 300, NAVY, "Plaquettes B2B")
    s += support(500, 600, 220, 130, NAVY, "Cartes de visite")
    s += support(740, 600, 220, 130, CREAM, "")
    s += support(1010, 230, 400, 230, FBLUE, "Masques de présentation")
    s += support(1010, 520, 190, 210, BURG, "Cartes de vœux")
    s += support(1220, 520, 190, 210, CREAM, "")
    for r in range(7):
        for c in range(6):
            col = [NAVY, CREAM, FBLUE, BURG, SLATE][(r * 6 + c) % 5]
            s += f'<rect x="{1460 + c * 58}" y="{230 + r * 72}" width="46" height="58" rx="5" fill="{col}"/>'
    s += t(1630, 770, "×2 ×2 ×2 …", 34, fam=TITLE, anchor="middle", weight=400, fill=PURPLE)
    s += thread("M280 520 C 420 520, 520 380, 730 380 S 1000 340, 1210 340 S 1400 300, 1640 420", 5)
    s += f'<rect x="560" y="860" width="1240" height="110" rx="55" fill="{WHITE}" stroke="{LAV}" stroke-width="3"/>'
    s += t(610, 928, "Agent IA", 28, fill=PURPLE, weight=600)
    s += t(760, 928, "« On réunit les bonnes expertises pour construire une réponse adaptée… »", 26, fill=INK, weight=300)
    s += t(120, 1000, "+ LinkedIn · nouveau site — visuels réels à intégrer", 22, fill=INK2, weight=600, upper=True, ls=0.12)
    return s


DISC = [("Stratégie", PURPLE), ("Architecture de marque", CYAN), ("Naming", RED), ("Design", PURPLE),
        ("Éditorial", YELLOW), ("Production", CYAN), ("IA", RED)]


def f09():
    s = washes(k=0.9)
    pos = [(260, 270), (640, 400), (920, 230), (1200, 410), (1460, 260), (1720, 400), (1000, 520)]
    for i, (x, y) in enumerate(pos):
        for (x2, y2) in pos[i + 1:i + 3]:
            s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{LAV}" stroke-width="3"/>'
    for (x, y), (lab, col) in zip(pos, DISC):
        s += tag(x - (len(lab) * 24 * 0.56 + 44) / 2, y - 23, lab, col, 24)
    for x, y in pos:
        s += f'<path d="M{x} {y + 24} C {x} 640, 960 620, 960 760" fill="none" stroke="{PURPLE}" stroke-width="2" opacity=".35"/>'
    s += thread("M0 760 L 1920 760", 6, head=(960, 760))
    s += t(960, 900, "Pour chaque enjeu, la bonne équipe.", 64, fam=TITLE, anchor="middle", weight=400)
    s += t(960, 980, "Et elle joue comme une seule.", 40, fill=INK2, weight=300, anchor="middle")
    return s


def f10():
    s = f'<rect width="1920" height="1080" fill="{WHITE}"/>'
    s += f'<rect width="1920" height="520" fill="{LAV}" opacity=".45"/>'
    rng5 = random.Random(2)
    cols = [PURPLE, CYAN, RED, YELLOW]
    for i in range(46):
        x, y = rng5.uniform(140, 1800), rng5.uniform(140, 470)
        a, L = rng5.uniform(0, 6.28), rng5.uniform(30, 90)
        c = cols[i % 4]
        s += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + L * math.cos(a):.0f}" y2="{y + L * math.sin(a):.0f}" stroke="{c}" stroke-width="3" opacity=".6"/>'
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{c}"/>'
    s += t(120, 100, "Côté Relax", 30, fam=TITLE, weight=500)
    s += t(1800, 100, "beaucoup de mouvement", 30, anchor="end", fill=INK2, weight=300)
    s += t(120, 610, "Côté client", 30, fam=TITLE, weight=500)
    s += t(1800, 610, "un seul fil", 30, anchor="end", fill=INK2, weight=300)
    s += thread("M0 760 L 1920 760", 6)
    s += t(960, 900, "On construit l'équipe autour du projet.", 62, fam=TITLE, anchor="middle", weight=400)
    s += t(960, 990, "Aucune couture.", 44, anchor="middle", fill=PURPLE, weight=500)
    return s


def f11():
    s = washes(k=1.0)
    words = [("IARD", GREY), ("Ancré", NAVY), ("Kakemonos", BURG), ("cohérence", INK), ("Naming", RED),
             ("Design", PURPLE), ("dirigeants", INK2), ("Cartes de vœux", BURG), ("LinkedIn", FBLUE),
             ("Architecte", NAVY), ("Agent IA", PURPLE), ("Stratégie", PURPLE), ("Pédagogue", NAVY),
             ("marché", INK2), ("Plaquettes B2B", NAVY), ("Éditorial", YELLOW), ("Team player", NAVY),
             ("Cabinet", GREY), ("Production", CYAN), ("verticales", INK2)]
    for i, (w, c) in enumerate(words):
        a, r = i * 0.62, 170 + i * 21
        x, y = 960 + r * math.cos(a), 470 + r * 0.55 * math.sin(a)
        s += t(f"{x:.0f}", f"{y:.0f}", w, 20 + i * 1.3, anchor="middle", fill=c, opacity=max(0.3, 1 - i * 0.03),
               fam=SERIF if c in (NAVY, BURG) else TEXT)
    sp = "M960 470 " + " ".join(
        f"L {960 + (8 + k * 9) * math.cos(k * 0.35):.0f} {470 + (8 + k * 9) * 0.55 * math.sin(k * 0.35):.0f}"
        for k in range(1, 90))
    s += f'<path d="{sp}" fill="none" stroke="url(#rib)" stroke-width="4" opacity=".8"/>'
    s += f'<circle cx="960" cy="470" r="16" fill="{PINK}"/>'
    s += t(960, 900, "Les meilleurs experts pour votre projet.", 58, fam=TITLE, anchor="middle", weight=400)
    s += t(960, 985, "Coordonnés par un partenaire de confiance.", 40, anchor="middle", fill=INK2, weight=300)
    return s


def f12():
    s = washes(k=0.7)
    for r, o in ((820, .07), (560, .1), (320, .14)):
        s += f'<circle cx="960" cy="540" r="{r}" fill="none" stroke="{PURPLE}" stroke-width="2" opacity="{o}"/>'
    s += logo(relax_logo, 610, 430, 700)
    s += t(960, 780, "Maintenant, relax, on s'occupe du reste.", 38, anchor="middle", fill=INK2, weight=300)
    s += t(960, 840, "(option — signature du site Relax)", 20, anchor="middle", fill=GREY, weight=600, upper=True, ls=0.12)
    return s


FRAMES = [
    ("01", "Chaos hérité", "0:00–0:09", f01, "cut",
     "<b>Ça part vite.</b> Des nœuds gris dérivent et tremblent ; l'ancien logo flotte sans hiérarchie ; « + 12 000 » se compte. Pas encore de fil."),
    ("02", "Le vrai sujet", "0:09–0:19", f02, "cut",
     "<b>« problème de logo » se barre</b> ; « cohérence globale » s'écrit. Le fil entre par le bas-gauche et calme le premier nœud."),
    ("03", "Comprendre", "0:19–0:27", f03, "fil",
     "<b>Le fil court de nœud en nœud</b>, sa tête rose devant ; chaque contact fait naître un mot d'enquête. Le rail des 5 étapes s'installe."),
    ("04", "Révéler", "0:27–0:36", f04, "fil",
     "<b>Les nœuds gris prennent les couleurs Finaxy</b> et se maillent en deux pôles que le fil relie : groupe / cabinet."),
    ("05", "L'intelligence collective", "0:36–0:40.5", f05, "fondu",
     "<b>Plan tenu.</b> Un panneau Finaxy (marine) porte la phrase en serif ; elle monte par masque, puis rien ne bouge."),
    ("06", "Organiser", "0:40.5–0:51", f06, "fil",
     "<b>Les mêmes nœuds se rangent</b> sous le logo dans les 3 vraies verticales (finaxy.com) ; les marques autonomes restent en pointillé."),
    ("07", "Exprimer", "0:51–0:59", f07, "fil",
     "<b>Le fil signe la virgule bordeaux</b> en passant : l'ancien logo s'efface, le nouveau se dessine. Les 4 traits se posent dessous."),
    ("08", "Déployer", "0:59–1:11", f08, "fil",
     "<b>1 → 2 → 4 → 8 → 64</b> : les supports Finaxy se démultiplient, reliés par le fil. L'agent IA écrit la dernière ligne."),
    ("09", "La bonne équipe", "1:11–1:20", f09, "recul",
     "<b>Recul</b> : les disciplines (pastilles aux couleurs Relax) s'allument dans l'ordre de la VO et convergent vers un seul fil."),
    ("10", "Sans couture", "1:20–1:30.5", f10, "fil",
     "<b>Deux tempos</b> : en haut l'agitation colorée des experts, en bas un seul fil immobile. « Aucune couture. »"),
    ("11", "Tourbillon", "1:30.5–1:36.5", f11, "fil",
     "<b>Tout le film tourbillonne</b> — mots, supports, disciplines — et s'agrège vers le point rose, qui ralentit."),
    ("12", "Respiration → relax•", "1:36.5–1:43.5", f12, "souffle",
     "<b>Inspiration</b> : le point rose se dilate, tout se suspend. <b>Expiration</b> relâchée : les ondes s'ouvrent, « relax » s'écrit et le point se pose."),
]


def cell(num, name, span, fn, seam, note):
    svg = f'<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">{DEFS}{fn()}</svg>'
    return f'''<article class="cell" id="frame-{num}">
  <div class="canvas">{svg}</div>
  <div class="label"><span>{num} · {name}</span><span>{span}</span></div>
  <p class="note">{note}</p>
  <span class="chip">→ {seam}</span>
</article>'''


acts = [("Avant — la complexité héritée", FRAMES[0:2]),
        ("La chaîne de décisions — Comprendre → Révéler → Organiser → Exprimer → Déployer", FRAMES[2:8]),
        ("La méthode Relax — et le soulagement", FRAMES[8:12])]
cells = "".join(f'<div class="act">{a}</div>' + "".join(cell(*f) for f in frs) for a, frs in acts)
seams = " ".join(f'<span><b>{f[0]}</b> {f[4]}</span>' for f in FRAMES)
sw = lambda c, n: f'<span class="sw"><i style="background:{c}"></i>{n} {c}</span>'

html = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storyboard — Relax × Finaxy ({VERSION})</title>
<style>
{(PROJECT / "assets/fonts/fonts.css").read_text()}
*{{box-sizing:border-box;margin:0}}
body{{background:#F6F5F9;color:{INK};font-family:'DM Sans',Helvetica,Arial,sans-serif;padding:48px 40px 80px}}
header{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-bottom:1px solid #DCDAE3;padding-bottom:24px;flex-wrap:wrap}}
h1{{font-family:Unbounded,Helvetica,sans-serif;font-weight:500;font-size:44px;line-height:1.1}}
h1 .dot{{color:{PINK}}}
.dek{{color:{INK2};font-size:16px;max-width:780px;margin-top:12px;line-height:1.55}}
.tag{{font-size:13px;font-weight:500;background:{INK};color:#fff;padding:10px 16px;border-radius:99px;white-space:nowrap}}
.changes{{margin:22px 0 0;padding:16px 20px;background:#fff;border-radius:14px;font-size:14px;line-height:1.6;outline:1px solid #E6E3EE}}
.changes b{{color:{PURPLE}}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 22px}}
@media (max-width:1100px){{.grid{{grid-template-columns:1fr}}}}
.act{{grid-column:1/-1;margin-top:30px;padding:12px 0 0;border-top:2px solid {LAV};font-family:Unbounded,Helvetica,sans-serif;font-size:13px;font-weight:500;color:{PURPLE}}}
.cell{{position:relative}}
.canvas{{aspect-ratio:16/9;container-type:inline-size;border-radius:14px;overflow:hidden;box-shadow:0 2px 14px rgba(31,20,67,.08)}}
.canvas > svg{{display:block;width:100%;height:100%}}
.label{{display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-top:12px}}
.label span:first-child{{font-family:Unbounded,Helvetica,sans-serif;font-weight:500;font-size:12px}}
.label span:last-child{{color:{INK2}}}
.note{{font-size:14px;line-height:1.5;color:#3d474f;margin-top:6px;padding-right:90px}}
.note b{{color:{INK}}}
.chip{{position:absolute;right:0;bottom:2px;font-size:11px;font-weight:600;background:{LAV};color:#2a2244;padding:4px 10px;border-radius:99px}}
.info{{background:#fff;border-radius:14px;padding:24px;font-size:14px;line-height:1.6;box-shadow:0 2px 14px rgba(31,20,67,.06)}}
.info h3{{font-family:Unbounded,Helvetica,sans-serif;font-size:13px;font-weight:500;margin-bottom:12px;color:{PURPLE}}}
.seams{{display:flex;flex-wrap:wrap;gap:8px}}
.seams span{{background:#F1EEF9;border-radius:99px;padding:4px 10px;font-size:12px}}
.sw{{display:inline-flex;align-items:center;gap:8px;margin:0 14px 8px 0;font-size:12px}}
.sw i{{width:20px;height:20px;border-radius:6px;display:inline-block;outline:1px solid #E6E3EE}}
</style></head><body>
<header>
  <div><h1>Relax × Finaxy — le fil<span class="dot">.</span> <span style="font-size:20px;color:{INK2}">{VERSION}</span></h1>
  <p class="dek">Case agence : Relax réunit et coordonne, sans couture, les meilleurs experts autour du projet — le client, lui, ne voit qu'un seul fil. Le film parle en Relax ; l'identité Finaxy y apparaît comme le travail réalisé.</p></div>
  <span class="tag">1920×1080 · ~100 s · 12 scènes · VO Algieba</span>
</header>
<div class="changes"><b>Changements depuis v1</b> — DA du film = DA Relax (fond blanc et lavis pastel du site, Unbounded + DM Sans, le ruban lavande comme fil, le point rose du logo comme tête du fil). L'identité Finaxy (marine, crème, bordeaux, serif) n'apparaît plus que sur les livrables montrés. VO scène 02 : « bien au-delà d'un simple problème de logo… un problème de cohérence globale ». Scène 06 : les 3 vraies verticales de finaxy.com. Scène 12 : le vrai logo relax•.</div>
<div class="grid">
{cells}
<div class="act">Repères</div>
<article class="cell info"><h3>Carte des transitions</h3><div class="seams">{seams}</div>
<p style="margin-top:14px;color:{INK2}">Le fil avance vers la droite, le monde glisse vers la gauche. Il n'est jamais coupé, sauf en 01→02 (il naît) et 11→12 (il devient souffle, puis le point du logo).</p></article>
<article class="cell info"><h3>Tokens</h3>
<p style="font-weight:600;margin-bottom:6px">Relax — le film</p>{sw(WHITE, "Blanc")}{sw(INK, "Encre")}{sw(LAV, "Lavande")}{sw(PURPLE, "Violet")}{sw(PINK, "Point")}{sw(CYAN, "Cyan")}{sw(YELLOW, "Jaune")}
<p style="font-weight:600;margin:8px 0 6px">Finaxy — le travail montré</p>{sw(NAVY, "Marine")}{sw(FBLUE, "Bleu")}{sw(CREAM, "Crème")}{sw(BURG, "Bordeaux")}
<p style="margin-top:8px"><span style="font-family:Unbounded;font-size:20px">Unbounded</span> + DM Sans (Relax) · <span style="font-family:'Instrument Serif';font-size:24px">Instrument Serif</span> (paroles Finaxy)</p></article>
<article class="cell info"><h3>Interdits</h3>
<p>Pas d'effet catalogue · pas d'anglais à l'écran (sauf « naming », « Team player ») · les couleurs Finaxy ne deviennent jamais le fond du film · le rose Relax jamais en texte · pas de fausse interface : vrais visuels ou placeholders étiquetés · ni diaporama, ni écran de veille.</p></article>
</div></body></html>'''

(PROJECT / "storyboard.html").write_text(html)
print("wrote", PROJECT / "storyboard.html", len(html))
