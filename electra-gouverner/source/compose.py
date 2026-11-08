"""Electra — 'Une carte pour les gouverner toutes' text overlays.
Builds separate RGBA layers (gradient, headline, body) so stills and video share one layout."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
ANTON = f"{F}/fontsource-anton-5.3.0/files/anton-latin-400-normal.woff"
MONT_M = f"{F}/fontsource-montserrat-5.3.0/files/montserrat-latin-500-normal.woff"
MONT_B = f"{F}/fontsource-montserrat-5.3.0/files/montserrat-latin-700-normal.woff"

WHITE = (255, 255, 255, 255)
MINT = (70, 226, 180, 255)  # Electra+ mint accent

HEAD = [[("UNE CARTE POUR LES", WHITE)], [("GOUVERNER TOUTES.", MINT)]]
BODY = [
    [("Avec la carte Electra, accédez à ", WHITE, "m"), ("plus d’un million", MINT, "b")],
    [("de points de charge", MINT, "b"), (" en Europe.", WHITE, "m")],
]


def text_w(font, s, track=0):
    return font.getlength(s) + track * max(len(s) - 1, 0)


def draw_tracked(d, x, y, s, font, fill, track):
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + track
    return x


def shadowed(layer, radius, opacity):
    a = layer.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    a = a.point(lambda v: int(v * opacity))
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(a)
    return Image.alpha_composite(sh, layer)


def layers(W, H, bottom_margin=0.075, grad_start=0.50):
    # --- headline (Anton, condensed, uppercase) ---
    hs = int(W * 0.112)
    while True:
        hf = ImageFont.truetype(ANTON, hs)
        track = hs * 0.01
        widest = max(sum(text_w(hf, s, track) for s, _ in ln) for ln in HEAD)
        if widest <= W * 0.86:
            break
        hs -= 2
    h_lead = hs * 1.02
    # --- body (Montserrat) ---
    bs = int(W * 0.0335)
    fm, fb = ImageFont.truetype(MONT_M, bs), ImageFont.truetype(MONT_B, bs)
    pick = {"m": fm, "b": fb}
    b_lead = bs * 1.42

    asc_h = hf.getbbox("UNE")[1]  # top offset of caps
    cap_h = hf.getbbox("H")[3] - asc_h
    gap = bs * 1.25

    body_h = b_lead * (len(BODY) - 1) + bs
    head_h = h_lead * (len(HEAD) - 1) + cap_h
    y_body = H * (1 - bottom_margin) - body_h
    y_head = y_body - gap - head_h

    head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(head)
    for i, ln in enumerate(HEAD):
        lw = sum(text_w(hf, s, track) for s, _ in ln)
        x = (W - lw) / 2
        for s, c in ln:
            x = draw_tracked(d, x, y_head + i * h_lead - asc_h, s, hf, c, track) - track + track
    head = shadowed(head, hs * 0.18, 0.55)

    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    for i, ln in enumerate(BODY):
        lw = sum(pick[k].getlength(s) for s, _, k in ln)
        x = (W - lw) / 2
        for s, c, k in ln:
            d.text((x, y_body + i * b_lead), s, font=pick[k], fill=c, anchor="la")
            x += pick[k].getlength(s)
    body = shadowed(body, bs * 0.35, 0.7)

    # --- bottom gradient for legibility ---
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g0 = int(H * grad_start)
    px = grad.load()
    col = Image.new("L", (1, H), 0)
    for y in range(g0, H):
        t = (y - g0) / (H - g0)
        col.putpixel((0, y), int(255 * 0.82 * (t ** 1.4)))
    grad = Image.new("RGBA", (W, H), (4, 14, 20, 255))  # Electra deep navy-black
    grad.putalpha(col.resize((W, H)))
    return grad, head, body


def still(src, dst, **kw):
    im = Image.open(src).convert("RGBA")
    g, h, b = layers(*im.size, **kw)
    out = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(im, g), h), b)
    out.convert("RGB").save(dst, quality=95)


def video_layers(W, H, outdir, **kw):
    g, h, b = layers(W, H, **kw)
    for n, l in (("grad", g), ("head", h), ("body", b)):
        l.save(f"{outdir}/{n}.png")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "still":
        still(sys.argv[2], sys.argv[3])
    else:
        video_layers(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
