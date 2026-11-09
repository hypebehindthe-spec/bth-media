"""Behind The Hype data carousel builder (1080x1350 JPEG slides, brand style).

Usage: python3 tools/bth_carousel.py posts/post_NNN_carousel.json
spec: {"out_prefix": "posts/post_NNN_s", "slides": [{"kicker": "...", "lines": [["text", style], ...]}]}
styles: "w" big white, "y" big yellow, "W" medium white, "Y" medium yellow, "s" body, "g" small grey source.
Each slide gets the BEHIND THE HYPE label, a slide counter and the handle at the bottom.
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/google-fonts/"
INK, YEL, WHITE, GREY = (14, 17, 22), (255, 199, 44), (245, 245, 240), (150, 155, 165)
W, H, M = 1080, 1350, 90
F = {"w": ("Poppins-Bold.ttf", 104, WHITE), "y": ("Poppins-Bold.ttf", 120, YEL),
     "W": ("Poppins-Bold.ttf", 62, WHITE), "Y": ("Poppins-Bold.ttf", 62, YEL),
     "s": ("Poppins-Medium.ttf", 44, WHITE), "g": ("Poppins-Regular.ttf", 32, GREY)}
GAP = {"w": 18, "y": 18, "W": 26, "Y": 26, "s": 22, "g": 0}


def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out


def slide(s, i, n, path):
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    lab = ImageFont.truetype(FD + "Poppins-Bold.ttf", 30)
    d.text((M, 80), "BEHIND THE HYPE", font=lab, fill=YEL)
    d.rectangle((M, 124, M + 70, 129), fill=YEL)
    cnt = ImageFont.truetype(FD + "Poppins-Medium.ttf", 30)
    c = f"{i}/{n}"
    d.text((W - M - d.textlength(c, font=cnt), 80), c, font=cnt, fill=GREY)
    blocks = []
    if s.get("kicker"):
        blocks.append((s["kicker"].upper(), "kick"))
    blocks += [tuple(x) for x in s["lines"]]
    rendered = []
    for text, st in blocks:
        if st == "kick":
            f = ImageFont.truetype(FD + "Poppins-Bold.ttf", 36); col = YEL; gap = 34
        else:
            fn, sz, col = F[st]; f = ImageFont.truetype(FD + fn, sz); gap = GAP[st]
            while st in "wy" and max(d.textlength(x, font=f) for x in text.split("|")) > W - 2 * M and sz > 60:
                sz -= 6; f = ImageFont.truetype(FD + fn, sz)
        lines = []
        for part in text.split("|"):
            lines += wrap(d, part, f, W - 2 * M)
        lh = int(f.size * 1.18)
        rendered.append((lines, f, col, lh, gap))
    total = sum(len(l) * lh + g for l, f, c, lh, g in rendered)
    y = max(200, (H - total) // 2 - 20)
    for lines, f, col, lh, gap in rendered:
        for ln in lines:
            d.text((M, y), ln, font=f, fill=col); y += lh
        y += gap + 14
    hf = ImageFont.truetype(FD + "Poppins-Medium.ttf", 30)
    d.text((M, H - 100), "@behind.the.hype.in", font=hf, fill=GREY)
    img.save(path, "JPEG", quality=92)


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    n = len(spec["slides"])
    for i, s in enumerate(spec["slides"], 1):
        p = f"{spec['out_prefix']}{i}.jpg"; slide(s, i, n, p); print(p)
