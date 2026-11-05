"""Original, royalty-free background music for Behind The Hype reels.

Everything is synthesised from scratch (no samples), so there is no copyright risk.
Usage: python3 bth_music.py <mood> <seconds> <out.wav> [seed]
Moods: drive (sport/business tension), chill (explainers), bright (gadgets/upbeat), dark (dramatic money stories)
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
MOODS = {
    #        bpm, root midi, scale intervals, chord degrees (in scale steps), swing
    "drive":  (104, 45, [0, 2, 3, 5, 7, 8, 10], [0, 5, 2, 6], 0.0),
    "chill":  (84, 48, [0, 2, 4, 5, 7, 9, 11], [0, 5, 3, 4], 0.12),
    "bright": (112, 50, [0, 2, 4, 5, 7, 9, 11], [0, 4, 5, 3], 0.0),
    "dark":   (92, 43, [0, 2, 3, 5, 7, 8, 10], [0, 5, 6, 4], 0.0),
}


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lowpass(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def highpass(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def env(n, a=0.01, r=0.2):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    na, nr = min(na, n), min(nr, n)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def chord_notes(root, scale, degree):
    notes = []
    for k in (0, 2, 4, 6):
        idx = degree + k
        notes.append(root + scale[idx % 7] + 12 * (idx // 7))
    return notes


def pad(freqs, n, rng):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            ph = rng.uniform(0, 2 * np.pi)
            ff = f * 2 ** (det / 12)
            # soft saw from a few harmonics
            for h in range(1, 7):
                out += np.sin(2 * np.pi * ff * h * t + ph * h) / (h * 1.3)
    out = lowpass(out, 1400)
    return out * env(n, 0.35, 0.5)


def kick(n):
    t = np.arange(n) / SR
    f = 110 * np.exp(-t * 28) + 42
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def hat(n, rng):
    x = highpass(rng.standard_normal(n), 7000)
    return x * np.exp(-np.arange(n) / SR * 60)


def snare(n, rng):
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)
    noise = highpass(rng.standard_normal(n), 1800) * np.exp(-t * 22)
    return 0.5 * body + 0.6 * noise


def pluck(f, n):
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t)
    return x * np.exp(-t * 6)


def build(mood="drive", seconds=45.0, seed=7):
    bpm, root, scale, prog, swing = MOODS[mood]
    rng = np.random.default_rng(seed)
    beat = 60.0 / bpm
    bar = 4 * beat
    total = int((seconds + 2) * SR)
    L = np.zeros(total)
    R = np.zeros(total)
    drums = np.zeros(total)
    bass = np.zeros(total)
    arp = np.zeros(total)

    nbars = int(np.ceil((seconds + 2) / bar))
    for b in range(nbars):
        start = int(b * bar * SR)
        deg = prog[b % len(prog)]
        notes = chord_notes(root + 12, scale, deg)
        n = min(int(bar * SR) + int(0.4 * SR), total - start)
        if n <= 0:
            break
        p = pad([midi_hz(m) for m in notes], n, rng)
        L[start:start + n] += p * 0.9
        R[start:start + n] += np.roll(p, 240) * 0.9
        # bass on beats 1 and 3
        for k in (0, 2):
            s = start + int(k * beat * SR)
            m = int(beat * 1.8 * SR)
            if s + m > total:
                continue
            f = midi_hz(root - 12 + scale[deg % 7])
            t = np.arange(m) / SR
            bass[s:s + m] += np.sin(2 * np.pi * f * t) * env(m, 0.01, 0.3)
        # arpeggio 8ths, intro bars skip it for build-up
        if b >= 1:
            for k in range(8):
                off = k * beat / 2 + (swing * beat / 2 if k % 2 else 0)
                s = start + int(off * SR)
                m = int(beat * 0.9 * SR)
                if s + m > total:
                    continue
                f = midi_hz(notes[[0, 1, 2, 3, 2, 1, 3, 2][k]] + 12)
                arp[s:s + m] += pluck(f, m) * (0.9 if k % 2 == 0 else 0.6)
        # drums from bar 2
        if b >= 2 or mood == "bright":
            for k in range(4):
                s = start + int(k * beat * SR)
                m = int(0.45 * SR)
                if s + m > total:
                    continue
                if k in (0, 2) or (mood in ("drive", "bright") and k == 3 and b % 2):
                    drums[s:s + m] += kick(m) * 0.9
                if k in (1, 3):
                    drums[s:s + m] += snare(m, rng) * 0.35
            for k in range(8):
                off = k * beat / 2 + (swing * beat / 2 if k % 2 else 0)
                s = start + int(off * SR)
                m = int(0.12 * SR)
                if s + m <= total:
                    drums[s:s + m] += hat(m, rng) * (0.18 if k % 2 else 0.28)

    arp = lowpass(arp, 3800)
    L += 0.55 * bass + 0.5 * drums + 0.42 * arp
    R += 0.55 * bass + 0.5 * drums + 0.42 * np.roll(arp, 600)
    out = np.stack([L, R], axis=1)[: int(seconds * SR)]
    # fades
    fi, fo = int(1.0 * SR), int(2.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]
    out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    out /= np.max(np.abs(out)) + 1e-9
    out *= 0.85
    return (out * 32767).astype(np.int16)


if __name__ == "__main__":
    mood = sys.argv[1] if len(sys.argv) > 1 else "drive"
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 45
    path = sys.argv[3] if len(sys.argv) > 3 else f"music_{mood}.wav"
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    wavfile.write(path, SR, build(mood, secs, seed))
    print(path)
