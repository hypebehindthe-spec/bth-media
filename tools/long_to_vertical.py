"""Turn a long video spec (long/long_NNN.json) into vertical 9:16 Instagram parts, built with bth_reel3.py.

Each part is a run of whole sections; keep every part under 3:00 so Instagram can recommend it as a reel.
The section voice files are joined with the same 0.6 s gap the long video uses, the hand-checked cuts are
carried over, and a short silent end card is added ("Part 2 is next" / "Full video on YouTube").
The file is NOT capped to 4.6 MB: these parts are for the owner to upload by hand.

Usage: python3 tools/long_to_vertical.py long/long_002.json "1-4" "5-8"
Writes long/long_NNN_ig_p1.mp4, _p2.mp4 ... plus a caption file per part.
"""
import json, os, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bth_reel  # noqa: E402
bth_reel.cap_size = lambda path: None   # manual upload: no Make size limit
import bth_reel3  # noqa: E402
bth_reel3.cap_size = lambda path: None

GAP, END = 0.6, 2.6


def read(path):
    with wave.open(path) as w:
        return w.getframerate(), np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def main(spec_path, ranges):
    spec = json.load(open(os.path.join(ROOT, spec_path)))
    base = os.path.splitext(spec_path)[0]
    secs = spec["sections"]
    n = len(ranges)
    for pi, rg in enumerate(ranges, 1):
        a, b = (int(x) for x in rg.split("-"))
        part = secs[a - 1:b]
        audio, beats, cuts, t = [], [], [], 0.0
        sr = None
        for si, sec in enumerate(part):
            r, x = read(os.path.join(ROOT, sec["voice"]))
            sr = sr or r
            assert r == sr, "sample rates differ"
            if si:
                audio.append(np.zeros(int(GAP * sr), dtype=np.int16))
                t += GAP
                cuts.append(round(t - GAP / 2, 2))
            sec_cuts = sec.get("cuts") or []
            assert len(sec_cuts) == len(sec["beats"]) - 1, f"section {sec['chapter']}: cuts don't match beats"
            cuts += [round(t + c, 2) for c in sec_cuts]
            for bi, beat in enumerate(sec["beats"]):
                nb = dict(beat)
                nb["bg"] = sec.get("bg")
                if bi == 0:
                    tag = f"F1'S BANNED TRICKS · PART {pi}" if "banned" in spec.get("out", "").lower() else f"PART {pi} OF {n}"
                    tag = spec.get("ig_tag", tag).replace("{n}", str(pi))
                    if si == 0:
                        nb["lines"] = [[tag, "Y"]] + [l for l in beat["lines"] if l[1] != "Y"]
                beats.append(nb)
            audio.append(x)
            t += len(x) / sr
        # silent end card
        audio.append(np.zeros(int(END * sr), dtype=np.int16))
        cuts.append(round(t + 0.25, 2))
        last = pi == n
        beats.append({"say": "Full video on YouTube: Behind The Hype." if last else f"Part {pi + 1} is next. Follow so you don't miss it.",
                      "lines": [["FULL VIDEO ON YOUTUBE", "Y"], ["Behind The Hype", "y"], ["link in bio", "s"]] if last else
                               [[f"PART {pi + 1} IS NEXT", "Y"], ["Follow", "w"], ["so you don't miss it", "y"]],
                      "art": ["▶️"] if last else ["🏁"], "count": False, "bg": "sun"})
        voice_rel = f"{base}_ig_p{pi}_voice.wav"
        with wave.open(os.path.join(ROOT, voice_rel), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes(np.concatenate(audio).tobytes())
        vspec = {"out": f"{base}_ig_p{pi}.mp4", "voice": voice_rel, "mood": spec.get("mood", "drive"),
                 "seed": spec.get("seed", 7) + pi, "cuts": cuts, "beats": beats}
        sp = os.path.join(ROOT, f"{base}_ig_p{pi}.json")
        json.dump(vspec, open(sp, "w"), ensure_ascii=False, indent=1)
        bth_reel3.build(sp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
