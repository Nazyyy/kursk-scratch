import os
import math
import struct
import wave
import hashlib
import json

ASSETS_DIR = "/home/dima/Projects/hackathon/scratch_project/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

asset_registry = {}

def register_asset(filename, data, data_format):
    md5 = hashlib.md5(data).hexdigest()
    md5ext = f"{md5}.{data_format}"
    filepath = os.path.join(ASSETS_DIR, md5ext)
    with open(filepath, "wb") as f:
        f.write(data)
    asset_registry[filename] = {
        "assetId": md5,
        "md5ext": md5ext,
        "dataFormat": data_format,
        "size": len(data),
        "path": filepath
    }
    print(f"Registered {filename} -> {md5ext} ({len(data)} bytes)")
    return asset_registry[filename]

def save_svg(name, content):
    data = content.strip().encode("utf-8")
    return register_asset(name, data, "svg")

def save_wav(name, samples, rate=44100):
    import io
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        # pack as 16-bit signed little-endian
        packed = struct.pack(f'<{len(samples)}h', *samples)
        w.writeframes(packed)
    data = wav_io.getvalue()
    meta = register_asset(name, data, "wav")
    meta["rate"] = rate
    meta["sampleCount"] = len(samples)
    return meta

print("Asset generator ready")
