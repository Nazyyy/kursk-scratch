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

print("Asset generator ready. Proceeding with audio synthesis...")

# 1. snd_click: high-precision glass tap
def gen_click(t, dur):
    return 0.7 * math.sin(2 * math.pi * 1400 * t) * math.exp(-t * 90)
synth_wav("snd_click", 0.05, gen_click)

# 2. snd_teleport: refined sci-fi quantum pulse
def gen_teleport(t, dur):
    p = t / dur
    freq = 280 + 1200 * (p**1.5)
    env = math.sin(math.pi * p)
    vibrato = 15 * math.sin(2 * math.pi * 24 * t)
    return 0.65 * math.sin(2 * math.pi * (freq + vibrato) * t) * env
synth_wav("snd_teleport", 0.45, gen_teleport)

# 3. snd_focus: crisp dual mechanical optical shutter
def gen_focus(t, dur):
    c1 = math.sin(2 * math.pi * 1850 * t) * math.exp(-t * 110)
    t2 = t - 0.05
    c2 = (math.sin(2 * math.pi * 2400 * t2) * math.exp(-t2 * 110)) if t2 > 0 else 0
    return 0.75 * (c1 + c2)
synth_wav("snd_focus", 0.12, gen_focus)

# 4. snd_wind: acoustic turbine resonance + air stream
def gen_wind(t, dur):
    p = t / dur
    hum = 0.4 * math.sin(2 * math.pi * 110 * t) + 0.25 * math.sin(2 * math.pi * 220 * t)
    stream = 0.2 * math.sin(2 * math.pi * 380 * t) * (0.6 + 0.4 * math.sin(2 * math.pi * 4 * t))
    return (hum + stream) * math.sin(math.pi * p)
synth_wav("snd_wind", 0.7, gen_wind)

# 5. snd_magnet: sharp geophysical sonar tick
def gen_magnet(t, dur):
    sub = t % 0.06
    env = math.exp(-sub * 80)
    return 0.7 * math.sin(2 * math.pi * 960 * t) * env
synth_wav("snd_magnet", 0.28, gen_magnet)

# 6. snd_correct: acoustic bell chord (C5 - G5 - C6)
def gen_correct(t, dur):
    p = t / dur
    c5 = math.sin(2 * math.pi * 523.25 * t) * math.exp(-t * 7)
    g5 = math.sin(2 * math.pi * 783.99 * t) * math.exp(-t * 6)
    c6 = math.sin(2 * math.pi * 1046.50 * t) * math.exp(-t * 5)
    return 0.4 * (c5 + g5 + c6)
synth_wav("snd_correct", 0.45, gen_correct)

# 7. snd_wrong: muted low damp
def gen_wrong(t, dur):
    f = 140 - 40 * (t / dur)
    return 0.5 * math.sin(2 * math.pi * f * t) * math.exp(-t * 10)
synth_wav("snd_wrong", 0.2, gen_wrong)

# 8. snd_fanfare: classical grand academic fanfare
def gen_fanfare(t, dur):
    if t < 0.2:
        f = 523.25
    elif t < 0.38:
        f = 659.25
    elif t < 0.58:
        f = 783.99
    elif t < 0.8:
        f = 659.25
    else:
        f = 1046.50
    decay = 1.0 if t < 0.8 else math.exp(-(t - 0.8) * 4)
    tone = math.sin(2 * math.pi * f * t) + 0.35 * math.sin(2 * math.pi * 2 * f * t)
    return 0.6 * tone * decay
synth_wav("snd_fanfare", 1.1, gen_fanfare)

print("Audio assets generated.")

print("2. Generating Liquid Glass Backdrops...")

# 1. bg_title: Liquid Glass Industrial CAD Control Deck
svg_bg_title = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="deck_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#040711"/>
      <stop offset="60%" stop-color="#0b1120"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="glass_panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e293b" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.88"/>
    </linearGradient>
    <linearGradient id="gold_accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#fbbf24"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#deck_bg)"/>

  <!-- Precision CAD Grid -->
  <g stroke="#38bdf8" stroke-width="0.5" stroke-opacity="0.08">
    <line x1="0" y1="30" x2="480" y2="30"/><line x1="0" y1="60" x2="480" y2="60"/>
    <line x1="0" y1="90" x2="480" y2="90"/><line x1="0" y1="120" x2="480" y2="120"/>
    <line x1="0" y1="150" x2="480" y2="150"/><line x1="0" y1="180" x2="480" y2="180"/>
    <line x1="0" y1="210" x2="480" y2="210"/><line x1="0" y1="240" x2="480" y2="240"/>
    <line x1="0" y1="270" x2="480" y2="270"/><line x1="0" y1="300" x2="480" y2="300"/>
    <line x1="0" y1="330" x2="480" y2="330"/>
    <line x1="40" y1="0" x2="40" y2="360"/><line x1="80" y1="0" x2="80" y2="360"/>
    <line x1="120" y1="0" x2="120" y2="360"/><line x1="160" y1="0" x2="160" y2="360"/>
    <line x1="200" y1="0" x2="200" y2="360"/><line x1="240" y1="0" x2="240" y2="360"/>
    <line x1="280" y1="0" x2="280" y2="360"/><line x1="320" y1="0" x2="320" y2="360"/>
    <line x1="360" y1="0" x2="360" y2="360"/><line x1="400" y1="0" x2="400" y2="360"/>
    <line x1="440" y1="0" x2="440" y2="360"/>
  </g>

  <!-- Technical axes crosshairs -->
  <g stroke="#38bdf8" stroke-width="1" stroke-opacity="0.3">
    <line x1="235" y1="180" x2="245" y2="180"/>
    <line x1="240" y1="175" x2="240" y2="185"/>
  </g>

  <!-- Main Hero Liquid Glass Card -->
  <g transform="translate(40, 36)">
    <rect width="400" height="98" rx="8" fill="url(#glass_panel)" stroke="#38bdf8" stroke-width="0.8" stroke-opacity="0.4"/>
    <!-- Specular highlight line on top edge -->
    <line x1="2" y1="1" x2="398" y2="1" stroke="#ffffff" stroke-width="1" stroke-opacity="0.6"/>
    <!-- Top badge -->
    <rect x="12" y="10" width="138" height="15" rx="3" fill="#0369a1" fill-opacity="0.4" stroke="#0ea5e9" stroke-width="0.6"/>
    <text x="81" y="21" font-family="sans-serif" font-size="8" font-weight="bold" fill="#38bdf8" text-anchor="middle" letter-spacing="1">IT-ЦОПП • КУРСКАЯ ОБЛАСТЬ</text>
    
    <!-- Title -->
    <text x="12" y="52" font-family="sans-serif" font-size="20" font-weight="900" fill="#f8fafc" letter-spacing="0.5">АРХИВ ПЕРВОПРОХОДЦЕВ</text>
    <!-- Subtitle -->
    <text x="12" y="70" font-family="sans-serif" font-size="11" font-weight="600" fill="url(#gold_accent)" letter-spacing="0.3">Инженерная летопись науки и техники Соловьиного Края</text>
    
    <!-- Telemetry right column -->
    <g font-family="monospace" font-size="8" fill="#64748b" text-anchor="end">
      <text x="388" y="22">LOC: 51°43′N 36°11′E</text>
      <text x="388" y="38">SYS: CHRONO-CAD v4.6</text>
      <text x="388" y="54">CLUSTERS: OPTICS | WIND | CORE</text>
      <text x="388" y="70">STATUS: READY FOR CADET</text>
    </g>
  </g>

  <!-- Central Schematic Rings (Engineering Reticle) -->
  <circle cx="240" cy="225" r="75" fill="none" stroke="#334155" stroke-width="1"/>
  <circle cx="240" cy="225" r="50" fill="none" stroke="#0284c7" stroke-width="0.8" stroke-dasharray="4 4" stroke-opacity="0.5"/>
  <circle cx="240" cy="225" r="25" fill="none" stroke="#f59e0b" stroke-width="0.6" stroke-opacity="0.4"/>
  <!-- Minimalist engineering nightingale glyph in center -->
  <path d="M 230 220 Q 240 212 250 220 Q 256 226 252 232 Q 244 235 236 229 Z M 250 220 L 260 222 L 251 224 Z" fill="#38bdf8" opacity="0.75"/>

  <!-- Footer Specs -->
  <rect x="20" y="336" width="440" height="1" fill="#334155"/>
  <text x="240" y="348" font-family="sans-serif" font-size="8.5" fill="#64748b" text-anchor="middle" letter-spacing="0.5">ОТКРЫТЫЙ РЕГИОНАЛЬНЫЙ КОНКУРС «IT-ЦОПП» ДЛЯ 6–11 КЛАССОВ</text>
</svg>"""
save_svg("bg_title", svg_bg_title)

# 2. bg_semenov: 1853 Semenov Observatory (Architectural Timber & Nocturnal Meridian)
svg_bg_semenov = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="night_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#02040a"/>
      <stop offset="50%" stop-color="#090d1c"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="brass_metal" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#b45309"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#78350f"/>
    </linearGradient>
  </defs>
  <!-- Night sky through the open observation slit -->
  <rect width="480" height="360" fill="url(#night_sky)"/>

  <!-- Constellations & Nocturnal Stars -->
  <g fill="#ffffff">
    <circle cx="70" cy="50" r="1.4" opacity="0.9"/>
    <circle cx="110" cy="75" r="1.1" opacity="0.7"/>
    <circle cx="150" cy="40" r="1.8" opacity="0.95"/>
    <circle cx="210" cy="65" r="1.2" opacity="0.8"/>
    <circle cx="270" cy="45" r="1.5" opacity="0.9"/>
    <circle cx="340" cy="35" r="2.0" opacity="1"/>
    <circle cx="380" cy="70" r="1.3" opacity="0.85"/>
    <circle cx="420" cy="50" r="1.6" opacity="0.9"/>
    <circle cx="170" cy="110" r="1.2" opacity="0.7"/>
  </g>
  <!-- Astronomical Ursa Major lines -->
  <g stroke="#38bdf8" stroke-width="0.6" stroke-dasharray="2 3" opacity="0.4">
    <line x1="270" y1="45" x2="310" y2="55"/>
    <line x1="310" y1="55" x2="340" y2="35"/>
    <line x1="340" y1="35" x2="370" y2="45"/>
    <line x1="370" y1="45" x2="380" y2="70"/>
    <line x1="380" y1="70" x2="350" y2="80"/>
    <line x1="350" y1="80" x2="340" y2="35"/>
  </g>

  <!-- Architectural Dome Timber Framing -->
  <path d="M 0 0 L 100 0 L 100 240 L 0 250 Z" fill="#181310"/>
  <path d="M 380 0 L 480 0 L 480 250 L 380 240 Z" fill="#181310"/>
  <path d="M 100 0 Q 240 45 380 0 L 380 18 Q 240 60 100 18 Z" fill="#291d15"/>
  <!-- Beams -->
  <line x1="100" y1="0" x2="100" y2="240" stroke="#3d2a1e" stroke-width="6"/>
  <line x1="380" y1="0" x2="380" y2="240" stroke="#3d2a1e" stroke-width="6"/>

  <!-- Floor Pavement -->
  <rect x="0" y="240" width="480" height="120" fill="#17120e"/>
  <line x1="0" y1="240" x2="480" y2="240" stroke="#3d2a1e" stroke-width="2"/>
  <line x1="0" y1="275" x2="480" y2="275" stroke="#261911" stroke-width="1.5"/>
  <line x1="0" y1="315" x2="480" y2="315" stroke="#261911" stroke-width="1.5"/>

  <!-- Astronomical Observation Desk on Left -->
  <g transform="translate(15, 230)">
    <rect width="85" height="55" rx="3" fill="#2d1c12" stroke="#452a1a" stroke-width="1"/>
    <!-- Antique manuscripts -->
    <rect x="8" y="-6" width="34" height="6" rx="1" fill="#fef08a" opacity="0.85"/>
    <rect x="46" y="-8" width="28" height="8" rx="1" fill="#e2e8f0" opacity="0.9"/>
    <!-- Brass Astrolabe -->
    <circle cx="60" cy="-18" r="9" fill="none" stroke="url(#brass_metal)" stroke-width="1.5"/>
    <line x1="60" y1="-26" x2="60" y2="-10" stroke="url(#brass_metal)" stroke-width="1"/>
    <line x1="52" y1="-18" x2="68" y2="-18" stroke="url(#brass_metal)" stroke-width="1"/>
  </g>

  <!-- Liquid Glass Header Tag -->
  <g transform="translate(80, 8)">
    <rect width="320" height="22" rx="4" fill="#0f172a" fill-opacity="0.8" stroke="#38bdf8" stroke-width="0.75" stroke-opacity="0.4"/>
    <line x1="1" y1="1" x2="319" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="160" y="15" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fef08a" text-anchor="middle" letter-spacing="1">КУРСК • 1853 г. • ОБСЕРВАТОРИЯ Ф.А. СЕМЁНОВА</text>
  </g>

  <!-- Technical Ephemeris Readout in Corner -->
  <g font-family="monospace" font-size="7.5" fill="#94a3b8" opacity="0.7">
    <text x="12" y="20">RA: 13h 47m</text>
    <text x="12" y="32">DEC: +49°18′</text>
    <text x="12" y="44">SAROS: 124</text>
  </g>
</svg>"""
save_svg("bg_semenov", svg_bg_semenov)

# 3. bg_ufimtsev: 1931 Ufimtsev Workshop & Aerodynamic Wind Tower
svg_bg_ufimtsev = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="slate_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
    <linearGradient id="brick_facade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3f1319"/>
      <stop offset="100%" stop-color="#24080d"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#slate_sky)"/>

  <!-- Streamlined aerodynamic wind vectors -->
  <g stroke="#ffffff" stroke-width="0.75" stroke-opacity="0.15" stroke-dasharray="8 6">
    <line x1="0" y1="50" x2="480" y2="45"/>
    <line x1="0" y1="90" x2="480" y2="82"/>
    <line x1="0" y1="130" x2="480" y2="125"/>
  </g>

  <!-- Street ground pavement -->
  <rect x="0" y="240" width="480" height="120" fill="#1e293b"/>
  <line x1="0" y1="240" x2="480" y2="240" stroke="#64748b" stroke-width="1.5"/>

  <!-- Ufimtsev Historic Workshop Facade on Left -->
  <g transform="translate(0, 115)">
    <rect width="165" height="125" fill="url(#brick_facade)" stroke="#4c1d24" stroke-width="1"/>
    <!-- Workshop windows -->
    <rect x="25" y="30" width="40" height="55" fill="#0f172a" stroke="#d97706" stroke-width="1.5"/>
    <line x1="45" y1="30" x2="45" y2="85" stroke="#d97706" stroke-width="1"/>
    <line x1="25" y1="55" x2="65" y2="55" stroke="#d97706" stroke-width="1"/>
    <!-- Technical signboard -->
    <rect x="15" y="8" width="135" height="15" rx="2" fill="#0f172a" stroke="#64748b" stroke-width="0.8"/>
    <text x="82" y="19" font-family="sans-serif" font-size="7.5" font-weight="bold" fill="#f8fafc" text-anchor="middle" letter-spacing="0.5">МАСТЕРСКАЯ А.Г. УФИМЦЕВА • 1931</text>
  </g>

  <!-- Precision Steel Lattice Tower (Ветроэлектростанция ВЭС-1) -->
  <polygon points="325,45 345,45 370,240 300,240" fill="#0f172a" stroke="#475569" stroke-width="1.2"/>
  <g stroke="#94a3b8" stroke-width="1" opacity="0.6">
    <line x1="325" y1="45" x2="370" y2="240"/>
    <line x1="345" y1="45" x2="300" y2="240"/>
    <line x1="320" y1="80" x2="350" y2="80"/>
    <line x1="315" y1="120" x2="355" y2="120"/>
    <line x1="310" y1="160" x2="360" y2="160"/>
    <line x1="305" y1="200" x2="365" y2="200"/>
  </g>

  <!-- Vintage Street Lantern connected to electric cable -->
  <rect x="435" y="170" width="4" height="75" fill="#0f172a"/>
  <circle cx="437" cy="165" r="10" fill="#fef08a" opacity="0.7"/>
  <circle cx="437" cy="165" r="4" fill="#ffffff"/>
  <!-- Cable to workshop -->
  <path d="M 335 55 Q 380 90 435 165" fill="none" stroke="#0ea5e9" stroke-width="1" stroke-dasharray="3 2" opacity="0.6"/>

  <!-- Liquid Glass Header -->
  <g transform="translate(60, 8)">
    <rect width="360" height="22" rx="4" fill="#0f172a" fill-opacity="0.82" stroke="#38bdf8" stroke-width="0.75" stroke-opacity="0.4"/>
    <line x1="1" y1="1" x2="359" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="180" y="15" font-family="sans-serif" font-size="9" font-weight="bold" fill="#38bdf8" text-anchor="middle" letter-spacing="1">КУРСК • 1931 г. • ВЕТРОСТАНЦИЯ А.Г. УФИМЦЕВА (ВЭС-1)</text>
  </g>

  <!-- Telemetry specs -->
  <g font-family="monospace" font-size="7.5" fill="#94a3b8" opacity="0.7" text-anchor="end">
    <text x="468" y="24">FLYWHEEL: 3.5 TONS</text>
    <text x="468" y="36">VACUUM: -0.98 BAR</text>
    <text x="468" y="48">PATENT: No. 68</text>
  </g>
</svg>"""
save_svg("bg_ufimtsev", svg_bg_ufimtsev)

# 4. bg_kma_aes: Kursk Magnetic Anomaly & Atomic Cluster (Kurchatov)
svg_bg_kma = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="kma_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0369a1"/>
      <stop offset="60%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#e0f2fe"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#kma_sky)"/>

  <!-- Electromagnetic flux curves of the anomaly -->
  <g stroke="#0284c7" stroke-width="1.2" stroke-dasharray="5 3" opacity="0.4" fill="none">
    <path d="M 30 170 Q 140 20 270 170"/>
    <path d="M 60 170 Q 150 50 240 170"/>
    <path d="M 10 180 Q 160 5 310 180"/>
  </g>

  <!-- Distant Clean Atomic Energy Cluster: Kursk NPP-2 (г. Курчатов) -->
  <g transform="translate(340, 105)">
    <!-- Cooling towers -->
    <path d="M 20 65 Q 23 35 18 10 L 40 10 Q 35 35 38 65 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="1"/>
    <path d="M 48 65 Q 51 35 46 10 L 68 10 Q 63 35 66 65 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="1"/>
    <!-- Reactor building VVER-TOI -->
    <rect x="75" y="25" width="42" height="40" fill="#cbd5e1" stroke="#64748b" stroke-width="1"/>
    <ellipse cx="96" cy="25" rx="16" ry="7" fill="#38bdf8" opacity="0.6"/>
    <!-- Atomic symbol -->
    <circle cx="96" cy="2" r="8" fill="none" stroke="#0284c7" stroke-width="1.2"/>
    <ellipse cx="96" cy="2" rx="12" ry="3.5" fill="none" stroke="#0284c7" stroke-width="0.8" transform="rotate(30 96 2)"/>
    <ellipse cx="96" cy="2" rx="12" ry="3.5" fill="none" stroke="#0284c7" stroke-width="0.8" transform="rotate(-30 96 2)"/>
  </g>

  <!-- Stepped Geological Terraces of the KMA Iron Ore Open Pit -->
  <polygon points="0,170 320,170 290,195 0,195" fill="#7c2d12"/>
  <polygon points="0,195 480,180 450,225 0,225" fill="#5c1d0e"/>
  <polygon points="0,225 480,225 430,260 0,260" fill="#3b1207"/>
  <polygon points="0,260 480,260 480,360 0,360" fill="#0f172a"/>

  <!-- High-grade Magnetite Quartzite layer -->
  <polygon points="70,268 330,268 310,312 50,312" fill="#1e293b" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="3 2"/>
  <text x="180" y="295" font-family="monospace" font-size="8.5" font-weight="bold" fill="#38bdf8" letter-spacing="1">ПЛАСТ МАГНЕТИТА Fe3O4 • КМА</text>

  <!-- Liquid Glass Header -->
  <g transform="translate(60, 8)">
    <rect width="360" height="22" rx="4" fill="#0f172a" fill-opacity="0.85" stroke="#0284c7" stroke-width="0.75" stroke-opacity="0.4"/>
    <line x1="1" y1="1" x2="359" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="180" y="15" font-family="sans-serif" font-size="9" font-weight="bold" fill="#38bdf8" text-anchor="middle" letter-spacing="1">КУРСКИЙ КРАЙ • КМА И ЭНЕРГИЯ АТОМА (г. КУРЧАТОВ)</text>
  </g>

  <g font-family="monospace" font-size="7.5" fill="#0369a1" opacity="0.85">
    <text x="12" y="22">MAG_IND: 42.8 µT</text>
    <text x="12" y="34">ORE: 30+ BILLION TONS</text>
    <text x="12" y="46">PWR: VVER-TOI 1255 MWe</text>
  </g>
</svg>"""
save_svg("bg_kma_aes", svg_bg_kma)

# 5. bg_hall_of_fame: Grand Engineering Archive & Register of Kursk Pioneers
svg_bg_hall = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360">
  <defs>
    <linearGradient id="archive_wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0f19"/>
      <stop offset="50%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#1f2937"/>
    </linearGradient>
    <linearGradient id="steel_gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="50%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#archive_wall)"/>

  <!-- Precision architectural floor with perspective reflection -->
  <rect x="0" y="240" width="480" height="120" fill="#0f172a"/>
  <polygon points="175,240 305,240 340,360 140,360" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>
  <line x1="240" y1="240" x2="240" y2="360" stroke="#475569" stroke-width="0.8" stroke-dasharray="3 3"/>

  <!-- Minimalist Neoclassical Fluted Columns -->
  <g fill="#1e293b" stroke="#334155" stroke-width="1">
    <rect x="18" y="25" width="22" height="215"/>
    <rect x="14" y="22" width="30" height="6" fill="#f59e0b"/>
    <rect x="14" y="238" width="30" height="6" fill="#f59e0b"/>

    <rect x="440" y="25" width="22" height="215"/>
    <rect x="436" y="22" width="30" height="6" fill="#f59e0b"/>
    <rect x="436" y="238" width="30" height="6" fill="#f59e0b"/>
  </g>

  <!-- Three Liquid Glass Architectural Portrait Modules -->
  <!-- 1. Semenov -->
  <g transform="translate(56, 50)">
    <rect width="96" height="128" rx="6" fill="#0f172a" fill-opacity="0.8" stroke="url(#steel_gold)" stroke-width="1.2"/>
    <line x1="1" y1="1" x2="95" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.6"/>
    <circle cx="48" cy="45" r="24" fill="#1e293b"/>
    <path d="M 40 42 Q 48 34 56 42 Q 58 56 48 60 Q 38 56 40 42 Z" fill="#fde047" opacity="0.8"/>
    <text x="48" y="86" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#fde047" text-anchor="middle">Ф.А. СЕМЁНОВ</text>
    <text x="48" y="98" font-family="sans-serif" font-size="7" fill="#94a3b8" text-anchor="middle">1794–1860</text>
    <text x="48" y="112" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#38bdf8" text-anchor="middle">ЗОЛОТАЯ МЕДАЛЬ РАН</text>
  </g>

  <!-- 2. Ufimtsev -->
  <g transform="translate(192, 45)">
    <rect width="96" height="128" rx="6" fill="#0f172a" fill-opacity="0.8" stroke="url(#steel_gold)" stroke-width="1.2"/>
    <line x1="1" y1="1" x2="95" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.6"/>
    <circle cx="48" cy="45" r="24" fill="#1e293b"/>
    <path d="M 40 42 Q 48 34 56 42 Q 58 56 48 60 Q 38 56 40 42 Z" fill="#38bdf8" opacity="0.8"/>
    <text x="48" y="86" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#38bdf8" text-anchor="middle">А.Г. УФИМЦЕВ</text>
    <text x="48" y="98" font-family="sans-serif" font-size="7" fill="#94a3b8" text-anchor="middle">1880–1936</text>
    <text x="48" y="112" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#fde047" text-anchor="middle">ПЕРВАЯ В МИРЕ ВЭС</text>
  </g>

  <!-- 3. Lazarev -->
  <g transform="translate(328, 50)">
    <rect width="96" height="128" rx="6" fill="#0f172a" fill-opacity="0.8" stroke="url(#steel_gold)" stroke-width="1.2"/>
    <line x1="1" y1="1" x2="95" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.6"/>
    <circle cx="48" cy="45" r="24" fill="#1e293b"/>
    <path d="M 40 42 Q 48 34 56 42 Q 58 56 48 60 Q 38 56 40 42 Z" fill="#4ade80" opacity="0.8"/>
    <text x="48" y="86" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#4ade80" text-anchor="middle">П.П. ЛАЗАРЕВ</text>
    <text x="48" y="98" font-family="sans-serif" font-size="7" fill="#94a3b8" text-anchor="middle">1878–1942</text>
    <text x="48" y="112" font-family="sans-serif" font-size="6.5" font-weight="bold" fill="#4ade80" text-anchor="middle">ЭКСПЕДИЦИЯ КМА</text>
  </g>

  <!-- Liquid Glass Header -->
  <g transform="translate(60, 8)">
    <rect width="360" height="22" rx="4" fill="#0f172a" fill-opacity="0.85" stroke="#f59e0b" stroke-width="0.75" stroke-opacity="0.4"/>
    <line x1="1" y1="1" x2="359" y2="1" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="180" y="15" font-family="sans-serif" font-size="9" font-weight="bold" fill="#fde047" text-anchor="middle" letter-spacing="1">ЗАЛ НАУЧНОЙ СЛАВЫ СОЛОВЬИНОГО КРАЯ</text>
  </g>
</svg>"""
save_svg("bg_hall_of_fame", svg_bg_hall)

print("Liquid Glass Backdrops generated.")

print("3. Generating Refined Character Costumes (Liquid Glass & Technical Styling)...")

# Hero 1: hero_copt (Field Engineering Cadet)
svg_hero_copt = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="13" fill="#fbcfe8"/>
  <path d="M 22 22 Q 35 8 48 22 Q 44 12 35 12 Q 26 12 22 22 Z" fill="#1e293b"/>
  <!-- Eyes & Focused Expression -->
  <circle cx="31" cy="21" r="1.8" fill="#0f172a"/>
  <circle cx="39" cy="21" r="1.8" fill="#0f172a"/>
  <path d="M 32 28 Q 35 30 38 28" stroke="#0f172a" stroke-width="1.2" fill="none"/>
  <!-- Field Engineering Jacket (Titanium Blue & Slate) -->
  <path d="M 19 38 L 51 38 L 54 82 L 16 82 Z" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <!-- Liquid Glass Badge -->
  <rect x="22" y="46" width="26" height="14" rx="2" fill="#0369a1" fill-opacity="0.8" stroke="#38bdf8" stroke-width="0.6"/>
  <text x="35" y="56" font-family="sans-serif" font-size="6" font-weight="bold" fill="#ffffff" text-anchor="middle">ЦОПП 46</text>
  <!-- Technical wrist tablet -->
  <rect x="7" y="60" width="8" height="10" rx="1.5" fill="#0284c7" stroke="#38bdf8" stroke-width="0.8"/>
  <circle cx="11" cy="65" r="1.5" fill="#22c55e"/>
  <!-- Boots & Trousers -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#1e293b" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#1e293b" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#0284c7"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#0284c7"/>
</svg>"""
save_svg("hero_copt", svg_hero_copt, cx=35, cy=55)

# Hero 2: hero_astronomer (1853 Scholar & Optical Loupe)
svg_hero_astronomer = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="13" fill="#fbcfe8"/>
  <path d="M 22 22 Q 35 8 48 22 Q 44 12 35 12 Q 26 12 22 22 Z" fill="#451a03"/>
  <!-- Brass spectacles -->
  <circle cx="30" cy="21" r="3.2" fill="none" stroke="#f59e0b" stroke-width="1.2"/>
  <circle cx="40" cy="21" r="3.2" fill="none" stroke="#f59e0b" stroke-width="1.2"/>
  <line x1="33.2" y1="21" x2="36.8" y2="21" stroke="#f59e0b" stroke-width="1"/>
  <!-- Velvet dark coat with copper buttons -->
  <path d="M 18 38 L 52 38 L 56 84 L 14 84 Z" fill="#1e1b4b" stroke="#64748b" stroke-width="0.8"/>
  <circle cx="35" cy="52" r="1.5" fill="#f59e0b"/>
  <circle cx="35" cy="64" r="1.5" fill="#f59e0b"/>
  <!-- Celestial chart in hand -->
  <rect x="4" y="60" width="14" height="20" rx="1" fill="#fef08a" stroke="#b45309" stroke-width="0.8"/>
  <!-- Boots -->
  <line x1="26" y1="84" x2="26" y2="102" stroke="#0f172a" stroke-width="6"/>
  <line x1="44" y1="84" x2="44" y2="102" stroke="#0f172a" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#3f1a08"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#3f1a08"/>
</svg>"""
save_svg("hero_astronomer", svg_hero_astronomer, cx=35, cy=55)

# Hero 3: hero_aviator (1931 Technician with Vernier Caliper)
svg_hero_aviator = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="24" r="13" fill="#fbcfe8"/>
  <!-- Aviator leather helmet & goggles -->
  <path d="M 21 24 Q 35 10 49 24 L 49 32 L 44 32 L 44 26 Q 35 16 26 26 L 26 32 L 21 32 Z" fill="#78350f"/>
  <rect x="24" y="14" width="10" height="6" rx="2" fill="#0284c7" stroke="#f59e0b" stroke-width="1"/>
  <rect x="36" y="14" width="10" height="6" rx="2" fill="#0284c7" stroke="#f59e0b" stroke-width="1"/>
  <line x1="34" y1="17" x2="36" y2="17" stroke="#78350f" stroke-width="1.5"/>
  <!-- Brown flight leather coat with sheepskin collar -->
  <path d="M 18 40 L 52 40 L 54 82 L 16 82 Z" fill="#9a3412" stroke="#451a03" stroke-width="1"/>
  <!-- Steel tool in hand -->
  <path d="M 8 55 L 12 75" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
  <!-- Boots -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#1e293b" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#1e293b" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#0f172a"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#0f172a"/>
</svg>"""
save_svg("hero_aviator", svg_hero_aviator, cx=35, cy=55)

# Hero 4: hero_physicist (KMA / Atomic Technician)
svg_hero_physicist = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="13" fill="#fbcfe8"/>
  <!-- Safety Helmet with optical HUD visor -->
  <path d="M 21 20 Q 35 8 49 20 L 49 24 L 21 24 Z" fill="#ffffff" stroke="#94a3b8" stroke-width="1"/>
  <rect x="24" y="18" width="22" height="5" rx="1.5" fill="#06b6d4" opacity="0.9"/>
  <!-- Technical lab cleanroom suit -->
  <path d="M 18 38 L 52 38 L 54 82 L 16 82 Z" fill="#f8fafc" stroke="#94a3b8" stroke-width="1"/>
  <rect x="16" y="65" width="38" height="5" fill="#0284c7"/>
  <!-- Sensor tablet -->
  <rect x="6" y="58" width="10" height="15" rx="1.5" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <circle cx="11" cy="65" r="1.5" fill="#22c55e"/>
  <!-- Boots -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#e2e8f0" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#e2e8f0" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#334155"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#334155"/>
</svg>"""
save_svg("hero_physicist", svg_hero_physicist, cx=35, cy=55)

# Hero 5: hero_triumph (Pioneer with Gold Demidov Medal)
svg_hero_triumph = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 110" width="70" height="110">
  <circle cx="35" cy="22" r="13" fill="#fbcfe8"/>
  <path d="M 22 22 Q 35 8 48 22 Q 44 12 35 12 Q 26 12 22 22 Z" fill="#1e293b"/>
  <!-- Dignified academic blazer -->
  <path d="M 18 38 L 52 38 L 54 82 L 16 82 Z" fill="#0f172a" stroke="#f59e0b" stroke-width="1"/>
  <!-- Red Imperial Ribbon & Gold Medal -->
  <line x1="29" y1="38" x2="35" y2="52" stroke="#dc2626" stroke-width="2.5"/>
  <line x1="41" y1="38" x2="35" y2="52" stroke="#dc2626" stroke-width="2.5"/>
  <circle cx="35" cy="56" r="6" fill="#fbbf24" stroke="#b45309" stroke-width="1"/>
  <!-- Certificate roll in hand -->
  <rect x="50" y="52" width="16" height="24" rx="1" fill="#fef08a" stroke="#b45309" stroke-width="0.8"/>
  <!-- Boots -->
  <line x1="26" y1="82" x2="26" y2="102" stroke="#0f172a" stroke-width="6"/>
  <line x1="44" y1="82" x2="44" y2="102" stroke="#0f172a" stroke-width="6"/>
  <ellipse cx="23" cy="104" rx="7" ry="4" fill="#020617"/>
  <ellipse cx="47" cy="104" rx="7" ry="4" fill="#020617"/>
</svg>"""
save_svg("hero_triumph", svg_hero_triumph, cx=35, cy=55)

print("4. Generating Cadastral Drone «Соловей-46»...")

# Kursik 1: kursik_hover (Aerodynamic Carbon Drone)
svg_kursik_hover = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <!-- Aerodynamic fuselage -->
  <ellipse cx="30" cy="24" rx="18" ry="10" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
  <!-- Specular highlight line -->
  <path d="M 16 22 Q 30 16 44 22" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.6" fill="none"/>
  <!-- Carbon-fiber wings -->
  <polygon points="18,22 28,8 36,22" fill="#1e293b" stroke="#0284c7" stroke-width="1"/>
  <!-- Sensor Head / Optics -->
  <circle cx="46" cy="20" r="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <circle cx="48" cy="18" r="3.5" fill="#06b6d4"/>
  <circle cx="49" cy="17" r="1.2" fill="#ffffff"/>
  <!-- Precision telemetry probe -->
  <polygon points="54,18 62,20 54,22" fill="#f59e0b"/>
  <!-- Stabilizer tail fins -->
  <polygon points="12,24 2,19 8,26" fill="#0284c7"/>
  <polygon points="12,26 4,31 8,28" fill="#0369a1"/>
  <!-- Miniature telemetry antenna -->
  <line x1="44" y1="12" x2="44" y2="6" stroke="#38bdf8" stroke-width="1.2"/>
  <circle cx="44" cy="5" r="1.8" fill="#38bdf8"/>
</svg>"""
save_svg("kursik_hover", svg_kursik_hover, cx=32, cy=25)

# Kursik 2: kursik_talk (Acoustic Communicator Active)
svg_kursik_talk = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <ellipse cx="30" cy="24" rx="18" ry="10" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
  <polygon points="18,22 28,6 36,22" fill="#1e293b" stroke="#0284c7" stroke-width="1"/>
  <circle cx="46" cy="20" r="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <circle cx="48" cy="18" r="3.5" fill="#38bdf8"/>
  <polygon points="54,18 62,20 54,22" fill="#f59e0b"/>
  <polygon points="12,24 2,19 8,26" fill="#0284c7"/>
  <!-- Acoustic communication rings -->
  <path d="M 58 14 Q 63 20 58 26" stroke="#38bdf8" stroke-width="1.2" fill="none"/>
  <path d="M 61 11 Q 67 20 61 29" stroke="#38bdf8" stroke-width="0.8" fill="none" opacity="0.6"/>
</svg>"""
save_svg("kursik_talk", svg_kursik_talk, cx=32, cy=25)

# Kursik 3: kursik_scan (Precision Downward LiDAR Cone)
svg_kursik_scan = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <!-- Laser scanner beam cone -->
  <polygon points="30,28 10,50 50,50" fill="#38bdf8" fill-opacity="0.25"/>
  <ellipse cx="30" cy="24" rx="18" ry="10" fill="#0f172a" stroke="#22c55e" stroke-width="1.2"/>
  <polygon points="18,22 28,10 36,22" fill="#1e293b" stroke="#22c55e" stroke-width="1"/>
  <circle cx="46" cy="20" r="8" fill="#1e293b" stroke="#22c55e" stroke-width="1"/>
  <circle cx="48" cy="18" r="3.5" fill="#22c55e"/>
  <polygon points="54,18 62,20 54,22" fill="#f59e0b"/>
  <polygon points="12,24 2,19 8,26" fill="#22c55e"/>
</svg>"""
save_svg("kursik_scan", svg_kursik_scan, cx=32, cy=25)

# Kursik 4: kursik_celebrate (Mission Accomplished)
svg_kursik_celebrate = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 50" width="64" height="50">
  <!-- Confirmation aura -->
  <circle cx="32" cy="24" r="22" fill="none" stroke="#22c55e" stroke-width="0.8" stroke-dasharray="3 3"/>
  <ellipse cx="30" cy="24" rx="18" ry="10" fill="#0f172a" stroke="#fbbf24" stroke-width="1.2"/>
  <!-- Wings high -->
  <polygon points="22,20 18,4 30,14" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <polygon points="32,20 40,4 44,16" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
  <circle cx="46" cy="20" r="8" fill="#1e293b" stroke="#fbbf24" stroke-width="1"/>
  <circle cx="48" cy="18" r="3.5" fill="#fbbf24"/>
  <polygon points="54,18 62,20 54,22" fill="#fbbf24"/>
</svg>"""
save_svg("kursik_celebrate", svg_kursik_celebrate, cx=32, cy=25)

print("5. Generating Historical Figures in Engraving Realism...")

# Fedor Semenov
svg_char_semenov = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <circle cx="40" cy="24" r="14" fill="#fed7aa"/>
  <path d="M 26 24 Q 40 8 54 24 Q 48 14 40 14 Q 32 14 26 24 Z" fill="#94a3b8"/>
  <path d="M 28 28 Q 40 44 52 28 Q 48 38 40 38 Q 32 38 28 28 Z" fill="#cbd5e1"/>
  <circle cx="35" cy="22" r="1.8" fill="#1e293b"/>
  <circle cx="45" cy="22" r="1.8" fill="#1e293b"/>
  <!-- Dignified 19th Century Dark Merchant Frock Coat -->
  <path d="M 20 40 L 60 40 L 66 95 L 14 95 Z" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <!-- Velvet lapels with gold trim -->
  <polygon points="32,40 40,62 48,40" fill="#0f172a"/>
  <line x1="32" y1="40" x2="40" y2="62" stroke="#f59e0b" stroke-width="0.8"/>
  <line x1="48" y1="40" x2="40" y2="62" stroke="#f59e0b" stroke-width="0.8"/>
  <!-- Brass Hand Refractor in hand -->
  <polygon points="62,60 76,40 78,43 64,63" fill="#f59e0b" stroke="#b45309" stroke-width="1"/>
  <!-- Published Work 'Таблицы затмений' -->
  <rect x="8" y="65" width="18" height="24" rx="1" fill="#78350f" stroke="#f59e0b" stroke-width="0.8"/>
  <!-- Boots -->
  <line x1="30" y1="95" x2="30" y2="114" stroke="#0f172a" stroke-width="7"/>
  <line x1="50" y1="95" x2="50" y2="114" stroke="#0f172a" stroke-width="7"/>
  <ellipse cx="27" cy="115" rx="8" ry="4" fill="#0f172a"/>
  <ellipse cx="53" cy="115" rx="8" ry="4" fill="#0f172a"/>
</svg>"""
save_svg("char_semenov", svg_char_semenov, cx=40, cy=60)

# Anatoly Ufimtsev
svg_char_ufimtsev = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <circle cx="40" cy="24" r="14" fill="#fed7aa"/>
  <path d="M 26 24 Q 40 8 54 24 Q 48 14 40 14 Q 32 14 26 24 Z" fill="#1e293b"/>
  <!-- Mustache -->
  <path d="M 33 29 Q 40 33 47 29 Q 43 31 40 31 Q 37 31 33 29 Z" fill="#1e293b"/>
  <circle cx="34" cy="22" r="1.8" fill="#0f172a"/>
  <circle cx="46" cy="22" r="1.8" fill="#0f172a"/>
  <!-- Work waistcoat, white shirt & red tie -->
  <path d="M 22 40 L 58 40 L 62 92 L 18 92 Z" fill="#334155" stroke="#1e293b" stroke-width="1"/>
  <polygon points="34,40 40,50 46,40" fill="#f8fafc"/>
  <polygon points="39,44 41,44 42,56 38,56" fill="#dc2626"/>
  <!-- Blueprint roll of the 1931 Wind Turbine -->
  <rect x="8" y="55" width="10" height="30" rx="2" fill="#bae6fd" stroke="#0284c7" stroke-width="0.8" transform="rotate(-15 13 70)"/>
  <!-- Steel vernier caliper in hand -->
  <path d="M 62,55 L 72,75" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
  <!-- Legs -->
  <line x1="30" y1="92" x2="30" y2="114" stroke="#1e293b" stroke-width="7"/>
  <line x1="50" y1="92" x2="50" y2="114" stroke="#1e293b" stroke-width="7"/>
  <ellipse cx="27" cy="115" rx="8" ry="4" fill="#0f172a"/>
  <ellipse cx="53" cy="115" rx="8" ry="4" fill="#0f172a"/>
</svg>"""
save_svg("char_ufimtsev", svg_char_ufimtsev, cx=40, cy=60)

# Academician Petr Lazarev
svg_char_lazarev = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120" width="80" height="120">
  <circle cx="40" cy="24" r="14" fill="#fed7aa"/>
  <path d="M 26 24 Q 40 8 54 24 Q 48 14 40 14 Q 32 14 26 24 Z" fill="#475569"/>
  <!-- Scholar round spectacles -->
  <circle cx="35" cy="23" r="3.2" fill="none" stroke="#0f172a" stroke-width="1.2"/>
  <circle cx="45" cy="23" r="3.2" fill="none" stroke="#0f172a" stroke-width="1.2"/>
  <line x1="38.2" y1="23" x2="41.8" y2="23" stroke="#0f172a" stroke-width="1"/>
  <!-- Academician Suit -->
  <path d="M 20 40 L 60 40 L 64 92 L 16 92 Z" fill="#0f172a" stroke="#334155" stroke-width="1"/>
  <!-- Electromagnetic Variometer Instrument -->
  <rect x="58" y="58" width="18" height="22" rx="2" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
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

# 1. telescope_lens (Normal / Seeking Focus)
svg_telescope_lens = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90">
  <circle cx="45" cy="45" r="42" fill="none" stroke="#f59e0b" stroke-width="2"/>
  <circle cx="45" cy="45" r="38" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="3 3"/>
  <line x1="45" y1="6" x2="45" y2="84" stroke="#38bdf8" stroke-width="1"/>
  <line x1="6" y1="45" x2="84" y2="45" stroke="#38bdf8" stroke-width="1"/>
  <circle cx="45" cy="45" r="14" fill="none" stroke="#ef4444" stroke-width="1.2"/>
  <circle cx="45" cy="45" r="2" fill="#ef4444"/>
  <text x="45" y="65" font-family="monospace" font-size="6" fill="#f59e0b" text-anchor="middle">ФОКУС: ПОИСК</text>
</svg>"""
save_svg("telescope_lens", svg_telescope_lens, cx=45, cy=45)

# 2. telescope_lens_sharp (Locked Precision Focus)
svg_telescope_lens_sharp = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90">
  <circle cx="45" cy="45" r="42" fill="none" stroke="#22c55e" stroke-width="2.5"/>
  <circle cx="45" cy="45" r="38" fill="none" stroke="#22c55e" stroke-width="1" stroke-dasharray="4 2"/>
  <line x1="45" y1="6" x2="45" y2="84" stroke="#22c55e" stroke-width="1.2"/>
  <line x1="6" y1="45" x2="84" y2="45" stroke="#22c55e" stroke-width="1.2"/>
  <circle cx="45" cy="45" r="14" fill="none" stroke="#22c55e" stroke-width="1.8"/>
  <circle cx="45" cy="45" r="2.5" fill="#22c55e"/>
  <text x="45" y="65" font-family="monospace" font-size="6" font-weight="bold" fill="#22c55e" text-anchor="middle">100% ФОКУС</text>
</svg>"""
save_svg("telescope_lens_sharp", svg_telescope_lens_sharp, cx=45, cy=45)

# 3. eclipse_target (Solar Eclipse)
svg_eclipse_target = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" height="60">
  <defs>
    <radialGradient id="solar_corona" cx="50%" cy="50%" r="50%">
      <stop offset="35%" stop-color="#fef08a" stop-opacity="1"/>
      <stop offset="65%" stop-color="#f59e0b" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="30" cy="30" r="28" fill="url(#solar_corona)"/>
  <circle cx="28" cy="30" r="18" fill="#02040a"/>
  <circle cx="44" cy="22" r="4" fill="#ffffff"/>
</svg>"""
save_svg("eclipse_target", svg_eclipse_target, cx=30, cy=30)

# 4. wind_rotor (Ufimtsev's 4-Blade Wooden Aerodynamic Rotor)
svg_wind_rotor = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 110" width="110" height="110">
  <g transform="translate(55,55)">
    <path d="M -5 -8 L -3 -50 Q 0 -54 3 -50 L 5 -8 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <path d="M 8 -5 L 50 -3 Q 54 0 50 3 L 8 5 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <path d="M 5 8 L 3 50 Q 0 54 -3 50 L -5 8 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <path d="M -8 5 L -50 3 Q -54 0 -50 -3 L -8 -5 Z" fill="#78350f" stroke="#451a03" stroke-width="1"/>
    <!-- Brass Hub with Centered Bolting -->
    <circle cx="0" cy="0" r="10" fill="#f59e0b" stroke="#78350f" stroke-width="1.8"/>
    <circle cx="0" cy="0" r="4" fill="#451a03"/>
  </g>
</svg>"""
save_svg("wind_rotor", svg_wind_rotor, cx=55, cy=55)

# 5. flywheel_meter (Ufimtsev Vacuum Kinetic Flywheel)
svg_flywheel_meter = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90">
  <circle cx="45" cy="45" r="42" fill="#0f172a" stroke="#475569" stroke-width="2.5"/>
  <circle cx="45" cy="45" r="36" fill="#1e293b"/>
  <circle cx="45" cy="45" r="26" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="6 4"/>
  <circle cx="45" cy="45" r="7" fill="#38bdf8"/>
  <path d="M 20 70 A 32 32 0 1 1 70 70" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-dasharray="3 3"/>
  <text x="45" y="65" font-family="monospace" font-size="6" font-weight="bold" fill="#38bdf8" text-anchor="middle">МАХОВИК ВАКУУМ</text>
  <text x="45" y="74" font-family="monospace" font-size="6" fill="#22c55e" text-anchor="middle">100% ЭНЕРГИЯ</text>
</svg>"""
save_svg("flywheel_meter", svg_flywheel_meter, cx=45, cy=45)

# 6. magneto_sensor (Geophysical Compass Sensor)
svg_magneto_sensor = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 70" width="70" height="70">
  <circle cx="35" cy="35" r="32" fill="#0f172a" stroke="#0ea5e9" stroke-width="2"/>
  <circle cx="35" cy="35" r="26" fill="#1e293b"/>
  <text x="35" y="18" font-family="sans-serif" font-size="7" font-weight="bold" fill="#ef4444" text-anchor="middle">N</text>
  <text x="35" y="56" font-family="sans-serif" font-size="7" font-weight="bold" fill="#38bdf8" text-anchor="middle">S</text>
  <!-- Needle -->
  <polygon points="35,13 38,35 32,35" fill="#ef4444"/>
  <polygon points="35,57 38,35 32,35" fill="#38bdf8"/>
  <circle cx="35" cy="35" r="3" fill="#f59e0b"/>
</svg>"""
save_svg("magneto_sensor", svg_magneto_sensor, cx=35, cy=35)

# 7. ore_vein (Magnetite Quartzite Ore)
svg_ore_vein = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 70 45" width="70" height="45">
  <polygon points="10,35 25,12 45,8 62,25 55,42 18,40" fill="#1e293b" stroke="#64748b" stroke-width="1.2"/>
  <polygon points="25,12 45,8 38,28 20,25" fill="#334155"/>
  <polygon points="45,8 62,25 48,35 38,28" fill="#0f172a"/>
  <!-- Sparkling magnetic points -->
  <circle cx="32" cy="18" r="2" fill="#38bdf8"/>
  <circle cx="48" cy="22" r="2" fill="#38bdf8"/>
  <ellipse cx="36" cy="24" rx="26" ry="14" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="3 3"/>
</svg>"""
save_svg("ore_vein", svg_ore_vein, cx=35, cy=22)

print("7. Generating Liquid Glass UI & Buttons...")

# Dialog Plate (Liquid Glass Panel)
svg_dialog_plate = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 80" width="440" height="80">
  <defs>
    <linearGradient id="dlg_glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e293b" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.92"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="438" height="78" rx="6" fill="url(#dlg_glass)" stroke="#38bdf8" stroke-width="0.8" stroke-opacity="0.4"/>
  <line x1="2" y1="2" x2="438" y2="2" stroke="#ffffff" stroke-width="1" stroke-opacity="0.6"/>
  <text x="424" y="72" font-family="sans-serif" font-size="7.5" fill="#64748b" text-anchor="end">[КЛИКНИТЕ ИЛИ НАЖМИТЕ ПРОБЕЛ ▼]</text>
</svg>"""
save_svg("dialog_plate", svg_dialog_plate, cx=220, cy=40)

# HUD Bar (Telemetry Header)
svg_hud_bar = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 26" width="460" height="26">
  <rect x="1" y="1" width="458" height="24" rx="4" fill="#0f172a" fill-opacity="0.9" stroke="#38bdf8" stroke-width="0.75" stroke-opacity="0.4"/>
  <line x1="2" y1="2" x2="458" y2="2" stroke="#ffffff" stroke-width="0.8" stroke-opacity="0.5"/>
  <rect x="5" y="4" width="70" height="18" rx="2" fill="#0284c7" fill-opacity="0.5"/>
  <text x="40" y="16" font-family="sans-serif" font-size="8" font-weight="bold" fill="#ffffff" text-anchor="middle">МИССИЯ</text>
  <circle cx="445" cy="13" r="4.5" fill="#22c55e"/>
</svg>"""
save_svg("hud_bar", svg_hud_bar, cx=230, cy=13)

# Buttons:
def make_liquid_btn(name, text, w, h, fill_col, stroke_col):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="6" fill="{fill_col}" stroke="{stroke_col}" stroke-width="1"/>
  <line x1="2" y1="2" x2="{w-2}" y2="2" stroke="#ffffff" stroke-width="1" stroke-opacity="0.6"/>
  <text x="{w/2}" y="{h/2 + 4}" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#ffffff" text-anchor="middle" letter-spacing="0.5">{text}</text>
</svg>"""

save_svg("btn_start", make_liquid_btn("btn_start", "▶ НАЧАТЬ ЭКСПЕДИЦИЮ", 180, 40, "#166534", "#4ade80"), cx=90, cy=20)
save_svg("btn_rules", make_liquid_btn("btn_rules", "ПРАВИЛА И ЗАДАЧИ", 160, 36, "#0369a1", "#38bdf8"), cx=80, cy=18)
save_svg("btn_authors", make_liquid_btn("btn_authors", "О ПРОЕКТЕ / АВТОРЫ", 160, 36, "#475569", "#94a3b8"), cx=80, cy=18)

save_svg("btn_opt_a", make_liquid_btn("btn_opt_a", "[ A ]  ЗОЛОТАЯ ДЕМИДОВСКАЯ ПРЕМИЯ 1858", 340, 32, "#1e293b", "#38bdf8"), cx=170, cy=16)
save_svg("btn_opt_b", make_liquid_btn("btn_opt_b", "[ B ]  НОБЕЛЕВСКАЯ ПРЕМИЯ", 340, 32, "#1e293b", "#38bdf8"), cx=170, cy=16)
save_svg("btn_opt_c", make_liquid_btn("btn_opt_c", "[ C ]  ОРДЕН АНДРЕЯ ПЕРВОЗВАННОГО", 340, 32, "#1e293b", "#38bdf8"), cx=170, cy=16)

save_svg("btn_brake", make_liquid_btn("btn_brake", "⚠ ТОРМОЗ РОТОРА", 130, 34, "#7f1d1d", "#ef4444"), cx=65, cy=17)
save_svg("btn_gear", make_liquid_btn("btn_gear", "⚡ ВАКУУМНЫЙ МАХОВИК", 140, 34, "#0c4a6e", "#38bdf8"), cx=70, cy=17)
save_svg("btn_drill", make_liquid_btn("btn_drill", "⛏ ИЗВЛЕЧЬ КЕРН КМА", 140, 34, "#1e3a8a", "#60a5fa"), cx=70, cy=17)
save_svg("btn_lock_focus", make_liquid_btn("btn_lock_focus", "🔍 ЗАФИКСИРОВАТЬ ФОКУС", 150, 34, "#14532d", "#22c55e"), cx=75, cy=17)

# Demidov Gold Medal
svg_fx_medal = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90" width="90" height="90">
  <defs>
    <linearGradient id="medal_gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
  </defs>
  <!-- Red Imperial ribbon loop -->
  <polygon points="36,4 45,18 54,4" fill="#dc2626"/>
  <!-- Gold Medal body -->
  <circle cx="45" cy="48" r="36" fill="url(#medal_gold)" stroke="#78350f" stroke-width="2"/>
  <circle cx="45" cy="48" r="32" fill="none" stroke="#fef08a" stroke-width="1.2" stroke-dasharray="2 2"/>
  <!-- Laurel wreath -->
  <circle cx="45" cy="48" r="26" fill="#d97706"/>
  <text x="45" y="42" font-family="sans-serif" font-size="7" font-weight="900" fill="#fef08a" text-anchor="middle">ДЕМИДОВСКАЯ</text>
  <text x="45" y="51" font-family="sans-serif" font-size="7" font-weight="900" fill="#fef08a" text-anchor="middle">ПРЕМИЯ</text>
  <text x="45" y="60" font-family="sans-serif" font-size="6.5" fill="#fef08a" text-anchor="middle">★ 1858 ★</text>
</svg>"""
save_svg("fx_medal", svg_fx_medal, cx=45, cy=45)

# Spark effect
svg_fx_spark = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60" width="60" height="60">
  <path d="M 30 10 L 33 26 L 49 30 L 33 34 L 30 50 L 27 34 L 11 30 L 27 26 Z" fill="#fbbf24"/>
  <circle cx="30" cy="30" r="4" fill="#ffffff"/>
  <circle cx="18" cy="18" r="2" fill="#38bdf8"/>
  <circle cx="42" cy="18" r="2" fill="#38bdf8"/>
</svg>"""
save_svg("fx_spark", svg_fx_spark, cx=30, cy=30)

# Save manifest
with open("/home/dima/Projects/hackathon/scratch_project/assets_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"All {len(manifest)} Liquid Glass assets successfully generated and registered!")
