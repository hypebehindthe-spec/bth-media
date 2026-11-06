"""Thumbnail / cover image for a Behind The Hype reel (YouTube Shorts thumbnail).

Usage: python3 bth_thumb.py '<json>' out.jpg
json: {"kicker": "UPI RECORD", "big": "₹1 LAKH CRORE", "sub": "moved every single day", "hook": "How did India get here?"}
Vertical 1080x1920 JPEG under 2 MB. All key text sits in the centre band so it survives square and 16:9 crops.
"""
import json, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FD = "/usr/share/fonts/truetype/google-fonts/"
INK, YEL, WHITE, GREY = (14, 17, 22), (255, 199, 44), (245, 245, 240), (150, 155, 165)
W, H, M = 1080, 1920, 80


def fit(d, text, path, maxw, start, minsize=60):
    size = start
    while size > minsize:
        f = ImageFont.truetype(path, size)
        if d.textlength(text, font=f) <= maxw:
            return f
        size -= 4
    return ImageFont.truetype(path, minsize)


def wrap_lines(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return [l for l in lines if l]


def make(spec, out):
    img = Image.new("RGB", (W, H), INK)
    # soft yellow glow behind the headline
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((-200, 520, W + 200, 1400), fill=130)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), (60, 48, 12)), img, glow)
    d = ImageDraw.Draw(img)

    bold = FD + "Poppins-Bold.ttf"
    # kicker pill
    kf = ImageFont.truetype(bold, 54)
    kt = spec.get("kicker", "").upper()
    y = 600
    if kt:
        tw = d.textlength(kt, font=kf)
        d.rounded_rectangle(((W - tw) / 2 - 36, y, (W + tw) / 2 + 36, y + 96), radius=48, fill=YEL)
        d.text(((W - tw) / 2, y + 12), kt, font=kf, fill=INK)
        y += 150
    # big headline, one or two lines, auto-fitted
    big = spec["big"].upper()
    parts = big.split("|") if "|" in big else [big]
    for part in parts:
        f = fit(d, part.strip(), bold, W - 2 * M, 190)
        tw = d.textlength(part.strip(), font=f)
        d.text(((W - tw) / 2 + 6, y + 6), part.strip(), font=f, fill=(0, 0, 0))
        d.text(((W - tw) / 2, y), part.strip(), font=f, fill=YEL)
        y += int(f.size * 1.12)
    # sub line
    sf = ImageFont.truetype(bold, 72)
    for ln in wrap_lines(d, spec.get("sub", ""), sf, W - 2 * M):
        tw = d.textlength(ln, font=sf)
        d.text(((W - tw) / 2, y + 10), ln, font=sf, fill=WHITE)
        y += 90
    # hook question
    hf = ImageFont.truetype(FD + "Poppins-Medium.ttf", 54)
    y += 40
    for ln in wrap_lines(d, spec.get("hook", ""), hf, W - 2 * M):
        tw = d.textlength(ln, font=hf)
        d.text(((W - tw) / 2, y), ln, font=hf, fill=GREY)
        y += 70
    # brand footer
    bf = ImageFont.truetype(bold, 44)
    d.ellipse((W / 2 - 60, H - 380, W / 2 + 60, H - 260), fill=YEL)
    lt = "BTH"
    lf = ImageFont.truetype(bold, 40)
    d.text((W / 2 - d.textlength(lt, font=lf) / 2, H - 346), lt, font=lf, fill=INK)
    bt = "BEHIND THE HYPE"
    d.text(((W - d.textlength(bt, font=bf)) / 2, H - 230), bt, font=bf, fill=WHITE)
    img.save(out, quality=90)


if __name__ == "__main__":
    make(json.loads(sys.argv[1]), sys.argv[2])
    print(sys.argv[2])
