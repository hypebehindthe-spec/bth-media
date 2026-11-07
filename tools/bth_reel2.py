"""Behind The Hype reel builder, v2 (default from post 004 v2 on).

Same spec format as bth_reel.py (out, voice, mood, seed, beats[{say, lines}], optional cuts), plus optional:
  "count": false on a beat  -> don't animate the first number on that beat
What v2 changes, for retention:
  - frame 1 is pure hook: no label, no slide counter, no progress bar (nothing that says "slideshow")
  - moving background (slow drifting warm glow) instead of a still card
  - every beat's lines pop in one by one; the first big number counts up
  - word-by-word captions of the voiceover in the lower third (current word in yellow),
    so people watching on mute keep watching
  - hard cuts between beats (punchier than cross-fades)
Usage: python3 tools/bth_reel2.py posts/post_NNN.json
"""
import json, math, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bth_music  # noqa: E402
from bth_reel import FONTS, FD, W, H, M, INK, YEL, WHITE, GREY, wrap, segments, cap_size  # noqa: E402
from scipy.io import wavfile  # noqa: E402

FPS = 30
TOP = 330            # text block never starts above this (Instagram's top UI)
CAP_Y = 1330         # caption band centre; Instagram's caption/buttons cover roughly y > 1500
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def make_glow():
    yy, xx = np.mgrid[0:900, 0:900] - 449.5
    g = np.exp(-(xx ** 2 + yy ** 2) / (2 * 150.0 ** 2))
    g = np.clip((g - g[0, 449]) / (1 - g[0, 449]), 0, 1)  # exactly 0 at the box edge
    return Image.fromarray((g * 255).astype(np.uint8), "L")


GLOW = make_glow()
BLOBS = [(Image.new("RGB", (900, 900), col), GLOW.point(lambda v, a=alpha: int(v * a)), ph, cx, cy, r)
         for col, alpha, ph, cx, cy, r in ((YEL, 0.10, 0.0, 0.25, 0.30, 0.18), ((60, 90, 160), 0.16, 2.1, 0.75, 0.72, 0.16))]


def background(t):
    """Dark card with two slow drifting glows (yellow and cool blue), very low intensity."""
    base = Image.new("RGB", (W, H), INK)
    for layer, mask, ph, cx, cy, r in BLOBS:
        x = int(W * (cx + r * math.sin(t * 0.21 + ph)) - 450)
        y = int(H * (cy + r * 0.6 * math.cos(t * 0.17 + ph)) - 450)
        base.paste(layer, (x, y), mask)
    return base


def fmt_like(template, value):
    """Format value the way the template number is written (decimals, Indian or western commas)."""
    dec = len(template.split(".")[1]) if "." in template else 0
    s = f"{value:.{dec}f}"
    if "," not in template:
        return s
    ip, _, fp = s.partition(".")
    if re.search(r"\d,\d\d,\d{3}", template):  # Indian grouping 1,48,800
        head, tail = ip[:-3], ip[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        ip = ",".join(groups + [tail]) if groups else tail
    else:
        ip = f"{int(ip):,}"
    return ip + ("." + fp if fp else "")


def layout(beat):
    """Return a list of (text, font, colour, y) for the beat's lines, centred vertically in the safe band."""
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    rows = []
    for text, style in beat["lines"]:
        fp, size, col = FONTS[style]
        f = ImageFont.truetype(fp, size)
        for ln in wrap(d, text, f, W - 2 * M):
            rows.append([ln, f, col, int(size * 1.2)])
        rows.append([None, None, None, int(size * 0.35)])
    rows = rows[:-1]
    th = sum(r[3] for r in rows)
    y = max(TOP, (CAP_Y - 170 - th) // 2 + 140)
    out = []
    for ln, f, col, lh in rows:
        if ln:
            out.append((ln, f, col, y))
        y += lh
    return out


def pauses(voice):
    log = subprocess.run(["ffmpeg", "-i", voice, "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(st, en))


def spread(words, a, b):
    wts = [len(re.sub(r"[^\w]", "", w)) + 2 for w in words]
    t, out = a, []
    for w, k in zip(words, wts):
        dt = (b - a) * k / sum(wts)
        out.append((w, t, t + dt))
        t += dt
    return out


def word_times(say, start, end, sil):
    """Time the beat's words: speech regions come from the pauses inside the segment; if the number of
    phrase breaks (, . ? !) matches the number of regions, each phrase gets its own region."""
    words = say.split()
    inner = [(a, b) for a, b in sil if a > start + 0.1 and b < end - 0.1]
    regions, t = [], start
    for a, b in inner:
        regions.append((t, a))
        t = b
    regions.append((t, end))
    regions = [(max(a, start + 0.03), b) for a, b in regions if b - a > 0.15]
    phrases, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.,?!]$", w):
            phrases.append(cur)
            cur = []
    if cur:
        phrases.append(cur)
    if len(phrases) == len(regions):
        out = []
        for ph, (a, b) in zip(phrases, regions):
            out += spread(ph, a, b)
        return out
    # otherwise spread over speech time only, skipping the pauses
    total = sum(b - a for a, b in regions)
    wts = [len(re.sub(r"[^\w]", "", w)) + 2 for w in words]
    out, acc, ri, used = [], 0.0, 0, 0.0
    def at(x):
        for a, b in regions:
            if x <= b - a:
                return a + x
            x -= b - a
        return regions[-1][1]
    for w, k in zip(words, wts):
        dt = total * k / sum(wts)
        out.append((w, at(acc), at(acc + dt)))
        acc += dt
    return out


def chunks(timed, n=3):
    """Group words into caption chunks of up to n words, breaking after punctuation."""
    out, cur = [], []
    for item in timed:
        cur.append(item)
        if len(cur) >= n or re.search(r"[.?!,]$", item[0]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


CAP_F = ImageFont.truetype(FD + "Poppins-Bold.ttf", 58)
HANDLE_F = ImageFont.truetype(FD + "Poppins-Medium.ttf", 34)


def draw_caption(img, chunk, t):
    d = ImageDraw.Draw(img)
    words = [w for w, _, _ in chunk]
    text = " ".join(words)
    tw = d.textlength(text, font=CAP_F)
    if tw > W - 2 * M:
        f = ImageFont.truetype(FD + "Poppins-Bold.ttf", int(58 * (W - 2 * M) / tw))
    else:
        f = CAP_F
    tw = d.textlength(text, font=f)
    x = (W - tw) / 2
    pad = 22
    bh = f.size + 30
    box = Image.new("RGBA", (int(tw + 2 * pad), bh), (0, 0, 0, 150))
    img.paste(box, (int(x - pad), int(CAP_Y - bh / 2)), box)
    for w, a, b in chunk:
        col = YEL if a <= t < b else WHITE
        d.text((x, CAP_Y - f.size / 2 - 8), w, font=f, fill=col)
        x += d.textlength(w + " ", font=f)


def render_beat_frame(beat, rows, t_in, idx):
    """rows drawn with staggered pop-in; first big number counts up on its first appearance."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    counted = False
    for k, (ln, f, col, y) in enumerate(rows):
        p = 1.0 if idx == 1 else ease((t_in - 0.10 * k) / 0.28)
        if p <= 0:
            continue
        text = ln
        if (not counted and col == YEL and f.size >= 90 and beat.get("count", True)
                and idx > 1 and NUM.search(ln) and t_in < 1.2):
            m = NUM.search(ln)
            target = float(m.group().replace(",", ""))
            cp = ease((t_in - 0.10 * k) / 0.75)
            text = ln[:m.start()] + fmt_like(m.group(), target * cp) + ln[m.end():]
        if not counted and col == YEL and f.size >= 90:
            counted = True
        a = int(255 * p)
        dy = int(36 * (1 - p))
        d.text((M, y + dy), text, font=f, fill=col + (a,))
    if idx > 1:  # small handle on everything except the hook frame
        h = "@behind.the.hype.in"
        d.text(((W - d.textlength(h, font=HANDLE_F)) / 2, 190), h, font=HANDLE_F, fill=GREY + (200,))
    return layer


def build(spec_path):
    spec = json.load(open(spec_path))
    root = os.path.dirname(HERE)
    voice = os.path.join(root, spec["voice"])
    out = os.path.join(root, spec["out"])
    beats = spec["beats"]
    segs, dur = segments(voice, beats, spec.get("cuts"))
    starts = np.cumsum([0] + segs[:-1])
    layouts = [layout(b) for b in beats]
    caps, sil = [], pauses(voice)
    for b, s0, s in zip(beats, starts, segs):
        caps += chunks(word_times(b["say"], s0, s0 + s, sil))
    tmp = tempfile.mkdtemp()
    video = f"{tmp}/video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                            "-pix_fmt", "yuv420p", video], stdin=subprocess.PIPE)
    nframes = int(math.ceil(dur * FPS))
    bi, ci = 0, 0
    for fi in range(nframes):
        t = fi / FPS
        while bi < len(beats) - 1 and t >= starts[bi + 1]:
            bi += 1
        img = background(t)
        layer = render_beat_frame(beats[bi], layouts[bi], t - starts[bi], bi + 1)
        img.paste(layer, (0, 0), layer)
        while ci < len(caps) - 1 and t >= caps[ci][-1][2]:
            ci += 1
        if caps[ci][0][1] - 0.05 <= t:
            draw_caption(img, caps[ci], t)
        enc.stdin.write(img.tobytes())
    enc.stdin.close()
    enc.wait()
    # music + mix (same as v1)
    music = f"{tmp}/music.wav"
    wavfile.write(music, bth_music.SR, bth_music.build(spec.get("mood", "drive"), dur + 0.8, int(spec.get("seed", 7))))
    vnorm = f"{tmp}/voice_norm.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                    "-ac", "2", "-ar", "48000", vnorm], check=True)
    mix = (f"[0:a]asplit=2[vo][sc];"
           f"[1:a]volume=0.20[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[md];"
           f"[vo][md]amix=inputs=2:duration=longest:normalize=0,atrim=0:{dur:.3f},afade=t=out:st={max(0, dur - 0.6):.3f}:d=0.6[aout]")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vnorm, "-i", music, "-i", video, "-filter_complex", mix,
                    "-map", "2:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
                    "-ac", "2", "-movflags", "+faststart", "-shortest", out], check=True)
    cap_size(out)
    print(json.dumps({"out": out, "duration": round(dur, 2), "segments": [round(s, 2) for s in segs],
                      "bytes": os.path.getsize(out)}))


if __name__ == "__main__":
    build(sys.argv[1])
