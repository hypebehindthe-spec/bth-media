"""Behind The Hype reel builder, v3 "illustrated" (A/B test from 9 Nov 2026, owner approved a 3-reel test).

Same spec as v2 (out, voice, mood, seed, cuts, beats[{say, lines}]) plus, per beat:
  "art": list of up to 3 illustrations, biggest first. Each item is an emoji ("🏭") or "coin:₹" / "coin:%"
         (a drawn coin with that symbol; use it instead of money emoji, which show dollar signs).
  "bg":  optional background colour name: sun, sky, mint, coral, lilac (otherwise rotates by beat).
What v3 changes vs v2:
  - bright colour backgrounds with a soft spotlight instead of a dark card
  - big colour illustrations (Google Noto Color Emoji, open licence) in the top half, popping in with a bounce
    and bobbing gently; the hook frame shows everything at once (it is the Instagram cover)
  - the first line becomes a dark "kicker" pill if its style is "Y" or "W" and it is short; big lines get a
    dark outline so they read on any colour
  - sound effects: a whoosh on every cut, a pop when each illustration lands, a tick when a number finishes
    counting (all synthesised here, no downloads)
Captions, word timing, count-up, music and size cap are reused from v2.
Usage: python3 tools/bth_reel3.py posts/post_NNN.json
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bth_music  # noqa: E402
from bth_reel import FD, W, H, M, INK, YEL, WHITE, wrap, segments, cap_size  # noqa: E402
from bth_reel2 import FPS, NUM, ease, fmt_like, pauses, word_times, chunks  # noqa: E402
from scipy.io import wavfile  # noqa: E402

EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
PALETTE = {"sun": (255, 214, 102), "sky": (125, 200, 255), "mint": (135, 222, 185),
           "coral": (255, 160, 140), "lilac": (196, 178, 255)}
ORDER = ["sun", "sky", "mint", "coral", "lilac"]
RED = (226, 54, 72)
CAP_Y = 1420
TEXT_TOP = 930
ART_C = (540, 640)
BOLD = FD + "Poppins-Bold.ttf"
SIZES = {"w": 112, "y": 112, "W": 70, "Y": 70, "s": 46, "g": 38}
CAP_F = ImageFont.truetype(BOLD, 58)
HANDLE_F = ImageFont.truetype(FD + "Poppins-Medium.ttf", 34)
_ef = ImageFont.truetype(EMOJI_FONT, 109)
_cache = {}


def ease_back(x):
    x = max(0.0, min(1.0, x))
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def art_image(item, size):
    key = (item, size)
    if key in _cache:
        return _cache[key]
    if item.startswith("coin:"):
        s = 400
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse((10, 22, s - 10, s - 2), fill=(196, 140, 20))
        d.ellipse((10, 10, s - 10, s - 14), fill=(255, 199, 44))
        d.ellipse((46, 44, s - 46, s - 48), outline=(214, 156, 24), width=10)
        f = ImageFont.truetype(BOLD, 210)
        sym = item[5:]
        tw = d.textlength(sym, font=f)
        d.text(((s - tw) / 2, 50), sym, font=f, fill=(150, 98, 8))
    else:
        im = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, 20), item, font=_ef, embedded_color=True)
        bb = im.getbbox()
        if not bb:
            raise SystemExit(f"Emoji not available in Noto Color Emoji: {item!r}")
        im = im.crop(bb)
    im = im.resize((size, max(1, int(size * im.height / im.width))), Image.LANCZOS)
    im.putalpha(im.getchannel("A").point(lambda v: 0 if v < 40 else v))  # drop the faint box some glyphs carry
    _cache[key] = im
    return im


def soft_shadow(im, blur, opacity):
    """Blurred drop shadow with room to fade out (an unpadded blur gets cut off at the image edge)."""
    pad = blur * 3
    sh = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", sh.size, 0)
    a.paste(im.getchannel("A").point(lambda v: int(v * opacity)), (pad, pad))
    sh.putalpha(a)
    return sh.filter(ImageFilter.GaussianBlur(blur)), pad


def art_slots(n):
    """(centre x, centre y, width) for 1-3 illustrations: main one centred, others smaller at the sides."""
    cx, cy = ART_C
    if n == 1:
        return [(cx, cy, 440)]
    if n == 2:
        return [(cx - 170, cy + 20, 380), (cx + 250, cy - 120, 230)]
    return [(cx, cy + 30, 400), (cx - 300, cy - 170, 210), (cx + 300, cy + 170, 210)]


def background(col, t):
    base = Image.new("RGB", (W, H), col)
    light = tuple(min(255, int(c + (255 - c) * 0.55)) for c in col)
    g = Image.new("L", (W // 4, H // 4), 0)
    ox = int(18 * math.sin(t * 0.4))
    ImageDraw.Draw(g).ellipse((20 + ox, 70, 250 + ox, 330), fill=200)
    g = g.filter(ImageFilter.GaussianBlur(40)).resize((W, H), Image.BILINEAR)
    return Image.composite(Image.new("RGB", (W, H), light), base, g)


def layout(beat, accent):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = list(beat["lines"])
    kicker = None
    if lines and lines[0][1] in ("Y", "W") and len(lines[0][0]) <= 26 and len(lines) > 1:
        kicker = lines.pop(0)[0].upper()
    avail = CAP_Y - 75 - TEXT_TOP
    scale = 1.0
    while True:  # shrink the whole block until it fits above the caption band
        rows = []
        for text, style in lines:
            size = int(SIZES[style] * scale)
            f = ImageFont.truetype(BOLD if style in "wyWYs" else FD + "Poppins-Medium.ttf", size)
            big = style in "wy"
            txt = text.upper() if big else text
            col = {"w": WHITE, "y": accent, "W": INK, "Y": INK, "s": INK, "g": (60, 64, 74)}[style]
            for ln in wrap(d, txt, f, W - 2 * M):
                rows.append([ln, f, col, int(size * 1.12), big])
            rows.append([None, None, None, int(size * 0.25), False])
        rows = rows[:-1]
        th = sum(r[3] for r in rows)
        if th <= avail or scale < 0.55:
            break
        scale -= 0.06
    y = TEXT_TOP + max(0, (CAP_Y - 90 - TEXT_TOP - th) // 2)
    out = []
    for ln, f, col, lh, big in rows:
        if ln:
            out.append((ln, f, col, y, big))
        y += lh
    return kicker, out


def draw_caption(img, chunk, t):
    d = ImageDraw.Draw(img)
    words = [w for w, _, _ in chunk]
    text = " ".join(words)
    tw = d.textlength(text, font=CAP_F)
    f = CAP_F if tw <= W - 2 * M else ImageFont.truetype(BOLD, int(58 * (W - 2 * M) / tw))
    tw = d.textlength(text, font=f)
    x = (W - tw) / 2
    pad, bh = 24, f.size + 30
    d.rounded_rectangle((x - pad, CAP_Y - bh / 2, x + tw + pad, CAP_Y + bh / 2), radius=18, fill=INK)
    for w, a, b in chunk:
        d.text((x, CAP_Y - f.size / 2 - 8), w, font=f, fill=YEL if a <= t < b else WHITE)
        x += d.textlength(w + " ", font=f)


def render(img, beat, kicker, rows, t_in, idx, accent):
    d = ImageDraw.Draw(img)
    hook = idx == 1
    # illustrations
    arts = beat.get("art", [])[:3]
    for k, (item, (cx, cy, size)) in enumerate(zip(arts, art_slots(len(arts)))):
        p = 1.0 if hook else ease_back((t_in - 0.08 - 0.12 * k) / 0.45)
        if p <= 0.01:
            continue
        s = max(8, int(size * max(0.05, p)))
        im = art_image(item, s)
        bob = int(10 * math.sin(t_in * 2.2 + k * 1.7))
        sh, pad = soft_shadow(im, 10, 0.22)
        x, y = cx - im.width // 2, cy - im.height // 2 + bob
        img.paste(sh, (x + 10 - pad, y + 18 - pad), sh)
        img.paste(im, (x, y), im)
    # kicker pill
    if kicker:
        f = ImageFont.truetype(BOLD, 46)
        tw = d.textlength(kicker, font=f)
        d.rounded_rectangle(((W - tw) / 2 - 32, 250, (W + tw) / 2 + 32, 328), radius=39, fill=INK)
        d.text(((W - tw) / 2, 259), kicker, font=f, fill=YEL)
    # text rows
    counted = False
    for k, (ln, f, col, y, big) in enumerate(rows):
        p = 1.0 if hook else ease((t_in - 0.25 - 0.10 * k) / 0.28)
        if p <= 0:
            continue
        text = ln
        if not counted and big and col != WHITE and beat.get("count", True) and not hook and NUM.search(ln) and t_in < 1.4:
            m = NUM.search(ln)
            cp = ease((t_in - 0.25 - 0.10 * k) / 0.75)
            text = ln[:m.start()] + fmt_like(m.group(), float(m.group().replace(",", "")) * cp) + ln[m.end():]
        if big and col != WHITE:
            counted = True
        tw = d.textlength(text, font=f)
        x = (W - tw) / 2
        yy = y + int(30 * (1 - p))
        if big:
            d.text((x, yy), text, font=f, fill=col, stroke_width=10, stroke_fill=INK)
        else:
            d.text((x, yy), text, font=f, fill=col)
    if not hook:
        h = "@behind.the.hype.in"
        d.text(((W - d.textlength(h, font=HANDLE_F)) / 2, 190), h, font=HANDLE_F, fill=(40, 44, 52))


# ---------- sound effects (synthesised) ----------
SR = 48000


def _env(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def whoosh(rng):
    n = int(0.38 * SR)
    noise = rng.standard_normal(n)
    # sweep a simple one-pole low-pass from dark to bright and back
    cut = np.concatenate([np.linspace(0.02, 0.35, n // 2), np.linspace(0.35, 0.05, n - n // 2)])
    out, y = np.zeros(n), 0.0
    for i in range(n):
        y += cut[i] * (noise[i] - y)
        out[i] = y
    return out * _env(n, 0.15, 0.2) * 0.9


def pop(freq=520):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = freq * (1 + 1.4 * np.exp(-t * 45))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 32) * 0.7


def tick():
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1760 * t) + 0.5 * np.sin(2 * np.pi * 2640 * t)) * np.exp(-t * 22) * 0.35


def sfx_track(beats, starts, dur, seed):
    rng = np.random.default_rng(seed)
    track = np.zeros(int((dur + 1) * SR))

    def add(sig, at):
        i = int(at * SR)
        j = min(len(track), i + len(sig))
        if 0 <= i < len(track):
            track[i:j] += sig[: j - i]
    for bi, (b, s0) in enumerate(zip(beats, starts)):
        if bi > 0:
            add(whoosh(rng), max(0, s0 - 0.12))
            for k in range(len(b.get("art", [])[:3])):
                add(pop(480 + 90 * k), s0 + 0.08 + 0.12 * k + 0.18)
            if b.get("count", True) and any(st in "y" and NUM.search(tx) for tx, st in b["lines"]):
                add(tick(), s0 + 1.0)
    track = track[: int(dur * SR)]
    return np.clip(track * 0.5, -1, 1)


def build(spec_path):
    spec = json.load(open(spec_path))
    root = os.path.dirname(HERE)
    voice = os.path.join(root, spec["voice"])
    out = os.path.join(root, spec["out"])
    beats = spec["beats"]
    segs, dur = segments(voice, beats, spec.get("cuts"))
    starts = np.cumsum([0] + segs[:-1])
    cols, accents, lays = [], [], []
    for i, b in enumerate(beats):
        name = b.get("bg") or ORDER[i % len(ORDER)]
        cols.append(PALETTE[name])
        accents.append(RED if name == "sun" else YEL)
        lays.append(layout(b, accents[-1]))
    caps, sil = [], pauses(voice)
    for b, s0, s in zip(beats, starts, segs):
        caps += chunks(word_times(b["say"], s0, s0 + s, sil))
    tmp = tempfile.mkdtemp()
    video = f"{tmp}/video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                            "-pix_fmt", "yuv420p", video], stdin=subprocess.PIPE)
    bi, ci = 0, 0
    for fi in range(int(math.ceil(dur * FPS))):
        t = fi / FPS
        while bi < len(beats) - 1 and t >= starts[bi + 1]:
            bi += 1
        img = background(cols[bi], t)
        kicker, rows = lays[bi]
        render(img, beats[bi], kicker, rows, t - starts[bi], bi + 1, accents[bi])
        while ci < len(caps) - 1 and t >= caps[ci][-1][2]:
            ci += 1
        if caps[ci][0][1] - 0.05 <= t:
            draw_caption(img, caps[ci], t)
        enc.stdin.write(img.tobytes())
    enc.stdin.close()
    enc.wait()
    music = f"{tmp}/music.wav"
    wavfile.write(music, bth_music.SR, bth_music.build(spec.get("mood", "drive"), dur + 0.8, int(spec.get("seed", 7))))
    sfx = f"{tmp}/sfx.wav"
    wavfile.write(sfx, SR, (sfx_track(beats, starts, dur, int(spec.get("seed", 7))) * 32767).astype(np.int16))
    vnorm = f"{tmp}/voice_norm.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                    "-ac", "2", "-ar", "48000", vnorm], check=True)
    mix = (f"[0:a]asplit=2[vo][sc];"
           f"[1:a]volume=0.18[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[md];"
           f"[2:a]aformat=channel_layouts=stereo,volume=0.55[fx];"
           f"[vo][md][fx]amix=inputs=3:duration=first:normalize=0,atrim=0:{dur:.3f},"
           f"afade=t=out:st={max(0, dur - 0.6):.3f}:d=0.6[aout]")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vnorm, "-i", music, "-i", sfx, "-i", video,
                    "-filter_complex", mix, "-map", "3:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-shortest", out], check=True)
    cap_size(out)
    print(json.dumps({"out": out, "duration": round(dur, 2), "segments": [round(s, 2) for s in segs],
                      "bytes": os.path.getsize(out)}))


if __name__ == "__main__":
    build(sys.argv[1])
