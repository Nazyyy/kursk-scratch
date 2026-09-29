import os
import math
import struct
import wave
import hashlib
import json

ASSETS_DIR = "/home/dima/Projects/hackathon/scratch_project/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

manifest = {}

def register_asset(key, data, data_format, extra=None):
    md5 = hashlib.md5(data).hexdigest()
    md5ext = f"{md5}.{data_format}"
    filepath = os.path.join(ASSETS_DIR, md5ext)
    with open(filepath, "wb") as f:
        f.write(data)
    entry = {
        "assetId": md5,
        "name": key,
        "md5ext": md5ext,
        "dataFormat": data_format,
        "size": len(data)
    }
    if extra:
        entry.update(extra)
    manifest[key] = entry
    return entry

def save_svg(key, content, cx=240, cy=180):
    data = content.strip().encode("utf-8")
    return register_asset(key, data, "svg", {
        "rotationCenterX": cx,
        "rotationCenterY": cy
    })

def synth_wav(key, duration_s, generator_fn, rate=44100):
    num_samples = int(duration_s * rate)
    samples = []
    for i in range(num_samples):
        t = i / rate
        val = generator_fn(t, duration_s)
        # clamp
        val = max(-1.0, min(1.0, val))
        samples.append(int(val * 32760))
    
    import io
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        packed = struct.pack(f'<{len(samples)}h', *samples)
        w.writeframes(packed)
    data = wav_io.getvalue()
    return register_asset(key, data, "wav", {
        "rate": rate,
        "sampleCount": num_samples
    })

print("Helper functions ready")
