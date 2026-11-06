"""Build a Behind The Hype reel: frames + voiceover + original music.

Usage: python3 bth_reel.py spec.json
spec.json:
{
  "out": "posts/post_002_v2.mp4",
  "voice": "audio/post_002_vo_v2.wav",
  "mood": "drive", "seed": 2,
  "beats": [
    {"say": "spoken line", "lines": [["Headline part", "w"], ["highlight", "y"], ["small grey text", "g"]]},
    ...
  ]
}
Line styles: "w" big white, "y" big yellow, "W" medium white, "Y" medium yellow, "g" small grey, "s" small white.
"""
import json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bth_music  # noqa: E402
from scipy.io import wavfile  # noqa: E402

FD = "/usr/share/fonts/truetype/google-fonts/"
INK, YEL, WHITE, GREY = (14, 17, 22), (255, 199, 44), (245, 245, 240), (150, 155, 165)
W, H, M = 1080, 1920, 90
FONTS = {
    "w": (FD + "Poppins-Bold.ttf", 96, WHITE), "y": (FD + "Poppins-Bold.ttf", 96, YEL),
    "W": (FD + "Poppins-Bold.ttf", 68, WHITE), "Y": (FD + "Poppins-Bold.ttf", 68, YEL),
    "g": (FD + "Poppins-Medium.ttf", 46, GREY), "s": (FD + "Poppins-Medium.ttf", 46, WHITE),
}


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_frame(beat, idx, total, path):
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    lab = ImageFont.truetype(FD + "Poppins-Bold.ttf", 40)
    d.text((M, 150), "BEHIND THE HYPE", font=lab, fill=YEL)
    d.rectangle((M, 212, M + 130, 218), fill=YEL)
    cnt = f"{idx:02d}/{total:02d}"
    d.text((W - M - d.textlength(cnt, font=lab), 150), cnt, font=lab, fill=GREY)
    blocks = []
    for text, style in beat["lines"]:
        fp, size, col = FONTS[style]
        f = ImageFont.truetype(fp, size)
        for ln in wrap(d, text, f, W - 2 * M):
            blocks.append((ln, f, col, int(size * 1.2)))
        blocks.append((None, None, None, int(size * 0.35)))
    blocks = blocks[:-1]
    th = sum(b[3] for b in blocks)
    y = max(300, (H - th) // 2 - 60)
    for ln, f, col, lh in blocks:
        if ln:
            d.text((M, y), ln, font=f, fill=col)
        y += lh
    h = ImageFont.truetype(FD + "Poppins-Medium.ttf", 40)
    handle = "@behind.the.hype.in"
    d.text(((W - d.textlength(handle, font=h)) / 2, H - 260), handle, font=h, fill=WHITE)
    img.save(path)


def segments(voice, beats):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", voice]).decode().strip())
    log = subprocess.run(["ffmpeg", "-i", voice, "-af", "silencedetect=noise=-35dB:d=0.2", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    # merge pauses that touch, then keep (midpoint, length)
    raw = sorted(zip(starts, ends))
    merged = []
    for a, b in raw:
        if merged and a - merged[-1][1] < 0.05:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    sil = [((a + b) / 2, b - a) for a, b in merged if 0.5 < a < dur - 0.5]
    words = [max(1, len(b["say"].split())) for b in beats]
    rate = dur / sum(words)
    exp = [w * rate for w in words]
    k, m = len(beats) - 1, len(sil)
    cuts = None
    if m >= k:
        # choose k pauses in order; each segment should last about as long as its words suggest,
        # and longer pauses (paragraph breaks) are preferred
        INF = float("inf")
        pts = [(0.0, 0.0)] + sil
        best = [[INF] * (m + 1) for _ in range(k + 1)]
        back = [[-1] * (m + 1) for _ in range(k + 1)]
        best[0][0] = 0.0
        for j in range(1, k + 1):
            for i in range(1, m + 1):
                for q in range(0, i):
                    if best[j - 1][q] == INF:
                        continue
                    seg = pts[i][0] - pts[q][0]
                    c = best[j - 1][q] + abs(seg - exp[j - 1]) / exp[j - 1] - 2.5 * pts[i][1]
                    if c < best[j][i]:
                        best[j][i], back[j][i] = c, q
        tail = lambda i: abs((dur - pts[i][0]) - exp[-1]) / exp[-1]
        i = min(range(1, m + 1), key=lambda x: best[k][x] + tail(x) if best[k][x] < INF else INF)
        if best[k][i] < INF:
            picked = []
            for j in range(k, 0, -1):
                picked.append(pts[i][0])
                i = back[j][i]
            cuts = picked[::-1]
    if cuts is None:
        acc, cuts = 0, []
        for w in words[:-1]:
            acc += w
            cuts.append(dur * acc / sum(words))
    edges = [0.0] + cuts + [dur]
    return [edges[i + 1] - edges[i] for i in range(len(beats))], dur


def build(spec_path):
    spec = json.load(open(spec_path))
    root = os.path.dirname(HERE)
    voice = os.path.join(root, spec["voice"])
    out = os.path.join(root, spec["out"])
    beats = spec["beats"]
    tmp = tempfile.mkdtemp()
    for i, b in enumerate(beats, 1):
        render_frame(b, i, len(beats), f"{tmp}/f{i:02d}.png")
    segs, dur = segments(voice, beats)
    XF = 0.25
    # per-beat clips with a slow push-in
    clips = []
    for i, s in enumerate(segs, 1):
        L = s + (XF if i < len(segs) else 0) + 0.05
        n = int(L * 30) + 1
        c = f"{tmp}/c{i:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", f"{tmp}/f{i:02d}.png", "-t", f"{L:.3f}",
                        "-vf", f"scale=2160:3840,zoompan=z='1+0.04*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "30", c], check=True)
        clips.append(c)
    # chain cross-fades
    inputs, fc, prev, off = [], [], "0:v", 0.0
    for c in clips:
        inputs += ["-i", c]
    for i in range(1, len(clips)):
        off += segs[i - 1]
        lab = f"v{i}"
        fc.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={XF}:offset={off - XF / 2:.3f}[{lab}]")
        prev = lab
    fc.append(f"color=c=0xFFC72C:s=1080x18:r=30:d={dur + 1:.3f}[bar];"
              f"[{prev}]drawbox=x=0:y=ih-18:w=iw:h=18:color=0x262B35:t=fill[bg];"
              f"[bg][bar]overlay=x='-w+w*t/{dur:.3f}':y=H-18:eof_action=pass,trim=0:{dur:.3f},format=yuv420p[vout]")
    video = f"{tmp}/video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30", video], check=True)
    # music + mix
    music = f"{tmp}/music.wav"
    wavfile.write(music, bth_music.SR, bth_music.build(spec.get("mood", "drive"), dur + 0.8, int(spec.get("seed", 7))))
    vnorm = f"{tmp}/voice_norm.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000",
                    "-ac", "2", "-ar", "48000", vnorm], check=True)
    voice = vnorm
    mix = (f"[0:a]asplit=2[vo][sc];"
           f"[1:a]volume=0.20[m];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[md];"
           f"[vo][md]amix=inputs=2:duration=longest:normalize=0,atrim=0:{dur:.3f},afade=t=out:st={max(0, dur - 0.6):.3f}:d=0.6[aout]")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", music, "-i", video, "-filter_complex", mix,
                    "-map", "2:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
                    "-ac", "2", "-movflags", "+faststart", "-shortest", out], check=True)
    print(json.dumps({"out": out, "duration": round(dur, 2), "segments": [round(s, 2) for s in segs]}))


if __name__ == "__main__":
    build(sys.argv[1])
