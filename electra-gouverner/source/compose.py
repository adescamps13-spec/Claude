"""Electra — 'Une carte pour les gouverner toutes' text overlays.
Builds separate RGBA layers (gradient, headline, body) so stills and video share one layout."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
INTER = "/usr/share/fonts/opentype/inter"
HEAD_FONT = f"{INTER}/InterDisplay-Bold.otf"
BODY_REG = f"{INTER}/InterDisplay-Regular.otf"
BODY_BOLD = f"{INTER}/InterDisplay-Bold.otf"

# Colours sampled from Electra's "Summer Celebration" post
WHITE = (255, 255, 255, 255)
ICE = (231, 254, 253, 255)   # first headline line, near-white mint
MINT = (187, 254, 233, 255)  # pastel mint for the rest of the headline

HEAD = [[("UNE CARTE POUR", ICE)], [("LES GOUVERNER", MINT)], [("TOUTES.", MINT)]]
BODY = [
    [("Avec la carte Electra, accédez à ", WHITE, "m"), ("plus d’un million", WHITE, "b")],
    [("de points de charge", WHITE, "b"), (" en Europe.", WHITE, "m")],
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


def layers(W, H, bottom_margin=0.08, grad_start=0.55):
    # --- headline (bold grotesk, uppercase, tight tracking & leading) ---
    hs = int(W * 0.082)
    while True:
        hf = ImageFont.truetype(HEAD_FONT, hs)
        track = -hs * 0.012
        widest = max(sum(text_w(hf, s, track) for s, _ in ln) for ln in HEAD)
        if widest <= W * 0.78:
            break
        hs -= 2
    h_lead = hs * 0.92
    # --- body (regular + bold, white) ---
    bs = int(W * 0.031)
    fm, fb = ImageFont.truetype(BODY_REG, bs), ImageFont.truetype(BODY_BOLD, bs)
    pick = {"m": fm, "b": fb}
    b_lead = bs * 1.32

    asc_h = hf.getbbox("UNE")[1]  # top offset of caps
    cap_h = hf.getbbox("H")[3] - asc_h
    gap = bs * 1.55

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
    head = shadowed(head, hs * 0.22, 0.45)

    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    for i, ln in enumerate(BODY):
        lw = sum(pick[k].getlength(s) for s, _, k in ln)
        x = (W - lw) / 2
        for s, c, k in ln:
            d.text((x, y_body + i * b_lead), s, font=pick[k], fill=c, anchor="la")
            x += pick[k].getlength(s)
    body = shadowed(body, bs * 0.4, 0.6)

    # --- bottom gradient for legibility ---
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g0 = int(H * grad_start)
    px = grad.load()
    col = Image.new("L", (1, H), 0)
    for y in range(g0, H):
        t = (y - g0) / (H - g0)
        col.putpixel((0, y), int(255 * 0.72 * (t ** 1.5)))
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
