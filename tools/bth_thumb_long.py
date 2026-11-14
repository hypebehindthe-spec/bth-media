"""16:9 YouTube thumbnail (1280x720) for long videos, in the style that works for story channels:
two short lines of huge outlined text (white + yellow), one big illustration ringed by a red hand-drawn
circle, a small location/year tag. Keep the words different from the video title.

Usage: python3 tools/bth_thumb_long.py '<json>' out.jpg
json: {"line1": "HE BEAT HUL", "line2": "WITH ₹3.50", "tag": "NIRMA · 1969", "art": "🚲", "art2": "🏢", "bg": "sun"}
"""
import json, math, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bth_reel3 import art_image, soft_shadow, PALETTE  # noqa: E402

FD = "/usr/share/fonts/truetype/google-fonts/"
W, H = 1280, 720
INK, YEL, WHITE, RED = (14, 17, 22), (255, 199, 44), (255, 255, 255), (226, 54, 72)


def fit(d, text, maxw, start):
    size = start
    while size > 40:
        f = ImageFont.truetype(FD + "Poppins-Bold.ttf", size)
        if d.textlength(text, font=f) <= maxw:
            return f
        size -= 4
    return ImageFont.truetype(FD + "Poppins-Bold.ttf", 40)


def make(spec, out):
    col = PALETTE.get(spec.get("bg", "sun"))
    img = Image.new("RGB", (W, H), col)
    light = tuple(min(255, int(c + (255 - c) * 0.6)) for c in col)
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((640, 60, 1240, 660), fill=220)
    g = g.filter(ImageFilter.GaussianBlur(90))
    img = Image.composite(Image.new("RGB", (W, H), light), img, g)
    d = ImageDraw.Draw(img)
    if spec.get("art2"):
        a2 = art_image(spec["art2"], 200)
        img.paste(a2, (1050, 70), a2)
    a = art_image(spec["art"], 430)
    ax, ay = 930 - a.width // 2, 400 - a.height // 2
    sh, pad = soft_shadow(a, 14, 0.25)
    img.paste(sh, (ax + 14 - pad, ay + 22 - pad), sh)
    img.paste(a, (ax, ay), a)
    pts = []
    rw, rh = a.width * 0.66, a.height * 0.7
    for i in range(100):
        t = -math.pi * 0.6 + 2 * math.pi * 1.08 * i / 99
        wob = 1 + 0.04 * math.sin(3 * t)
        x = 930 + rw * wob * math.cos(t) * math.cos(-0.12) - rh * wob * math.sin(t) * math.sin(-0.12)
        y = 400 + rw * wob * math.cos(t) * math.sin(-0.12) + rh * wob * math.sin(t) * math.cos(-0.12)
        pts.append((x, y))
    d.line(pts, fill=RED, width=16, joint="curve")
    f1 = fit(d, spec["line1"], 700, 150)
    f2 = fit(d, spec["line2"], 700, 150)
    y = 140
    d.text((60, y), spec["line1"], font=f1, fill=WHITE, stroke_width=12, stroke_fill=INK)
    y += int(f1.size * 1.1)
    d.text((60, y), spec["line2"], font=f2, fill=YEL, stroke_width=12, stroke_fill=INK)
    tf = ImageFont.truetype(FD + "Poppins-Bold.ttf", 34)
    tag = spec.get("tag", "")
    if tag:
        tw = d.textlength(tag, font=tf)
        d.rounded_rectangle((60, 600, 60 + tw + 44, 660), radius=30, fill=RED)
        d.text((82, 607), tag, font=tf, fill=WHITE)
    img.save(out, quality=92)


if __name__ == "__main__":
    make(json.loads(sys.argv[1]), sys.argv[2])
    print(sys.argv[2])
