"""Synthesize the ad's sound effects (no sourced audio). Deterministic: fixed seed.
Writes 48 kHz / 24-bit stereo WAVs to ../sfx/.
Peak levels put each effect 14-15 dB (integrated) under the -14.8 LUFS voice."""
import math
import os
import struct
import wave

import numpy as np

SR = 48000
OUT = os.path.join(os.path.dirname(__file__), "..", "sfx")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261008)


def svf_bandpass(x, fc, q):
    """Chamberlin state-variable filter with per-sample cutoff (array)."""
    lp = bp = 0.0
    y = np.zeros_like(x)
    damp = 1.0 / q
    for i in range(len(x)):
        f = 2 * math.sin(math.pi * min(fc[i], SR / 6) / SR)
        hp = x[i] - lp - damp * bp
        bp += f * hp
        lp += f * bp
        y[i] = bp
    return y


def onepole_lp(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    y = np.zeros_like(x)
    s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s
        y[i] = s
    return y


def smooth_env(n, attack_frac, curve=2.0):
    t = np.linspace(0, 1, n)
    a = attack_frac
    up = np.clip(t / a, 0, 1) ** curve
    down = np.clip((1 - t) / (1 - a), 0, 1) ** (curve * 1.3)
    return np.where(t < a, up, down)


def fade(x, fin=0.004, fout=0.02):
    n_in, n_out = int(fin * SR), int(fout * SR)
    x[:n_in] *= np.sin(np.linspace(0, math.pi / 2, n_in)) ** 2
    x[-n_out:] *= np.cos(np.linspace(0, math.pi / 2, n_out)) ** 2
    return x


def write(name, left, right=None, peak_db=-9.0):
    right = left if right is None else right
    st = np.stack([left, right], 1)
    st = st / np.abs(st).max() * 10 ** (peak_db / 20)
    data = (np.clip(st, -1, 1) * (2**23 - 1)).astype(np.int32)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(SR)
        raw = bytearray()
        for l, r in data:
            raw += struct.pack("<i", int(l))[:3] + struct.pack("<i", int(r))[:3]
        w.writeframes(bytes(raw))
    print("wrote", name, f"{len(left)/SR:.3f}s")


# 1. Airy whoosh: pink-ish noise through a swept band-pass, swell then fade (0.55 s)
def whoosh(dur=0.55, peak_at=0.58, f_lo=380, f_hi=1500, seed_shift=0):
    n = int(dur * SR)
    white = rng.standard_normal(n + seed_shift)[seed_shift:]
    pink = onepole_lp(white, 1200) * 0.7 + white * 0.08
    t = np.linspace(0, 1, n)
    # cutoff rises into the swell and relaxes after it
    sweep = np.where(t < peak_at, (t / peak_at) ** 1.4, 1 - 0.55 * np.clip((t - peak_at) / (1 - peak_at), 0, 1) ** 0.9)
    fc = f_lo + (f_hi - f_lo) * sweep
    y = svf_bandpass(pink, fc, q=0.9)
    y += 0.35 * onepole_lp(pink, 260)  # soft body
    y = onepole_lp(y, 5200)  # no harsh highs
    y *= smooth_env(n, peak_at, curve=2.2)
    return fade(y, 0.01, 0.06)


wl = whoosh()
# gentle stereo width: second decorrelated noise layer, mixed lightly
wr = 0.85 * wl + 0.15 * whoosh(seed_shift=977)
write("whoosh-air.wav", wl, wr, peak_db=-17.7)

# 2. Soft tick: rounded, very short (45 ms) — damped sine with a muted transient
n = int(0.045 * SR)
t = np.arange(n) / SR
tick = np.sin(2 * math.pi * 1350 * t) * np.exp(-t / 0.0075)
tick += 0.55 * np.sin(2 * math.pi * 520 * t) * np.exp(-t / 0.012)
tick = onepole_lp(tick, 4200)
tick[: int(0.0015 * SR)] *= np.linspace(0, 1, int(0.0015 * SR))
write("tick-soft.wav", fade(tick, 0.0015, 0.008), peak_db=-22)

# 3. Rising tone: gentle sine glide up a fifth+ (0.7 s) with soft fade
dur = 0.72
n = int(dur * SR)
t = np.arange(n) / SR
f0, f1 = 330.0, 554.37  # E4 -> C#5, exponential glide
f = f0 * (f1 / f0) ** (t / dur) ** 1.15
ph = 2 * math.pi * np.cumsum(f) / SR
rise = np.sin(ph) + 0.12 * np.sin(2 * ph) + 0.04 * np.sin(3 * ph)
env = np.clip(t / 0.22, 0, 1) ** 1.6 * np.clip((dur - t) / 0.28, 0, 1) ** 1.4
rise *= env
write("rise-soft.wav", fade(rise, 0.01, 0.03), peak_db=-27.4)

# 4. "Power on" chime: warm two-note sine (G4 then D5), gentle decay (~1.1 s)
dur = 1.15
n = int(dur * SR)
t = np.arange(n) / SR
chime = np.zeros(n)
for f, start, amp in ((392.0, 0.0, 1.0), (587.33, 0.12, 0.85)):
    tt = np.clip(t - start, 0, None)
    on = (t >= start).astype(float)
    att = np.clip(tt / 0.006, 0, 1)
    dec = np.exp(-tt / 0.32)
    note = np.sin(2 * math.pi * f * tt) + 0.18 * np.sin(2 * math.pi * 2 * f * tt) * np.exp(-tt / 0.12)
    note += 0.05 * np.sin(2 * math.pi * 3.01 * f * tt) * np.exp(-tt / 0.07)
    chime += amp * on * att * dec * note
chime = onepole_lp(chime, 5000)
write("chime-power-on.wav", fade(chime, 0.002, 0.15), peak_db=-18.8)

