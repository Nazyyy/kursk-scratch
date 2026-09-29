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

print("1. Generating Sounds...")

# 1. snd_click: short UI tap
def gen_click(t, dur):
    return math.sin(2 * math.pi * 1200 * t) * math.exp(-t * 80)
synth_wav("snd_click", 0.06, gen_click)

# 2. snd_teleport: sci-fi time warp sweep
def gen_teleport(t, dur):
    p = t / dur
    freq = 220 + 1300 * p + 30 * math.sin(2 * math.pi * 18 * t)
    env = math.sin(math.pi * p)
    return 0.7 * math.sin(2 * math.pi * freq * t) * env
synth_wav("snd_teleport", 0.5, gen_teleport)

# 3. snd_focus: mechanical lens ratchet click
def gen_focus(t, dur):
    click1 = math.sin(2 * math.pi * 1600 * t) * math.exp(-t * 90)
    t2 = t - 0.06
    click2 = (math.sin(2 * math.pi * 2200 * t2) * math.exp(-t2 * 90)) if t2 > 0 else 0
    return 0.8 * (click1 + click2)
synth_wav("snd_focus", 0.15, gen_focus)

# 4. snd_wind: wind turbine hum and gust
def gen_wind(t, dur):
    p = t / dur
    hum = 0.4 * math.sin(2 * math.pi * 95 * t) + 0.25 * math.sin(2 * math.pi * 190 * t)
    gust = (0.5 + 0.5 * math.sin(2 * math.pi * 2 * t))
    noise = 0.2 * math.sin(2 * math.pi * 440 * t) * math.sin(2 * math.pi * 37 * t)
    return (hum + noise) * gust * math.sin(math.pi * p)
synth_wav("snd_wind", 0.8, gen_wind)

# 5. snd_magnet: pulsed detector beep
def gen_magnet(t, dur):
    sub_t = t % 0.08
    amp = math.exp(-sub_t * 60)
    return 0.6 * math.sin(2 * math.pi * 920 * t) * amp
synth_wav("snd_magnet", 0.35, gen_magnet)

# 6. snd_correct: cheerful victory chime (Major arpeggio C5 - E5 - G5 - C6)
def gen_correct(t, dur):
    step = int(t / 0.09)
    freqs = [523.25, 659.25, 783.99, 1046.50]
    f = freqs[min(step, len(freqs)-1)]
    local_t = t - step * 0.09
    decay = math.exp(-local_t * 10) if step < 3 else math.exp(-local_t * 5)
    return 0.7 * math.sin(2 * math.pi * f * t) * decay
synth_wav("snd_correct", 0.45, gen_correct)

# 7. snd_wrong: error buzz
def gen_wrong(t, dur):
    f = 160 - 50 * (t / dur)
    amp = math.exp(-t * 8)
    return 0.6 * (math.sin(2 * math.pi * f * t) + 0.3 * math.sin(2 * math.pi * 3 * f * t)) * amp
synth_wav("snd_wrong", 0.25, gen_wrong)

# 8. snd_fanfare: triumphant celebration brass
def gen_fanfare(t, dur):
    p = t / dur
    if t < 0.2:
        f = 523.25 # C5
    elif t < 0.4:
        f = 659.25 # E5
    elif t < 0.6:
        f = 783.99 # G5
    elif t < 0.85:
        f = 659.25 # E5
    else:
        f = 1046.50 # C6
    amp = math.sin(math.pi * (t % 0.2) / 0.2) if t < 0.85 else math.exp(-(t-0.85)*3)
    tone = math.sin(2 * math.pi * f * t) + 0.4 * math.sin(2 * math.pi * 2 * f * t) + 0.2 * math.sin(2 * math.pi * 3 * f * t)
    return 0.6 * tone * amp
synth_wav("snd_fanfare", 1.2, gen_fanfare)

print("Sounds generated.")

print("2. Generating Backdrops...")

# 1. bg_title (480x360)
svg_bg_title = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="grad_title" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050814"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
    <linearGradient id="neon_gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="50%" stop-color="#fef08a"/>
      <stop offset="100%" stop-color="#fbbf24"/>
    </linearGradient>
    <linearGradient id="neon_cyan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06b6d4"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#grad_title)"/>
  
  <!-- Digital grid -->
  <g stroke="#38bdf8" stroke-width="0.5" stroke-opacity="0.15">
    <line x1="0" y1="40" x2="480" y2="40"/>
    <line x1="0" y1="80" x2="480" y2="80"/>
    <line x1="0" y1="120" x2="480" y2="120"/>
    <line x1="0" y1="160" x2="480" y2="160"/>
    <line x1="0" y1="200" x2="480" y2="200"/>
    <line x1="0" y1="240" x2="480" y2="240"/>
    <line x1="0" y1="280" x2="480" y2="280"/>
    <line x1="0" y1="320" x2="480" y2="320"/>
    <line x1="60" y1="0" x2="60" y2="360"/>
    <line x1="120" y1="0" x2="120" y2="360"/>
    <line x1="180" y1="0" x2="180" y2="360"/>
    <line x1="240" y1="0" x2="240" y2="360"/>
    <line x1="300" y1="0" x2="300" y2="360"/>
    <line x1="360" y1="0" x2="360" y2="360"/>
    <line x1="420" y1="0" x2="420" y2="360"/>
  </g>

  <!-- Glowing rings portal -->
  <circle cx="240" cy="180" r="130" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="8 6" stroke-opacity="0.4"/>
  <circle cx="240" cy="180" r="90" fill="none" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="12 4" stroke-opacity="0.3"/>
  <circle cx="240" cy="180" r="50" fill="none" stroke="#38bdf8" stroke-width="1" stroke-opacity="0.5"/>

  <!-- Nightingale silhouette vector -->
  <path d="M 230 170 Q 245 160 255 170 Q 262 178 258 185 Q 248 190 238 182 Z M 255 170 L 268 172 L 257 175 Z M 230 170 Q 220 185 210 195 Q 222 188 235 180 Z" fill="#38bdf8" opacity="0.6"/>

  <!-- Top badge -->
  <rect x="110" y="14" width="260" height="24" rx="12" fill="#0f172a" stroke="#0ea5e9" stroke-width="1"/>
  <text x="240" y="30" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">★ IT-ЦОПП • КУРСКАЯ ОБЛАСТЬ ★</text>

  <!-- Main Title -->
  <text x="240" y="72" font-family="sans-serif" font-size="24" font-weight="900" fill="url(#neon_gold)" text-anchor="middle" letter-spacing="1.5">КОД ПЕРВОПРОХОДЦЕВ</text>
  <text x="240" y="94" font-family="sans-serif" font-size="13" font-weight="bold" fill="#e2e8f0" text-anchor="middle">Научный прорыв Соловьиного края</text>
  
  <!-- Subtitle pills -->
  <g font-family="sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">
    <rect x="70" y="105" width="105" height="18" rx="9" fill="#1e293b" stroke="#475569" stroke-width="0.8"/>
    <text x="122" y="117">Ф.А. СЕМЁНОВ (1853)</text>
    
    <rect x="187" y="105" width="105" height="18" rx="9" fill="#1e293b" stroke="#475569" stroke-width="0.8"/>
    <text x="240" y="117">А.Г. УФИМЦЕВ (1931)</text>

    <rect x="304" y="105" width="105" height="18" rx="9" fill="#1e293b" stroke="#475569" stroke-width="0.8"/>
    <text x="356" y="117">КМА И МИРНЫЙ АТОМ</text>
  </g>

  <!-- Tech corner accents -->
  <path d="M 15 25 L 35 25 L 35 15 M 15 25 L 15 45" stroke="#38bdf8" stroke-width="2" fill="none"/>
  <path d="M 465 25 L 445 25 L 445 15 M 465 25 L 465 45" stroke="#38bdf8" stroke-width="2" fill="none"/>
  <path d="M 15 335 L 35 335 L 35 345 M 15 335 L 15 315" stroke="#38bdf8" stroke-width="2" fill="none"/>
  <path d="M 465 335 L 445 335 L 445 345 M 465 335 L 465 315" stroke="#38bdf8" stroke-width="2" fill="none"/>

  <!-- Footer hint -->
  <text x="240" y="348" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Открытый региональный конкурс «IT-ЦОПП» для 6-11 классов</text>
</svg>"""
save_svg("bg_title", svg_bg_title)

# 2. bg_semenov (1853 Observatory)
svg_bg_semenov = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="60%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
    <linearGradient id="wood_floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#451a03"/>
      <stop offset="100%" stop-color="#271002"/>
    </linearGradient>
  </defs>
  <!-- Sky background through dome slit -->
  <rect width="480" height="360" fill="url(#night_sky)"/>

  <!-- Stars -->
  <g fill="#ffffff">
    <circle cx="50" cy="45" r="1.5" opacity="0.9"/>
    <circle cx="95" cy="70" r="1.2" opacity="0.8"/>
    <circle cx="140" cy="35" r="1.8" opacity="0.95"/>
    <circle cx="180" cy="85" r="1" opacity="0.7"/>
    <circle cx="230" cy="40" r="1.4" opacity="0.85"/>
    <circle cx="310" cy="55" r="1.6" opacity="0.9"/>
    <circle cx="380" cy="30" r="2" opacity="1"/>
    <circle cx="430" cy="75" r="1.2" opacity="0.8"/>
    <circle cx="460" cy="110" r="1.5" opacity="0.75"/>
    <circle cx="80" cy="130" r="1.3" opacity="0.85"/>
    <circle cx="160" cy="140" r="1.1" opacity="0.6"/>
  </g>

  <!-- Constellation Ursa Major lines -->
  <g stroke="#93c5fd" stroke-width="0.8" stroke-dasharray="2 2" opacity="0.5">
    <line x1="310" y1="55" x2="340" y2="65"/>
    <line x1="340" y1="65" x2="380" y2="30"/>
    <line x1="380" y1="30" x2="410" y2="45"/>
    <line x1="410" y1="45" x2="430" y2="75"/>
    <line x1="430" y1="75" x2="395" y2="90"/>
    <line x1="395" y1="90" x2="380" y2="30"/>
  </g>

  <!-- Wooden Observatory Dome Opening -->
  <path d="M 0 0 L 120 0 L 120 220 L 0 240 Z" fill="#311e11"/>
  <path d="M 360 0 L 480 0 L 480 240 L 360 220 Z" fill="#311e11"/>
  <path d="M 120 0 Q 240 60 360 0 L 360 20 Q 240 75 120 20 Z" fill="#452514"/>

  <!-- Wooden pillars -->
  <rect x="110" y="0" width="16" height="230" fill="#24140b"/>
  <rect x="354" y="0" width="16" height="230" fill="#24140b"/>

  <!-- Wooden Floor -->
  <polygon points="0,230 480,230 480,360 0,360" fill="url(#wood_floor)"/>
  <g stroke="#1b0b02" stroke-width="1.5" opacity="0.6">
    <line x1="0" y1="260" x2="480" y2="260"/>
    <line x1="0" y1="295" x2="480" y2="295"/>
    <line x1="0" y1="330" x2="480" y2="330"/>
  </g>

  <!-- Antique table & manuscripts on left -->
  <rect x="15" y="240" width="90" height="50" fill="#582a0e" rx="3"/>
  <rect x="25" y="235" width="35" height="6" fill="#fef08a" opacity="0.8"/>
  <rect x="65" y="233" width="30" height="8" fill="#e2e8f0" opacity="0.9"/>
  <!-- Astrolabe on table -->
  <circle cx="80" cy="225" r="10" fill="none" stroke="#f59e0b" stroke-width="2"/>
  <line x1="80" y1="215" x2="80" y2="235" stroke="#f59e0b" stroke-width="1.5"/>

  <!-- Header banner -->
  <rect x="80" y="6" width="320" height="22" rx="4" fill="#000000" fill-opacity="0.6" stroke="#f59e0b" stroke-width="0.8"/>
  <text x="240" y="21" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fef08a" text-anchor="middle">КУРСК • 1853 г. • ОБСЕРВАТОРИЯ Ф.А. СЕМЁНОВА</text>
</svg>"""
save_svg("bg_semenov", svg_bg_semenov)

# 3. bg_ufimtsev (1931 Wind Turbine & Workshop)
svg_bg_ufimtsev = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="wind_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#94a3b8"/>
    </linearGradient>
    <linearGradient id="brick_wall" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#881337"/>
      <stop offset="100%" stop-color="#4c0519"/>
    </linearGradient>
  </defs>
  <!-- Sky -->
  <rect width="480" height="360" fill="url(#wind_sky)"/>

  <!-- Swift windy clouds -->
  <path d="M 20 60 Q 80 40 160 55 Q 240 70 320 50 Q 400 35 460 55 L 480 90 L 0 90 Z" fill="#ffffff" fill-opacity="0.2"/>
  <path d="M 0 110 Q 100 85 220 100 Q 340 115 480 95 L 480 140 L 0 140 Z" fill="#ffffff" fill-opacity="0.15"/>

  <!-- Ground / Semenovskaya street pavement -->
  <rect x="0" y="240" width="480" height="120" fill="#334155"/>
  <polygon points="0,240 480,240 480,250 0,250" fill="#475569"/>

  <!-- Red-brick workshop on the left (Ufimtsev's house/workshop) -->
  <rect x="0" y="110" width="170" height="135" fill="url(#brick_wall)"/>
  <rect x="25" y="140" width="45" height="60" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <line x1="47" y1="140" x2="47" y2="200" stroke="#f59e0b" stroke-width="1.5"/>
  <line x1="25" y1="170" x2="70" y2="170" stroke="#f59e0b" stroke-width="1.5"/>
  <!-- Workshop sign -->
  <rect x="15" y="118" width="140" height="16" fill="#1e293b" rx="2" stroke="#94a3b8" stroke-width="0.8"/>
  <text x="85" y="130" font-family="sans-serif" font-size="8" font-weight="bold" fill="#f8fafc" text-anchor="middle">МАСТЕРСКАЯ А.Г. УФИМЦЕВА</text>

  <!-- Steel lattice tower of the wind generator in background center-right -->
  <polygon points="330,40 350,40 375,240 305,240" fill="#1e293b" opacity="0.9"/>
  <!-- Truss lattice lines -->
  <g stroke="#94a3b8" stroke-width="1.5" opacity="0.7">
    <line x1="330" y1="40" x2="375" y2="240"/>
    <line x1="350" y1="40" x2="305" y2="240"/>
    <line x1="324" y1="80" x2="356" y2="80"/>
    <line x1="319" y1="120" x2="361" y2="120"/>
    <line x1="314" y1="160" x2="366" y2="160"/>
    <line x1="309" y1="200" x2="371" y2="200"/>
  </g>

  <!-- Vintage street lantern on right -->
  <rect x="440" y="160" width="6" height="85" fill="#0f172a"/>
  <circle cx="443" cy="155" r="12" fill="#fef08a" opacity="0.6"/>
  <circle cx="443" cy="155" r="5" fill="#ffffff"/>

  <!-- Header banner -->
  <rect x="70" y="6" width="340" height="22" rx="4" fill="#000000" fill-opacity="0.65" stroke="#38bdf8" stroke-width="0.8"/>
  <text x="240" y="21" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">КУРСК • 1931 г. • ВЕТРОСТАНЦИЯ А.Г. УФИМЦЕВА</text>
</svg>"""
save_svg("bg_ufimtsev", svg_bg_ufimtsev)

# 4. bg_kma_aes (Kursk Magnetic Anomaly & Nuclear Power Plant)
svg_bg_kma = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="sky_kma" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0369a1"/>
      <stop offset="45%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
  </defs>
  <!-- Sky -->
  <rect width="480" height="360" fill="url(#sky_kma)"/>

  <!-- Magnetic field curves -->
  <path d="M 50 160 Q 150 40 280 160" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.5"/>
  <path d="M 20 180 Q 150 10 320 180" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.4"/>
  <path d="M 80 150 Q 150 70 250 150" fill="none" stroke="#0ea5e9" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.6"/>

  <!-- Distant Kursk NPP (г. Курчатов) cooling towers and dome on right horizon -->
  <g fill="#94a3b8" opacity="0.85">
    <!-- Cooling towers -->
    <path d="M 360 170 Q 363 140 357 115 L 383 115 Q 377 140 380 170 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="1"/>
    <path d="M 390 170 Q 393 140 387 115 L 413 115 Q 407 140 410 170 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="1"/>
    <!-- Reactor block dome -->
    <rect x="420" y="130" width="40" height="40" fill="#cbd5e1"/>
    <ellipse cx="440" cy="130" rx="16" ry="8" fill="#38bdf8" opacity="0.7"/>
    <!-- Atom symbol over plant -->
    <circle cx="440" cy="100" r="10" fill="none" stroke="#0284c7" stroke-width="1.5"/>
    <ellipse cx="440" cy="100" rx="14" ry="4" fill="none" stroke="#0284c7" stroke-width="1" transform="rotate(30 440 100)"/>
    <ellipse cx="440" cy="100" rx="14" ry="4" fill="none" stroke="#0284c7" stroke-width="1" transform="rotate(-30 440 100)"/>
  </g>

  <!-- Giant open pit quarry terraces (КМА) -->
  <polygon points="0,170 340,170 300,200 0,200" fill="#9a3412"/>
  <polygon points="0,200 480,185 450,225 0,225" fill="#78350f"/>
  <polygon points="0,225 480,225 430,265 0,265" fill="#451a03"/>
  <polygon points="0,265 480,265 480,360 0,360" fill="#1e293b"/>

  <!-- Rich banded iron formation layer (Magnetite ore) -->
  <polygon points="80,270 320,270 300,310 60,310" fill="#334155" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4 2"/>
  <text x="180" y="295" font-family="sans-serif" font-size="10" font-weight="bold" fill="#38bdf8">ЗАЛЕЖИ МАГНЕТИТА КМА</text>

  <!-- Header banner -->
  <rect x="60" y="6" width="360" height="22" rx="4" fill="#000000" fill-opacity="0.65" stroke="#0284c7" stroke-width="0.8"/>
  <text x="240" y="21" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">КУРСКИЙ КРАЙ • КМА И ЭНЕРГИЯ АТОМА (г. КУРЧАТОВ)</text>
</svg>"""
save_svg("bg_kma_aes", svg_bg_kma)

# 5. bg_hall_of_fame (Grand Museum Hall of Kursk Pioneers)
svg_bg_hall = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="palace_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e1b4b"/>
      <stop offset="50%" stop-color="#2e1065"/>
      <stop offset="100%" stop-color="#3b0764"/>
    </linearGradient>
    <linearGradient id="gold_frame" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbbf24"/>
      <stop offset="50%" stop-color="#fef08a"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
  </defs>
  <!-- Wall -->
  <rect width="480" height="360" fill="url(#palace_wall)"/>

  <!-- Marble floor with reflection -->
  <rect x="0" y="240" width="480" height="120" fill="#0f172a"/>
  <!-- Grand red carpet in center -->
  <polygon points="170,240 310,240 350,360 130,360" fill="#991b1b"/>
  <polygon points="180,240 300,240 338,360 142,360" fill="#b91c1c"/>
  <line x1="180" y1="240" x2="142" y2="360" stroke="#f59e0b" stroke-width="2"/>
  <line x1="300" y1="240" x2="338" y2="360" stroke="#f59e0b" stroke-width="2"/>

  <!-- Neoclassical Columns -->
  <g fill="#e2e8f0" stroke="#94a3b8" stroke-width="1">
    <rect x="15" y="30" width="25" height="215"/>
    <rect x="10" y="25" width="35" height="8" rx="2" fill="#f59e0b"/>
    <rect x="10" y="240" width="35" height="10" rx="2" fill="#f59e0b"/>

    <rect x="440" y="30" width="25" height="215"/>
    <rect x="435" y="25" width="35" height="8" rx="2" fill="#f59e0b"/>
    <rect x="435" y="240" width="35" height="10" rx="2" fill="#f59e0b"/>
  </g>

  <!-- Three Ornate Portrait Frames on the wall -->
  <!-- 1. Semenov -->
  <g>
    <rect x="55" y="55" width="95" height="125" rx="4" fill="#0f172a" stroke="url(#gold_frame)" stroke-width="4"/>
    <circle cx="102" cy="100" r="28" fill="#1e293b"/>
    <!-- Silhouette/Portrait icon -->
    <path d="M 94 95 Q 102 85 110 95 Q 112 110 102 115 Q 92 110 94 95 Z" fill="#fef08a"/>
    <text x="102" y="145" font-family="sans-serif" font-size="8" font-weight="bold" fill="#fef08a" text-anchor="middle">Ф.А. СЕМЁНОВ</text>
    <text x="102" y="157" font-family="sans-serif" font-size="7" fill="#cbd5e1" text-anchor="middle">Астроном • Оптик</text>
    <text x="102" y="167" font-family="sans-serif" font-size="6.5" fill="#f59e0b" text-anchor="middle">Демидовская премия</text>
  </g>

  <!-- 2. Ufimtsev -->
  <g>
    <rect x="192" y="50" width="96" height="125" rx="4" fill="#0f172a" stroke="url(#gold_frame)" stroke-width="4"/>
    <circle cx="240" cy="95" r="28" fill="#1e293b"/>
    <path d="M 232 90 Q 240 80 248 90 Q 250 105 240 110 Q 230 105 232 90 Z" fill="#38bdf8"/>
    <text x="240" y="140" font-family="sans-serif" font-size="8" font-weight="bold" fill="#38bdf8" text-anchor="middle">А.Г. УФИМЦЕВ</text>
    <text x="240" y="152" font-family="sans-serif" font-size="7" fill="#cbd5e1" text-anchor="middle">Изобретатель ВЭС</text>
    <text x="240" y="162" font-family="sans-serif" font-size="6.5" fill="#38bdf8" text-anchor="middle">Авиаконструктор</text>
  </g>

  <!-- 3. Lazarev / KMA -->
  <g>
    <rect x="330" y="55" width="95" height="125" rx="4" fill="#0f172a" stroke="url(#gold_frame)" stroke-width="4"/>
    <circle cx="377" cy="100" r="28" fill="#1e293b"/>
    <path d="M 369 95 Q 377 85 385 95 Q 387 110 377 115 Q 367 110 369 95 Z" fill="#4ade80"/>
    <text x="377" y="145" font-family="sans-serif" font-size="8" font-weight="bold" fill="#4ade80" text-anchor="middle">П.П. ЛАЗАРЕВ</text>
    <text x="377" y="157" font-family="sans-serif" font-size="7" fill="#cbd5e1" text-anchor="middle">Академик • КМА</text>
    <text x="377" y="167" font-family="sans-serif" font-size="6.5" fill="#4ade80" text-anchor="middle">Геофизика недр</text>
  </g>

  <!-- Central Pedestal -->
  <polygon points="205,240 275,240 285,255 195,255" fill="#f59e0b"/>

  <!-- Header banner -->
  <rect x="60" y="6" width="360" height="22" rx="4" fill="#000000" fill-opacity="0.65" stroke="#f59e0b" stroke-width="0.8"/>
  <text x="240" y="21" font-family="sans-serif" font-size="11" font-weight="bold" fill="#fef08a" text-anchor="middle">ЗАЛ НАУЧНОЙ СЛАВЫ СОЛОВЬИНОГО КРАЯ</text>
</svg>"""
save_svg("bg_hall_of_fame", svg_bg_hall)

print("Backdrops generated.")

print("3. Generating Hero Costumes...")

# Hero 1: hero_copt (IT-ЦОПП school uniform)
svg_hero_copt = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <!-- Body/Head -->
  <circle cx="35" cy="22" r="14" fill="#fed7aa"/>
  <!-- Hair -->
  <path d="M 21 22 Q 35 6 49 22 Q 45 10 35 10 Q 25 10 21 22 Z" fill="#92400e"/>
  <!-- Eyes & Smile -->
  <circle cx="30" cy="21" r="2" fill="#0f172a"/>
  <circle cx="40" cy="21" r="2" fill="#0f172a"/>
  <path d="M 31 28 Q 35 32 39 28" stroke="#0f172a" stroke-width="1.5" fill="none"/>
  <!-- IT-ЦОПП Hoodie (Blue & Cyan) -->
  <path d="M 20 40 L 50 40 L 54 80 L 16 80 Z" fill="#0284c7" rx="3"/>
  <path d="M 27 40 L 35 55 L 43 40" stroke="#f59e0b" stroke-width="2" fill="none"/>
  <!-- ЦОПП Badge -->
  <rect x="23" y="48" width="24" height="12" rx="2" fill="#0f172a"/>
  <text x="35" y="57" font-family="sans-serif" font-size="6" font-weight="bold" fill="#38bdf8" text-anchor="middle">ЦОПП</text>
  <!-- Arms & Smart Communicator -->
  <path d="M 20 42 L 10 65" stroke="#0284c7" stroke-width="6" stroke-linecap="round"/>
  <path d="M 50 42 L 58 60 L 52 70" stroke="#0284c7" stroke-width="6" stroke-linecap="round"/>
  <!-- Wrist screen -->
  <rect x="7" y="62" width="7" height="6" rx="1" fill="#38bdf8"/>
  <!-- Legs -->
  <line x1="26" y1="80" x2="26" y2="102" stroke="#1e293b" stroke-width="6"/>
  <line x1="44" y1="80" x2="44" y2="102" stroke="#1e293b" stroke-width="6"/>
  <!-- Shoes -->
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#0ea5e9"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#0ea5e9"/>
</svg>"""
save_svg("hero_copt", svg_hero_copt, cx=35, cy=55)

# Hero 2: hero_astronomer (1853 Victorian cloak & spectacles)
svg_hero_astronomer = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="14" fill="#fed7aa"/>
  <path d="M 21 22 Q 35 6 49 22 Q 45 10 35 10 Q 25 10 21 22 Z" fill="#78350f"/>
  <!-- Round brass spectacles -->
  <circle cx="30" cy="21" r="3.5" fill="none" stroke="#f59e0b" stroke-width="1.2"/>
  <circle cx="40" cy="21" r="3.5" fill="none" stroke="#f59e0b" stroke-width="1.2"/>
  <line x1="33.5" y1="21" x2="36.5" y2="21" stroke="#f59e0b" stroke-width="1"/>
  <path d="M 31 29 Q 35 32 39 29" stroke="#0f172a" stroke-width="1.5" fill="none"/>
  <!-- Victorian Vest & Dark Cloak -->
  <path d="M 16 38 L 54 38 L 58 85 L 12 85 Z" fill="#1e1b4b"/>
  <polygon points="26,38 35,55 44,38" fill="#7c2d12"/>
  <!-- Brass buttons -->
  <circle cx="35" cy="62" r="1.5" fill="#f59e0b"/>
  <circle cx="35" cy="72" r="1.5" fill="#f59e0b"/>
  <!-- Starchart in hand -->
  <rect x="4" y="60" width="14" height="20" rx="1" fill="#fef08a" stroke="#b45309" stroke-width="0.8"/>
  <circle cx="11" cy="70" r="3" fill="none" stroke="#b45309" stroke-width="0.8"/>
  <!-- Legs & Boots -->
  <line x1="26" y1="85" x2="26" y2="102" stroke="#0f172a" stroke-width="6"/>
  <line x1="44" y1="85" x2="44" y2="102" stroke="#0f172a" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#451a03"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#451a03"/>
</svg>"""
save_svg("hero_astronomer", svg_hero_astronomer, cx=35, cy=55)

# Hero 3: hero_aviator (1931 Flight leather jacket & goggles)
svg_hero_aviator = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="24" r="13" fill="#fed7aa"/>
  <!-- Aviator leather helmet -->
  <path d="M 21 24 Q 35 10 49 24 L 49 32 L 44 32 L 44 26 Q 35 15 26 26 L 26 32 L 21 32 Z" fill="#78350f"/>
  <!-- Aviator Goggles on forehead -->
  <rect x="24" y="14" width="10" height="6" rx="2" fill="#38bdf8" stroke="#f59e0b" stroke-width="1"/>
  <rect x="36" y="14" width="10" height="6" rx="2" fill="#38bdf8" stroke="#f59e0b" stroke-width="1"/>
  <line x1="34" y1="17" x2="36" y2="17" stroke="#78350f" stroke-width="1.5"/>
  <!-- Face -->
  <circle cx="30" cy="24" r="2" fill="#0f172a"/>
  <circle cx="40" cy="24" r="2" fill="#0f172a"/>
  <path d="M 31 30 Q 35 34 39 30" stroke="#0f172a" stroke-width="1.5" fill="none"/>
  <!-- Brown flight jacket with fleece collar -->
  <path d="M 18 40 L 52 40 L 54 82 L 16 82 Z" fill="#9a3412"/>
  <path d="M 20 40 Q 35 48 50 40 L 46 48 L 24 48 Z" fill="#fef08a"/>
  <!-- Wrench in right hand -->
  <path d="M 8 55 L 12 75" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <circle cx="7" cy="55" r="4" fill="none" stroke="#64748b" stroke-width="2"/>
  <!-- Legs -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#334155" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#334155" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#1e293b"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#1e293b"/>
</svg>"""
save_svg("hero_aviator", svg_hero_aviator, cx=35, cy=55)

# Hero 4: hero_physicist (KMA / Atomic researcher with sensor)
svg_hero_physicist = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="14" fill="#fed7aa"/>
  <!-- White Safety Helmet with cyan visor -->
  <path d="M 20 20 Q 35 6 50 20 L 50 25 L 20 25 Z" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <rect x="23" y="18" width="24" height="6" rx="2" fill="#06b6d4" opacity="0.8"/>
  <circle cx="30" cy="24" r="2" fill="#0f172a"/>
  <circle cx="40" cy="24" r="2" fill="#0f172a"/>
  <path d="M 31 30 Q 35 33 39 30" stroke="#0f172a" stroke-width="1.5" fill="none"/>
  <!-- High-tech white lab suit with blue radiation belt -->
  <path d="M 18 38 L 52 38 L 54 82 L 16 82 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <rect x="16" y="65" width="38" height="6" fill="#0284c7"/>
  <!-- Sensor handheld unit -->
  <rect x="6" y="58" width="10" height="16" rx="2" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <circle cx="11" cy="64" r="2" fill="#22c55e"/>
  <!-- Legs -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#e2e8f0" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#e2e8f0" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#475569"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#475569"/>
</svg>"""
save_svg("hero_physicist", svg_hero_physicist, cx=35, cy=55)

# Hero 5: hero_triumph (Winner with Gold Demidov Medal)
svg_hero_triumph = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="14" fill="#fed7aa"/>
  <path d="M 21 22 Q 35 6 49 22 Q 45 10 35 10 Q 25 10 21 22 Z" fill="#92400e"/>
  <!-- Golden laurel wreath on head -->
  <path d="M 22 14 Q 35 8 48 14" stroke="#fbbf24" stroke-width="3" fill="none"/>
  <circle cx="30" cy="21" r="2" fill="#0f172a"/>
  <circle cx="40" cy="21" r="2" fill="#0f172a"/>
  <path d="M 29 27 Q 35 34 41 27" stroke="#0f172a" stroke-width="2" fill="none"/>
  <!-- Formal navy suit -->
  <path d="M 18 38 L 52 38 L 54 82 L 16 82 Z" fill="#1e1b4b"/>
  <!-- Red Imperial Ribbon & Gold Demidov Medal -->
  <line x1="28" y1="38" x2="35" y2="52" stroke="#dc2626" stroke-width="2.5"/>
  <line x1="42" y1="38" x2="35" y2="52" stroke="#dc2626" stroke-width="2.5"/>
  <circle cx="35" cy="56" r="6" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <!-- Certificate of Honor in hand -->
  <rect x="50" y="52" width="16" height="24" rx="1" fill="#fef08a" stroke="#b45309" stroke-width="0.8"/>
  <line x1="53" y1="58" x2="63" y2="58" stroke="#b45309" stroke-width="0.8"/>
  <line x1="53" y1="63" x2="63" y2="63" stroke="#b45309" stroke-width="0.8"/>
  <line x1="53" y1="68" x2="60" y2="68" stroke="#b45309" stroke-width="0.8"/>
  <!-- Legs -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#0f172a" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#0f172a" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#0f172a"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#0f172a"/>
</svg>"""
save_svg("hero_triumph", svg_hero_triumph, cx=35, cy=55)

print("Hero costumes generated.")

print("4. Generating Kursik (Cyber-Nightingale) Costumes...")

# Kursik 1: kursik_hover
svg_kursik_hover = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <!-- Thruster particle -->
  <polygon points="12,30 2,33 10,26" fill="#38bdf8" opacity="0.8"/>
  <!-- Nightingale cyber body -->
  <ellipse cx="28" cy="24" rx="16" ry="11" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
  <!-- Belly glow plate -->
  <path d="M 20 28 Q 28 34 38 28 Z" fill="#0284c7"/>
  <!-- Wing (cyber feathers) -->
  <polygon points="16,22 28,10 34,22" fill="#0ea5e9" stroke="#0284c7" stroke-width="1"/>
  <!-- Head -->
  <circle cx="44" cy="18" r="9" fill="#e2e8f0" stroke="#475569" stroke-width="1"/>
  <!-- Cyber Eye (Cyan LED) -->
  <circle cx="46" cy="16" r="3" fill="#06b6d4"/>
  <circle cx="47" cy="15" r="1" fill="#ffffff"/>
  <!-- Golden Beak -->
  <polygon points="52,16 62,19 52,22" fill="#fbbf24" stroke="#d97706" stroke-width="0.8"/>
  <!-- Tail feathers -->
  <polygon points="14,26 2,22 8,28" fill="#0284c7"/>
  <polygon points="14,27 4,32 10,29" fill="#0369a1"/>
  <!-- Mini headphone/antenna -->
  <line x1="42" y1="10" x2="42" y2="6" stroke="#0ea5e9" stroke-width="1.5"/>
  <circle cx="42" cy="5" r="2" fill="#38bdf8"/>
</svg>"""
save_svg("kursik_hover", svg_kursik_hover, cx=32, cy=25)

# Kursik 2: kursik_talk (soundwaves from beak/speaker)
svg_kursik_talk = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <polygon points="12,30 2,33 10,26" fill="#38bdf8" opacity="0.8"/>
  <ellipse cx="28" cy="24" rx="16" ry="11" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
  <path d="M 20 28 Q 28 34 38 28 Z" fill="#0284c7"/>
  <polygon points="16,22 28,8 34,22" fill="#0ea5e9" stroke="#0284c7" stroke-width="1"/>
  <circle cx="44" cy="18" r="9" fill="#e2e8f0" stroke="#475569" stroke-width="1"/>
  <circle cx="46" cy="16" r="3.2" fill="#06b6d4"/>
  <!-- Beak open in song -->
  <polygon points="52,15 62,16 53,19" fill="#fbbf24"/>
  <polygon points="53,20 60,23 52,24" fill="#fbbf24"/>
  <!-- Sound wave arcs -->
  <path d="M 59 12 Q 63 19 59 26" stroke="#38bdf8" stroke-width="1.5" fill="none"/>
  <path d="M 62 9 Q 67 19 62 29" stroke="#38bdf8" stroke-width="1.2" fill="none" opacity="0.6"/>
  <!-- Tail -->
  <polygon points="14,26 2,22 8,28" fill="#0284c7"/>
  <!-- Antenna -->
  <line x1="42" y1="10" x2="42" y2="6" stroke="#0ea5e9" stroke-width="1.5"/>
  <circle cx="42" cy="5" r="2" fill="#facc15"/>
</svg>"""
save_svg("kursik_talk", svg_kursik_talk, cx=32, cy=25)

# Kursik 3: kursik_scan (projecting blue scanner beam down)
svg_kursik_scan = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <!-- Downward scanning laser cone -->
  <polygon points="28,30 6,50 50,50" fill="#38bdf8" opacity="0.3"/>
  <ellipse cx="28" cy="24" rx="16" ry="11" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
  <path d="M 20 28 Q 28 34 38 28 Z" fill="#22c55e"/>
  <polygon points="16,22 28,14 34,22" fill="#0ea5e9" stroke="#0284c7" stroke-width="1"/>
  <circle cx="44" cy="18" r="9" fill="#e2e8f0" stroke="#475569" stroke-width="1"/>
  <circle cx="46" cy="16" r="3" fill="#22c55e"/>
  <polygon points="52,16 62,19 52,22" fill="#fbbf24"/>
  <polygon points="14,26 2,22 8,28" fill="#0284c7"/>
</svg>"""
save_svg("kursik_scan", svg_kursik_scan, cx=32, cy=25)

# Kursik 4: kursik_celebrate (sparks & joy)
svg_kursik_celebrate = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <!-- Sparks -->
  <circle cx="58" cy="8" r="2" fill="#fbbf24"/>
  <circle cx="20" cy="6" r="1.5" fill="#f43f5e"/>
  <circle cx="48" cy="4" r="2" fill="#38bdf8"/>
  <ellipse cx="28" cy="24" rx="16" ry="11" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
  <!-- Wings raised high in victory -->
  <polygon points="24,20 20,4 32,14" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <polygon points="30,20 38,4 42,16" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <circle cx="44" cy="18" r="9" fill="#e2e8f0" stroke="#475569" stroke-width="1"/>
  <circle cx="46" cy="16" r="3" fill="#fbbf24"/>
  <polygon points="52,16 62,19 52,22" fill="#fbbf24"/>
  <!-- Mini celebratory laurel sprig in beak -->
  <path d="M 58 19 Q 62 14 60 10" stroke="#22c55e" stroke-width="1.5" fill="none"/>
</svg>"""
save_svg("kursik_celebrate", svg_kursik_celebrate, cx=32, cy=25)

print("5. Generating Historical Figures Costumes...")

# Figure 1: char_semenov (Fedor Semenov)
svg_char_semenov = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <!-- Head & Gray Hair -->
  <circle cx="40" cy="24" r="15" fill="#fed7aa"/>
  <path d="M 25 24 Q 40 6 55 24 Q 50 12 40 12 Q 30 12 25 24 Z" fill="#94a3b8"/>
  <!-- Gray Beard -->
  <path d="M 28 28 Q 40 44 52 28 Q 48 38 40 38 Q 32 38 28 28 Z" fill="#cbd5e1"/>
  <!-- Face details -->
  <circle cx="35" cy="22" r="2" fill="#1e293b"/>
  <circle cx="45" cy="22" r="2" fill="#1e293b"/>
  <path d="M 36 28 Q 40 30 44 28" stroke="#1e293b" stroke-width="1" fill="none"/>
  <!-- 19th Century Dark Blue Merchant Caftan -->
  <path d="M 20 40 L 60 40 L 66 95 L 14 95 Z" fill="#1e3a8a"/>
  <!-- Velvet lapels with gold trim -->
  <polygon points="32,40 40,60 48,40" fill="#1e293b"/>
  <line x1="32" y1="40" x2="40" y2="60" stroke="#f59e0b" stroke-width="1"/>
  <line x1="48" y1="40" x2="40" y2="60" stroke="#f59e0b" stroke-width="1"/>
  <!-- Brass hand telescope in right hand -->
  <polygon points="62,60 76,40 78,43 64,63" fill="#f59e0b" stroke="#b45309" stroke-width="1"/>
  <rect x="74" y="38" width="5" height="4" rx="1" fill="#fef08a"/>
  <!-- Book 'Затмения' in left hand -->
  <rect x="8" y="65" width="18" height="24" rx="1" fill="#78350f" stroke="#f59e0b" stroke-width="1"/>
  <line x1="12" y1="72" x2="22" y2="72" stroke="#fef08a" stroke-width="1"/>
  <line x1="12" y1="77" x2="22" y2="77" stroke="#fef08a" stroke-width="1"/>
  <!-- Boots -->
  <line x1="30" y1="95" x2="30" y2="114" stroke="#0f172a" stroke-width="7"/>
  <line x1="50" y1="95" x2="50" y2="114" stroke="#0f172a" stroke-width="7"/>
  <ellipse cx="27" cy="115" rx="8" ry="4" fill="#0f172a"/>
  <ellipse cx="53" cy="115" rx="8" ry="4" fill="#0f172a"/>
</svg>"""
save_svg("char_semenov", svg_char_semenov, cx=40, cy=60)

# Figure 2: char_ufimtsev (Anatoly Ufimtsev)
svg_char_ufimtsev = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <circle cx="40" cy="24" r="14" fill="#fed7aa"/>
  <!-- Dark wavy hair 1930s style -->
  <path d="M 26 24 Q 40 8 54 24 Q 48 14 40 14 Q 32 14 26 24 Z" fill="#1e293b"/>
  <!-- Distinctive mustache -->
  <path d="M 33 29 Q 40 33 47 29 Q 43 31 40 31 Q 37 31 33 29 Z" fill="#1e293b"/>
  <circle cx="34" cy="22" r="2" fill="#0f172a"/>
  <circle cx="46" cy="22" r="2" fill="#0f172a"/>
  <!-- White shirt, tie & engineer's leather apron -->
  <path d="M 22 40 L 58 40 L 62 92 L 18 92 Z" fill="#78350f"/>
  <!-- White shirt collar & red tie -->
  <polygon points="34,40 40,50 46,40" fill="#f8fafc"/>
  <polygon points="39,44 41,44 42,56 38,56" fill="#dc2626"/>
  <!-- Blueprint roll in left arm -->
  <rect x="8" y="55" width="10" height="30" rx="3" fill="#bae6fd" stroke="#0284c7" stroke-width="1" transform="rotate(-15 13 70)"/>
  <!-- Large steel wrench in right hand -->
  <path d="M 62,55 L 72,75" stroke="#94a3b8" stroke-width="4" stroke-linecap="round"/>
  <circle cx="62" cy="55" r="5" fill="none" stroke="#94a3b8" stroke-width="2.5"/>
  <!-- Trousers & work shoes -->
  <line x1="30" y1="92" x2="30" y2="114" stroke="#334155" stroke-width="7"/>
  <line x1="50" y1="92" x2="50" y2="114" stroke="#334155" stroke-width="7"/>
  <ellipse cx="27" cy="115" rx="8" ry="4" fill="#1e293b"/>
  <ellipse cx="53" cy="115" rx="8" ry="4" fill="#1e293b"/>
</svg>"""
save_svg("char_ufimtsev", svg_char_ufimtsev, cx=40, cy=60)

# Figure 3: char_lazarev (Academician Petr Lazarev)
svg_char_lazarev = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <circle cx="40" cy="24" r="14" fill="#fed7aa"/>
  <!-- Hair & Spectacles -->
  <path d="M 26 24 Q 40 8 54 24 Q 48 14 40 14 Q 32 14 26 24 Z" fill="#475569"/>
  <!-- Scholar round glasses -->
  <circle cx="35" cy="23" r="3.5" fill="none" stroke="#0f172a" stroke-width="1.2"/>
  <circle cx="45" cy="23" r="3.5" fill="none" stroke="#0f172a" stroke-width="1.2"/>
  <line x1="38.5" y1="23" x2="41.5" y2="23" stroke="#0f172a" stroke-width="1"/>
  <path d="M 36 30 Q 40 33 44 30" stroke="#0f172a" stroke-width="1" fill="none"/>
  <!-- Academician Suit & Vest -->
  <path d="M 20 40 L 60 40 L 64 92 L 16 92 Z" fill="#0f172a"/>
  <!-- Vest & bowtie -->
  <polygon points="34,40 40,55 46,40" fill="#334155"/>
  <polygon points="37,42 43,42 41,45 39,45" fill="#0284c7"/>
  <!-- Handheld Magnetic Variometer device -->
  <rect x="58" y="58" width="18" height="22" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <circle cx="67" cy="69" r="6" fill="#0f172a" stroke="#f59e0b" stroke-width="0.8"/>
  <line x1="67" y1="65" x2="67" y2="73" stroke="#ef4444" stroke-width="1.5"/>
  <!-- Legs -->
  <line x1="30" y1="92" x2="30" y2="114" stroke="#0f172a" stroke-width="7"/>
  <line x1="50" y1="92" x2="50" y2="114" stroke="#0f172a" stroke-width="7"/>
  <ellipse cx="27" cy="115" rx="8" ry="4" fill="#020617"/>
  <ellipse cx="53" cy="115" rx="8" ry="4" fill="#020617"/>
</svg>"""
save_svg("char_lazarev", svg_char_lazarev, cx=40, cy=60)

print("6. Generating Interactive Mechanism Sprites...")

# 1. telescope_lens (90x90, cx=45, cy=45)
svg_telescope_lens = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90">
  <!-- Outer brass reticle ring -->
  <circle cx="45" cy="45" r="42" fill="none" stroke="#f59e0b" stroke-width="3"/>
  <circle cx="45" cy="45" r="38" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="3 3"/>
  <!-- Crosshairs -->
  <line x1="45" y1="8" x2="45" y2="82" stroke="#38bdf8" stroke-width="1.2"/>
  <line x1="8" y1="45" x2="82" y2="45" stroke="#38bdf8" stroke-width="1.2"/>
  <!-- Inner focus target circle -->
  <circle cx="45" cy="45" r="14" fill="none" stroke="#22c55e" stroke-width="1.5"/>
  <circle cx="45" cy="45" r="2" fill="#ef4444"/>
  <!-- Angle graduation ticks -->
  <line x1="45" y1="3" x2="45" y2="7" stroke="#f59e0b" stroke-width="2"/>
  <line x1="45" y1="83" x2="45" y2="87" stroke="#f59e0b" stroke-width="2"/>
  <line x1="3" y1="45" x2="7" y2="45" stroke="#f59e0b" stroke-width="2"/>
  <line x1="83" y1="45" x2="87" y2="45" stroke="#f59e0b" stroke-width="2"/>
</svg>"""
save_svg("telescope_lens", svg_telescope_lens, cx=45, cy=45)

# 2. eclipse_target (60x60, cx=30, cy=30)
svg_eclipse_target = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" height="60">
  <defs>
    <radialGradient id="sun_corona" cx="50%" cy="50%" r="50%">
      <stop offset="40%" stop-color="#fef08a" stop-opacity="1"/>
      <stop offset="70%" stop-color="#f59e0b" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <!-- Solar Corona -->
  <circle cx="30" cy="30" r="28" fill="url(#sun_corona)"/>
  <!-- Moon disc blocking the Sun (Eclipse) -->
  <circle cx="28" cy="30" r="18" fill="#020617"/>
  <!-- Shining diamond ring effect -->
  <circle cx="45" cy="22" r="5" fill="#ffffff"/>
  <circle cx="45" cy="22" r="8" fill="#fef08a" opacity="0.6"/>
</svg>"""
save_svg("eclipse_target", svg_eclipse_target, cx=30, cy=30)

# 3. wind_rotor (110x110, cx=55, cy=55) - Ufimtsev's aerodynamic 4-blade rotor
svg_wind_rotor = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 110" width="110" height="110">
  <g transform="translate(55,55)">
    <!-- 4 aerodynamic curved blades -->
    <path d="M -6 -10 L -4 -50 Q 0 -54 4 -50 L 6 -10 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <path d="M 10 -6 L 50 -4 Q 54 0 50 4 L 10 6 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <path d="M 6 10 L 4 50 Q 0 54 -4 50 L -6 10 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <path d="M -10 6 L -50 4 Q -54 0 -50 -4 L -10 -6 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    
    <!-- Central brass hub & bolts -->
    <circle cx="0" cy="0" r="12" fill="#f59e0b" stroke="#78350f" stroke-width="2"/>
    <circle cx="0" cy="0" r="5" fill="#451a03"/>
    <circle cx="0" cy="-8" r="1.5" fill="#fef08a"/>
    <circle cx="8" cy="0" r="1.5" fill="#fef08a"/>
    <circle cx="0" cy="8" r="1.5" fill="#fef08a"/>
    <circle cx="-8" cy="0" r="1.5" fill="#fef08a"/>
  </g>
</svg>"""
save_svg("wind_rotor", svg_wind_rotor, cx=55, cy=55)

# 4. flywheel_meter (90x90, cx=45, cy=45) - Ufimtsev vacuum flywheel gauge
svg_flywheel_meter = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90">
  <!-- Steel vacuum casing -->
  <circle cx="45" cy="45" r="42" fill="#0f172a" stroke="#64748b" stroke-width="3"/>
  <circle cx="45" cy="45" r="36" fill="#1e293b"/>
  <!-- Flywheel disc representation -->
  <circle cx="45" cy="45" r="26" fill="none" stroke="#f59e0b" stroke-width="4" stroke-dasharray="8 6"/>
  <!-- Center hub -->
  <circle cx="45" cy="45" r="8" fill="#38bdf8"/>
  <circle cx="45" cy="45" r="3" fill="#ffffff"/>
  <!-- Dynamic energy scale ticks -->
  <path d="M 20 70 A 32 32 0 1 1 70 70" fill="none" stroke="#22c55e" stroke-width="3" stroke-dasharray="4 4"/>
  <!-- Label -->
  <text x="45" y="65" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#38bdf8" text-anchor="middle">МАХОВИК ВАКУУМНЫЙ</text>
  <text x="45" y="74" font-family="sans-serif" font-size="6" fill="#22c55e" text-anchor="middle">100% ЭНЕРГИЯ</text>
</svg>"""
save_svg("flywheel_meter", svg_flywheel_meter, cx=45, cy=45)

# 5. magneto_sensor (70x70, cx=35, cy=35) - KMA geophysics magnetometer
svg_magneto_sensor = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 70" width="70" height="70">
  <circle cx="35" cy="35" r="32" fill="#0f172a" stroke="#0ea5e9" stroke-width="2.5"/>
  <circle cx="35" cy="35" r="26" fill="#1e293b"/>
  <!-- Compass graduations -->
  <g stroke="#94a3b8" stroke-width="1">
    <line x1="35" y1="11" x2="35" y2="15"/>
    <line x1="35" y1="55" x2="35" y2="59"/>
    <line x1="11" y1="35" x2="15" y2="35"/>
    <line x1="55" y1="35" x2="59" y2="35"/>
  </g>
  <text x="35" y="19" font-family="sans-serif" font-size="7" font-weight="bold" fill="#ef4444" text-anchor="middle">N</text>
  <text x="35" y="55" font-family="sans-serif" font-size="7" font-weight="bold" fill="#38bdf8" text-anchor="middle">S</text>
  <!-- Needle (North = Red, South = Blue) -->
  <polygon points="35,13 38,35 32,35" fill="#ef4444"/>
  <polygon points="35,57 38,35 32,35" fill="#38bdf8"/>
  <circle cx="35" cy="35" r="3.5" fill="#f59e0b"/>
</svg>"""
save_svg("magneto_sensor", svg_magneto_sensor, cx=35, cy=35)

# 6. ore_vein (70x45, cx=35, cy=22) - Magnetite iron ore deposit
svg_ore_vein = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 45" width="70" height="45">
  <!-- Ore crystal clump -->
  <polygon points="10,35 25,12 45,8 62,25 55,42 18,40" fill="#334155" stroke="#64748b" stroke-width="1.5"/>
  <polygon points="25,12 45,8 38,28 20,25" fill="#475569"/>
  <polygon points="45,8 62,25 48,35 38,28" fill="#1e293b"/>
  <!-- Glowing magnetic sparkles -->
  <circle cx="32" cy="18" r="2.5" fill="#38bdf8"/>
  <circle cx="48" cy="22" r="2" fill="#38bdf8"/>
  <circle cx="22" cy="32" r="2" fill="#38bdf8"/>
  <!-- Magnetic pulse ring -->
  <ellipse cx="36" cy="24" rx="28" ry="16" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="3 3"/>
</svg>"""
save_svg("ore_vein", svg_ore_vein, cx=35, cy=22)

print("7. Generating UI, Buttons & Dialog Sprites...")

# 1. dialog_plate (440x80, cx=220, cy=40)
svg_dialog_plate = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 80" width="440" height="80">
  <defs>
    <linearGradient id="dlg_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f172a" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#1e1b4b" stop-opacity="0.95"/>
    </linearGradient>
  </defs>
  <!-- Frame -->
  <rect x="2" y="2" width="436" height="76" rx="8" fill="url(#dlg_bg)" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Inner tech corners -->
  <path d="M 6 16 L 6 6 L 16 6" stroke="#f59e0b" stroke-width="1.5" fill="none"/>
  <path d="M 434 16 L 434 6 L 424 6" stroke="#f59e0b" stroke-width="1.5" fill="none"/>
  <path d="M 6 64 L 6 74 L 16 74" stroke="#f59e0b" stroke-width="1.5" fill="none"/>
  <path d="M 434 64 L 434 74 L 424 74" stroke="#f59e0b" stroke-width="1.5" fill="none"/>
  <!-- Hint at bottom -->
  <text x="420" y="72" font-family="sans-serif" font-size="8" fill="#94a3b8" text-anchor="end">[КЛИКНИТЕ ИЛИ НАЖМИТЕ ПРОБЕЛ ДЛЯ ПРОДОЛЖЕНИЯ ▼]</text>
</svg>"""
save_svg("dialog_plate", svg_dialog_plate, cx=220, cy=40)

# 2. hud_bar (460x26, cx=230, cy=13)
svg_hud_bar = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 26" width="460" height="26">
  <rect x="1" y="1" width="458" height="24" rx="4" fill="#0f172a" fill-opacity="0.9" stroke="#0ea5e9" stroke-width="1"/>
  <!-- Left badge -->
  <rect x="5" y="4" width="75" height="18" rx="2" fill="#0369a1"/>
  <text x="42" y="16" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">МИССИЯ</text>
  <!-- Decorative indicator -->
  <circle cx="445" cy="13" r="5" fill="#22c55e"/>
</svg>"""
save_svg("hud_bar", svg_hud_bar, cx=230, cy=13)

# 3. btn_start (180x40, cx=90, cy=20)
svg_btn_start = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 40" width="180" height="40">
  <defs>
    <linearGradient id="btn_green" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#16a34a"/>
      <stop offset="100%" stop-color="#14532d"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="176" height="36" rx="8" fill="url(#btn_green)" stroke="#4ade80" stroke-width="1.8"/>
  <text x="90" y="24" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#ffffff" text-anchor="middle" letter-spacing="0.5">▶ НАЧАТЬ ЭКСПЕДИЦИЮ</text>
</svg>"""
save_svg("btn_start", svg_btn_start, cx=90, cy=20)

# 4. btn_rules (160x36, cx=80, cy=18)
svg_btn_rules = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 36" width="160" height="36">
  <defs>
    <linearGradient id="btn_blue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0c4a6e"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="156" height="32" rx="6" fill="url(#btn_blue)" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="80" y="22" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">📖 ПРАВИЛА И ЗАДАЧИ</text>
</svg>"""
save_svg("btn_rules", svg_btn_rules, cx=80, cy=18)

# 5. btn_authors (160x36, cx=80, cy=18)
svg_btn_authors = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 36" width="160" height="36">
  <defs>
    <linearGradient id="btn_purple" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#4c1d95"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="156" height="32" rx="6" fill="url(#btn_purple)" stroke="#c084fc" stroke-width="1.5"/>
  <text x="80" y="22" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">★ О ПРОЕКТЕ / АВТОРЫ</text>
</svg>"""
save_svg("btn_authors", svg_btn_authors, cx=80, cy=18)

# 6. btn_opt_a (340x32, cx=170, cy=16)
svg_btn_opt_a = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 32" width="340" height="32">
  <rect x="1" y="1" width="338" height="30" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <rect x="4" y="4" width="24" height="24" rx="4" fill="#0284c7"/>
  <text x="16" y="20" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">A</text>
  <text x="36" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#e2e8f0">[ ВАРИАНТ А ]</text>
</svg>"""
save_svg("btn_opt_a", svg_btn_opt_a, cx=170, cy=16)

# 7. btn_opt_b (340x32, cx=170, cy=16)
svg_btn_opt_b = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 32" width="340" height="32">
  <rect x="1" y="1" width="338" height="30" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <rect x="4" y="4" width="24" height="24" rx="4" fill="#0284c7"/>
  <text x="16" y="20" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">B</text>
  <text x="36" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#e2e8f0">[ ВАРИАНТ B ]</text>
</svg>"""
save_svg("btn_opt_b", svg_btn_opt_b, cx=170, cy=16)

# 8. btn_opt_c (340x32, cx=170, cy=16)
svg_btn_opt_c = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 32" width="340" height="32">
  <rect x="1" y="1" width="338" height="30" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
  <rect x="4" y="4" width="24" height="24" rx="4" fill="#0284c7"/>
  <text x="16" y="20" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">C</text>
  <text x="36" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#e2e8f0">[ ВАРИАНТ C ]</text>
</svg>"""
save_svg("btn_opt_c", svg_btn_opt_c, cx=170, cy=16)

# 9. btn_brake (120x34, cx=60, cy=17)
svg_btn_brake = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 34" width="120" height="34">
  <rect x="1" y="1" width="118" height="32" rx="6" fill="#7f1d1d" stroke="#ef4444" stroke-width="1.5"/>
  <text x="60" y="21" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#fee2e2" text-anchor="middle">⚠ ТОРМОЗ РОТОРА</text>
</svg>"""
save_svg("btn_brake", svg_btn_brake, cx=60, cy=17)

# 10. btn_gear (120x34, cx=60, cy=17)
svg_btn_gear = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 34" width="120" height="34">
  <rect x="1" y="1" width="118" height="32" rx="6" fill="#0c4a6e" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="60" y="21" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#e0f2fe" text-anchor="middle">⚡ МАХОВИК В СЕТЬ</text>
</svg>"""
save_svg("btn_gear", svg_btn_gear, cx=60, cy=17)

# 11. fx_spark (60x60, cx=30, cy=30)
svg_fx_spark = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" height="60">
  <path d="M 30 10 L 33 26 L 49 30 L 33 34 L 30 50 L 27 34 L 11 30 L 27 26 Z" fill="#fbbf24"/>
  <circle cx="30" cy="30" r="4" fill="#ffffff"/>
  <circle cx="18" cy="18" r="2" fill="#38bdf8"/>
  <circle cx="42" cy="18" r="2" fill="#38bdf8"/>
  <circle cx="18" cy="42" r="2" fill="#38bdf8"/>
  <circle cx="42" cy="42" r="2" fill="#38bdf8"/>
</svg>"""
save_svg("fx_spark", svg_fx_spark, cx=30, cy=30)

# 12. fx_medal (80x80, cx=40, cy=40) - Gold Demidov Medal
svg_fx_medal = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
  <defs>
    <linearGradient id="gold_disc" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
  </defs>
  <!-- Red Imperial ribbon loop at top -->
  <polygon points="32,4 40,16 48,4" fill="#dc2626"/>
  <!-- Gold Medal rim -->
  <circle cx="40" cy="44" r="32" fill="url(#gold_disc)" stroke="#78350f" stroke-width="2"/>
  <circle cx="40" cy="44" r="28" fill="none" stroke="#fef08a" stroke-width="1.2" stroke-dasharray="2 2"/>
  <!-- Laurel wreath inside -->
  <circle cx="40" cy="44" r="22" fill="#d97706"/>
  <!-- Imperial Russian Academy Profile / Eagle emblem -->
  <text x="40" y="38" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#fef08a" text-anchor="middle">ДЕМИДОВСКАЯ</text>
  <text x="40" y="46" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#fef08a" text-anchor="middle">ПРЕМИЯ</text>
  <text x="40" y="55" font-family="sans-serif" font-size="6" fill="#fef08a" text-anchor="middle">★ 1858 ★</text>
</svg>"""
save_svg("fx_medal", svg_fx_medal, cx=40, cy=40)

# Save manifest to disk
with open("/home/dima/Projects/hackathon/scratch_project/assets_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"All {len(manifest)} assets generated and saved to manifest!")
