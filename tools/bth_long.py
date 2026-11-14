"""Behind The Hype long video builder (16:9, 1920x1080), for the weekly YouTube story video.

Usage: python3 tools/bth_long.py long/long_NNN.json   -> long/long_NNN.mp4, .srt, _chapters.txt
Spec:
{
 "out": "long/long_001.mp4",
 "title_bar": {"brand": "BEHIND THE HYPE", "line1": "HE TOOK ON HUL", "line2": "WITH A BICYCLE", "sub": "Nirma · Gujarat · 1969"},
 "mood": "chill", "seed": 101,
 "sections": [ {"chapter": "The chemist", "bg": "mint", "voice": "audio/x_s2.wav",
                "beats": [{"say": "...", "lines": [[text, style], ...], "art": ["🚲", "coin:₹"], "circle": 0, "count": false}]} ]
}
Each section is voiced separately (Gemini takes over ~90 s fail) and joined with a short gap.
Look (from what works for ZeroInOn and our illustrated test):
  - opening section: a dark title bar across the top (brand, two-line headline white + yellow, grey subtitle),
    the hook visible from frame 0 so it also works as the thumbnail moment
  - bright colour scene per chapter, big illustrations on the right that bounce in and drift, text on the left
  - "circle": index of an illustration to ring with a hand-drawn red circle that draws itself in
  - chapter pill top-left, word-by-word captions at the bottom, count-up on big yellow numbers
  - whoosh on cuts, pop when art lands, tick when a number lands, music ducked under the voice
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bth_music  # noqa: E402
from bth_reel import FD, INK, YEL, WHITE, wrap, segments  # noqa: E402
from bth_reel2 import NUM, ease, fmt_like, pauses, word_times, chunks  # noqa: E402
from bth_reel3 import art_image, soft_shadow, ease_back, PALETTE, ORDER, RED, whoosh, pop, tick, SR  # noqa: E402
from scipy.io import wavfile  # noqa: E402

W, H, FPS = 1920, 1080, 25
GAP = 0.6                      # silence between voiced sections
BOLD = FD + "Poppins-Bold.ttf"
MED = FD + "Poppins-Medium.ttf"
SIZES = {"w": 104, "y": 104, "W": 64, "Y": 64, "s": 44, "g": 36}
CAP_Y = 980
TEXT_X, TEXT_W = 150, 860
ART_C = (1400, 560)
GREY = (60, 64, 74)
HOOK_RED = (226, 54, 72)
_font = {}


def F(path, size):
    k = (path, size)
    if k not in _font:
        _font[k] = ImageFont.truetype(path, size)
    return _font[k]


def bg_frame(col, t):
    base = Image.new("RGB", (W, H), col)
    light = tuple(min(255, int(c + (255 - c) * 0.55)) for c in col)
    g = Image.new("L", (W // 4, H // 4), 0)
    ox = int(30 * math.sin(t * 0.25))
    ImageDraw.Draw(g).ellipse((230 + ox, 10, 470 + ox, 250), fill=200)
    g = g.filter(ImageFilter.GaussianBlur(45)).resize((W, H), Image.BILINEAR)
    return Image.composite(Image.new("RGB", (W, H), light), base, g)


def art_slots(n):
    cx, cy = ART_C
    if n == 1:
        return [(cx, cy, 480)]
    if n == 2:
        return [(cx - 120, cy + 40, 420), (cx + 280, cy - 210, 250)]
    return [(cx, cy + 60, 380), (cx - 300, cy - 200, 230), (cx + 300, cy - 160, 230)]


def layout(beat, accent, top):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    avail = CAP_Y - 90 - top
    scale = 1.0
    while True:
        rows = []
        for text, style in beat["lines"]:
            size = int(SIZES[style] * scale)
            f = F(BOLD if style in "wyWYs" else MED, size)
            big = style in "wy"
            txt = text.upper() if big else text
            col = {"w": WHITE, "y": accent, "W": INK, "Y": INK, "s": INK, "g": GREY}[style]
            for ln in wrap(d, txt, f, TEXT_W):
                rows.append([ln, f, col, int(size * 1.12), big])
            rows.append([None, None, None, int(size * 0.25), False])
        rows = rows[:-1]
        th = sum(r[3] for r in rows)
        if th <= avail or scale < 0.55:
            break
        scale -= 0.06
    y = top + max(0, (avail - th) // 2)
    out = []
    for ln, f, col, lh, big in rows:
        if ln:
            out.append((ln, f, col, y, big))
        y += lh
    return out


def draw_circle(img, cx, cy, rw, rh, p):
    """Hand-drawn red ellipse that draws itself (p 0..1), slightly tilted and overshooting."""
    if p <= 0:
        return
    d = ImageDraw.Draw(img)
    n = 90
    pts = []
    for i in range(int(n * min(1, p) * 1.08) + 1):
        a = -math.pi * 0.6 + 2 * math.pi * 1.08 * i / n
        wob = 1 + 0.035 * math.sin(3 * a)
        x = cx + rw * wob * math.cos(a) * math.cos(-0.12) - rh * wob * math.sin(a) * math.sin(-0.12)
        y = cy + rw * wob * math.cos(a) * math.sin(-0.12) + rh * wob * math.sin(a) * math.cos(-0.12)
        pts.append((x, y))
    if len(pts) > 1:
        d.line(pts, fill=HOOK_RED, width=14, joint="curve")


def draw_title_bar(img, tb):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 262), fill=(20, 22, 28))
    bf = F(BOLD, 30)
    d.text((70, 30), tb.get("brand", "BEHIND THE HYPE"), font=bf, fill=YEL)
    f1 = F(BOLD, 74)
    for i, (txt, col) in enumerate([(tb["line1"], WHITE), (tb["line2"], YEL)]):
        tw = d.textlength(txt, font=f1)
        d.text(((W - tw) / 2, 40 + i * 80), txt, font=f1, fill=col, stroke_width=4, stroke_fill=(0, 0, 0))
    sf = F(MED, 30)
    st = tb.get("sub", "")
    d.text(((W - d.textlength(st, font=sf)) / 2, 214), st, font=sf, fill=(200, 200, 205))


def draw_caption(img, chunk, t):
    d = ImageDraw.Draw(img)
    words = [w for w, _, _ in chunk]
    f = F(BOLD, 52)
    text = " ".join(words)
    tw = d.textlength(text, font=f)
    if tw > W - 300:
        f = F(BOLD, int(52 * (W - 300) / tw))
        tw = d.textlength(text, font=f)
    x = (W - tw) / 2
    bh = f.size + 28
    d.rounded_rectangle((x - 24, CAP_Y - bh / 2, x + tw + 24, CAP_Y + bh / 2), radius=16, fill=INK)
    for w, a, b in chunk:
        d.text((x, CAP_Y - f.size / 2 - 8), w, font=f, fill=YEL if a <= t < b else WHITE)
        x += d.textlength(w + " ", font=f)


def render(img, beat, rows, t_in, first, accent, chapter, hook):
    d = ImageDraw.Draw(img)
    arts = beat.get("art", [])[:3]
    slots = art_slots(len(arts))
    if hook:
        slots = [(x, y + 90, int(s * 0.85)) for x, y, s in slots]
    for k, (item, (cx, cy, size)) in enumerate(zip(arts, slots)):
        p = 1.0 if first else ease_back((t_in - 0.1 - 0.15 * k) / 0.5)
        if p <= 0.01:
            continue
        drift = 1 + 0.03 * math.sin(t_in * 0.6 + k)
        s = max(8, int(size * max(0.05, p) * drift))
        im = art_image(item, s)
        bob = int(12 * math.sin(t_in * 1.8 + k * 1.7))
        sh, pad = soft_shadow(im, 12, 0.22)
        x, y = cx - im.width // 2, cy - im.height // 2 + bob
        img.paste(sh, (x + 12 - pad, y + 20 - pad), sh)
        img.paste(im, (x, y), im)
        if beat.get("circle") == k:
            cp = 1.0 if first else ease((t_in - 0.9) / 0.6)
            draw_circle(img, cx, cy + bob, im.width * 0.62, im.height * 0.62, cp)
    if not hook:
        pf = F(BOLD, 34)
        ct = chapter.upper()
        tw = d.textlength(ct, font=pf)
        d.rounded_rectangle((70, 50, 70 + tw + 56, 112), radius=31, fill=INK)
        d.text((98, 58), ct, font=pf, fill=YEL)
        hf = F(MED, 28)
        h = "BEHIND THE HYPE"
        d.text((W - 70 - d.textlength(h, font=hf), 66), h, font=hf, fill=(40, 44, 52))
    counted = False
    for k, (ln, f, col, y, big) in enumerate(rows):
        p = 1.0 if first else ease((t_in - 0.3 - 0.12 * k) / 0.3)
        if p <= 0:
            continue
        text = ln
        if (not counted and big and col != WHITE and beat.get("count", True) and not first
                and NUM.search(ln) and t_in < 1.6):
            m = NUM.search(ln)
            cp = ease((t_in - 0.3 - 0.12 * k) / 0.8)
            text = ln[:m.start()] + fmt_like(m.group(), float(m.group().replace(",", "")) * cp) + ln[m.end():]
        if big and col != WHITE:
            counted = True
        xx = TEXT_X - int(40 * (1 - p))
        if big:
            d.text((xx, y), text, font=f, fill=col, stroke_width=9, stroke_fill=INK)
        else:
            d.text((xx, y), text, font=f, fill=col)


def fmt_ts(x, srt=True):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    if srt:
        return f"{h:02}:{m:02}:{int(s):02},{int(round(s % 1 * 1000)) % 1000:03}"
    return f"{m}:{int(s):02}"


def build(spec_path):
    spec = json.load(open(spec_path))
    root = os.path.dirname(HERE)
    out = os.path.join(root, spec["out"])
    tmp = tempfile.mkdtemp()
    # 1. voice: normalise each section, measure, join with gaps
    timeline, voice_parts, t0, chapters = [], [], 0.0, []
    for si, sec in enumerate(spec["sections"]):
        v = os.path.join(root, sec["voice"])
        segs, dur = segments(v, sec["beats"], sec.get("cuts"))
        sil = [(a + t0, b + t0) for a, b in pauses(v)]
        chapters.append((t0, sec["chapter"]))
        s0 = t0
        for bi, (b, s) in enumerate(zip(sec["beats"], segs)):
            end = s0 + s + (GAP if bi == len(segs) - 1 and si < len(spec["sections"]) - 1 else 0)
            timeline.append(dict(sec=si, beat=b, start=s0, end=end, first=(si == 0 and bi == 0),
                                 words=word_times(b["say"], s0, s0 + s, sil)))
            s0 += s
        n = f"{tmp}/v{si}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                        "-ac", "2", "-ar", "48000", n], check=True)
        voice_parts.append(n)
        t0 += dur + (GAP if si < len(spec["sections"]) - 1 else 0)
    total = t0 + 1.2
    # join voice with gaps
    lst = f"{tmp}/list.txt"
    silence = f"{tmp}/gap.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(GAP), silence], check=True)
    with open(lst, "w") as f:
        for i, p in enumerate(voice_parts):
            f.write(f"file '{p}'\n")
            if i < len(voice_parts) - 1:
                f.write(f"file '{silence}'\n")
    voice = f"{tmp}/voice.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", voice], check=True)
    # 2. captions
    caps = []
    for e in timeline:
        caps += chunks(e["words"], 4)
    # 3. frames
    cols = [PALETTE[s.get("bg") or ORDER[i % len(ORDER)]] for i, s in enumerate(spec["sections"])]
    accents = [RED if (s.get("bg") or ORDER[i % len(ORDER)]) == "sun" else YEL for i, s in enumerate(spec["sections"])]
    lays = []
    for e in timeline:
        hook = e["sec"] == 0
        lays.append(layout(e["beat"], accents[e["sec"]], 330 if hook else 170))
    video = f"{tmp}/video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                            "-pix_fmt", "yuv420p", video], stdin=subprocess.PIPE)
    bi, ci = 0, 0
    for fi in range(int(math.ceil(total * FPS))):
        t = fi / FPS
        while bi < len(timeline) - 1 and t >= timeline[bi + 1]["start"]:
            bi += 1
        e = timeline[bi]
        hook = e["sec"] == 0
        img = bg_frame(cols[e["sec"]], t)
        render(img, e["beat"], lays[bi], t - e["start"], e["first"], accents[e["sec"]],
               spec["sections"][e["sec"]]["chapter"], hook)
        if hook:
            draw_title_bar(img, spec["title_bar"])
        while ci < len(caps) - 1 and t >= caps[ci][-1][2]:
            ci += 1
        if caps and caps[ci][0][1] - 0.05 <= t <= caps[ci][-1][2] + 0.4:
            draw_caption(img, caps[ci], t)
        enc.stdin.write(img.tobytes())
    enc.stdin.close()
    enc.wait()
    # 4. music + sfx + mix
    music = f"{tmp}/music.wav"
    wavfile.write(music, bth_music.SR, bth_music.build(spec.get("mood", "chill"), total + 1, int(spec.get("seed", 7))))
    rng = np.random.default_rng(int(spec.get("seed", 7)))
    track = np.zeros(int((total + 1) * SR))

    def add(sig, at):
        i = int(at * SR)
        j = min(len(track), i + len(sig))
        if 0 <= i < len(track):
            track[i:j] += sig[: j - i]
    for e in timeline:
        if not e["first"]:
            add(whoosh(rng), max(0, e["start"] - 0.12))
            for k in range(len(e["beat"].get("art", [])[:3])):
                add(pop(480 + 90 * k), e["start"] + 0.28 + 0.15 * k)
        if e["beat"].get("circle") is not None:
            add(whoosh(rng) * 0.5, e["start"] + 0.9)
        if e["beat"].get("count", True) and any(st == "y" and NUM.search(tx) for tx, st in e["beat"]["lines"]):
            add(tick(), e["start"] + 1.1)
    sfx = f"{tmp}/sfx.wav"
    wavfile.write(sfx, SR, (np.clip(track * 0.5, -1, 1) * 32767).astype(np.int16))
    mix = (f"[0:a]asplit=2[vo][sc];"
           f"[1:a]volume=0.16[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
           f"[2:a]aformat=channel_layouts=stereo,volume=0.5[fx];"
           f"[vo]apad=whole_dur={total:.3f}[vp];"
           f"[vp][md][fx]amix=inputs=3:duration=first:normalize=0,atrim=0:{total:.3f},"
           f"afade=t=out:st={max(0, total - 1.2):.3f}:d=1.2[aout]")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", music, "-i", sfx, "-i", video,
                    "-filter_complex", mix, "-map", "3:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-shortest", out], check=True)
    # 5. subtitles + chapters
    base = os.path.splitext(out)[0]
    with open(base + ".srt", "w") as f:
        for i, c in enumerate(caps, 1):
            f.write(f"{i}\n{fmt_ts(c[0][1])} --> {fmt_ts(c[-1][2])}\n{' '.join(w for w, _, _ in c)}\n\n")
    with open(base + "_chapters.txt", "w") as f:
        for a, name in chapters:
            f.write(f"{fmt_ts(a, False)} {name}\n")
    print(json.dumps({"out": out, "duration": round(total, 1), "bytes": os.path.getsize(out),
                      "chapters": [(fmt_ts(a, False), n) for a, n in chapters]}, ensure_ascii=False))


if __name__ == "__main__":
    build(sys.argv[1])
