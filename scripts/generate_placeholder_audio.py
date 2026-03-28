import math
import os
import wave
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX_DIR = os.path.join(ROOT, "video", "teaser_trailer", "audio", "SFX")
MUSIC_DIR = os.path.join(ROOT, "video", "teaser_trailer", "audio", "Music")

os.makedirs(SFX_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

SAMPLE_RATE = 44100


def write_wave(path, samples):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples)
        wf.writeframes(frames)


def tone(freq, duration, amp=0.5):
    count = int(SAMPLE_RATE * duration)
    return [amp * math.sin(2 * math.pi * freq * (i / SAMPLE_RATE)) for i in range(count)]


def noise(duration, amp=0.2):
    import random

    count = int(SAMPLE_RATE * duration)
    return [amp * (random.random() * 2.0 - 1.0) for _ in range(count)]


def fade(samples, fade_in=0.02, fade_out=0.1):
    n = len(samples)
    in_n = int(SAMPLE_RATE * fade_in)
    out_n = int(SAMPLE_RATE * fade_out)
    out = samples[:]
    for i in range(min(in_n, n)):
        out[i] *= i / max(1, in_n)
    for i in range(min(out_n, n)):
        idx = n - 1 - i
        out[idx] *= i / max(1, out_n)
    return out


def mix(a, b):
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        av = a[i] if i < len(a) else 0.0
        bv = b[i] if i < len(b) else 0.0
        out.append(av + bv)
    return out


write_wave(os.path.join(SFX_DIR, "sfx_boot_hit.wav"), fade(tone(60, 0.5, 0.8), 0.01, 0.25))
write_wave(os.path.join(SFX_DIR, "sfx_ui_beeps.wav"), fade(tone(1200, 0.6, 0.18), 0.01, 0.08))
write_wave(os.path.join(SFX_DIR, "sfx_glitch_breach.wav"), fade(noise(1.0, 0.22), 0.01, 0.2))
write_wave(os.path.join(SFX_DIR, "sfx_impact_hit.wav"), fade(tone(90, 0.7, 0.9), 0.005, 0.3))
write_wave(os.path.join(SFX_DIR, "sfx_final_rise.wav"), fade(tone(300, 1.2, 0.25), 0.05, 0.2))

base = tone(110, 35.0, 0.07)
over = tone(220, 35.0, 0.03)
music = fade(mix(base, over), 0.2, 0.4)
write_wave(os.path.join(MUSIC_DIR, "music_spy_bed.wav"), music)

print("Placeholder audio files created.")
