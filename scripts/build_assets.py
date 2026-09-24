#!/usr/bin/env python3
"""Build every README SVG from live LeetCode / Codeforces data (run by .github/workflows/profile-assets.yml)."""
import base64
import html
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = str(ROOT / "assets")
CACHE = ROOT / "assets" / "data" / "cp.json"
PORTFOLIO = "ojas-srivastava.vercel.app"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
FP, FPL = "O5WS-7F3A9E2B1C4D", "o5ws7f3a9e2b1c4d"

BG = "#0B0E14"
EM, CY, AM = "#34D399", "#22D3EE", "#FBBF24"
OR, BL, VI, PK, CC = "#FFA116", "#3B9DE8", "#A78BFA", "#F472B6", "#D6A76C"
TXT, SOFT, MUTED, DIM = "#F0F6FC", "#C9D1D9", "#8B949E", "#6E7681"

LC_FALLBACK = [1486, 1462, 1411, 1484, 1527, 1557, 1643, 1647, 1683, 1674, 1681, 1718, 1714, 1727, 1747,
               1760, 1800, 1828, 1858, 1889, 1920, 1904, 1952, 1925, 1931, 1956, 1994, 1983, 2009, 2039, 2048]
CF_FALLBACK = [402, 650, 899, 1004, 1059, 1014, 1033, 1072, 1104, 1125, 1178, 1183, 1128, 1157, 1360, 1351,
               1331, 1201, 1421, 1376]


def fetch(url, timeout=40):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def esc(s):
    return html.escape(str(s), quote=False)


def t(x, y, s, size=16, fill=SOFT, weight=400, mono=False, anchor=None, ls=None, extra="", raw=False):
    a = f' text-anchor="{anchor}"' if anchor else ""
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    body = s if raw else esc(s)
    return (f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{a}{l}{extra}>{body}</text>')


def glow(gid, color, op):
    return (f'<radialGradient id="{gid}" cx=".5" cy=".5" r=".5"><stop stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')


def lin(gid, a, b, vertical=False, oa=1, ob=1):
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop stop-color="{a}" stop-opacity="{oa}"/>'
            f'<stop offset="1" stop-color="{b}" stop-opacity="{ob}"/></linearGradient>')


def chip(x, y, label, color, size=12.5):
    w = round(len(label) * size * 0.62 + 26)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="9" fill="{color}" fill-opacity="0.1" '
            f'stroke="{color}" stroke-opacity="0.35"/>' + t(x + 13, y + 20, label, size, SOFT, 600, True)), w


def particles(path, color, n=3, dur=10, r=3):
    out = []
    for k in range(n):
        out.append(f'<circle r="{r}" fill="{color}" opacity="0"><set attributeName="opacity" to="0.9" begin="0s"/>'
                   f'<animateMotion dur="{dur}s" begin="-{k * dur / n:.2f}s" repeatCount="indefinite" path="{path}"/></circle>')
    return "".join(out)


def sweep(x, y, w, h, rx, color, delay=0, width=2):
    return (f'<rect class="sweep" style="animation-delay:-{delay}s" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" pathLength="1000"/>')


def band(w, h):
    return (f'<g clip-path="url(#clipAll)"><rect class="scan" x="-300" y="0" width="300" height="{h}" fill="url(#band)"/></g>')


def doc(name, w, h, title, body, defs="", css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-labelledby="t-{name}">
  <title id="t-{name}">{esc(title)}</title>
  <metadata>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
      <rdf:Description dc:creator="Ojas Srivastava" dc:identifier="{FP}" dc:source="https://github.com/Ojas-Srivastava05" dc:rights="Copyright 2026 Ojas Srivastava. Unauthorized copying prohibited."/>
    </rdf:RDF>
  </metadata>
  <!-- o5ws-integrity:{name}:7f3a9e2b1c4d -->
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="#FFFFFF" stroke-opacity="0.04"/></pattern>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{EM}"/><stop offset=".55" stop-color="{CY}"/><stop offset="1" stop-color="{AM}"/></linearGradient>
    <linearGradient id="txt" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".55" stop-color="#A7F3D0"/><stop offset="1" stop-color="#FDE68A"/></linearGradient>
    <linearGradient id="band" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="0.06"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
    <clipPath id="clipAll"><rect width="{w}" height="{h}" rx="24"/></clipPath>
    {defs}
    <style>
      .fade {{ animation: fade .7s ease both; }}
      .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
      .blink {{ animation: blink 1.1s steps(1) infinite; }}
      .dash {{ stroke-dasharray: 10 14; animation: dash 14s linear infinite; }}
      .draw {{ stroke-dasharray: 1000; animation: draw 2.6s cubic-bezier(.4,0,.2,1) both; }}
      .sweep {{ stroke-dasharray: 110 890; animation: sweep 7s linear infinite; }}
      .scan {{ animation: scan 8s cubic-bezier(.6,0,.4,1) infinite; }}
      @keyframes sweep {{ from {{ stroke-dashoffset: 1000; }} to {{ stroke-dashoffset: 0; }} }}
      @keyframes scan {{ 0% {{ transform: translateX(-420px); }} 60%, 100% {{ transform: translateX({w + 420}px); }} }}
      @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
      @keyframes pulse {{ 0%, 100% {{ opacity: .3; }} 50% {{ opacity: 1; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes dash {{ to {{ stroke-dashoffset: -480; }} }}
      @keyframes draw {{ from {{ stroke-dashoffset: 1000; }} to {{ stroke-dashoffset: 0; }} }}
      {css}
    </style>
  </defs>
  <rect width="{w}" height="{h}" rx="24" fill="{BG}"/>
  <rect width="{w}" height="{h}" rx="24" fill="url(#grid)"/>
  {body}
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="23.5" stroke="#FFFFFF" stroke-opacity="0.09"/>
  <text x="-9999" y="-9999" opacity="0" font-size="1">{FPL}</text>
</svg>
'''


def write(fname, content):
    with open(f"{OUT}/{fname}", "w", encoding="utf-8") as f:
        f.write(content)


def hero(solved_total):
    W, H = 1200, 620
    stack = ("C++  ·  PYTHON  ·  TYPESCRIPT  ·  FASTAPI  ·  NODE.JS  ·  EXPRESS  ·  NEXT.JS  ·  REACT  ·  "
             "POSTGRESQL  ·  MONGODB  ·  REDIS  ·  FIREBASE  ·  DOCKER  ·  GCP  ·  GITHUB ACTIONS  ·  "
             "GEMINI  ·  RAG  ·  SCIKIT-LEARN  ·  ")
    L = round(len(stack) * 8.7)
    defs = (glow("gA", EM, .22) + glow("gB", CY, .14) + glow("gC", AM, .08)
            + lin("term", EM, AM, oa=.7, ob=.5)
            + '<clipPath id="mq"><rect x="40" y="556" width="1120" height="40" rx="12"/></clipPath>'
            + '<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0" gradientTransform="translate(-600 0)">'
              '<stop stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="0.85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>'
              '<animateTransform attributeName="gradientTransform" type="translate" values="-600 0;-600 0;900 0" keyTimes="0;.45;1" dur="6s" repeatCount="indefinite"/></linearGradient>')
    css = f".marq {{ animation: marq 45s linear infinite; }} @keyframes marq {{ to {{ transform: translateX(-{L}px); }} }}"
    b = []
    b.append('<ellipse cx="1010" cy="130" rx="440" ry="320" fill="url(#gA)"/>')
    b.append('<ellipse cx="150" cy="560" rx="400" ry="260" fill="url(#gB)"/>')
    b.append('<ellipse cx="620" cy="300" rx="300" ry="200" fill="url(#gC)"/>')
    b.append('<path class="dash" d="M40 470C220 380 360 520 540 430C700 350 820 560 1160 470" stroke="url(#acc)" stroke-opacity="0.25" stroke-width="1.5"/>')
    b.append(particles("M40 470C220 380 360 520 540 430C700 350 820 560 1160 470", EM, 4, 12, 2.6))

    b.append('<rect x="40" y="36" width="1120" height="44" rx="12" fill="#FFFFFF" fill-opacity="0.035" stroke="#34D399" stroke-opacity="0.25"/>')
    b.append(f'<circle class="pulse" cx="64" cy="58" r="10" fill="{EM}" fill-opacity="0.25"/><circle cx="64" cy="58" r="4.5" fill="{EM}"/>')
    b.append(t(84, 63, "OPEN TO SUMMER 2027 SOFTWARE ENGINEERING INTERNSHIPS", 12.5, EM, 700, True, ls=1.6))
    b.append(f'<rect x="846" y="45" width="302" height="26" rx="13" fill="{CY}" fill-opacity="0.1" stroke="{CY}" stroke-opacity="0.45"/>')
    b.append(t(997, 62, f"↗  {PORTFOLIO.upper()}", 11.5, CY, 700, True, "middle", 1.1))

    b.append(t(70, 150, "// software engineer · full-stack & applied ai", 15, MUTED, 500, True))
    b.append(t(64, 238, "Ojas", 92, "url(#txt)", 800, ls=-2))
    b.append(t(64, 330, f'Srivastava<tspan fill="{EM}">.</tspan>', 92, "url(#txt)", 800, ls=-2, raw=True))
    b.append(t(64, 238, "Ojas", 92, "url(#shine)", 800, ls=-2))
    b.append(t(64, 330, "Srivastava.", 92, "url(#shine)", 800, ls=-2))
    b.append(t(70, 382, "I build backend systems, full-stack products and applied AI —", 19, SOFT))
    b.append(t(70, 411, "and sharpen them with daily competitive programming.", 19, SOFT))

    stats = [("2048", "LEETCODE PEAK"), ("Top 2%", "LC GLOBAL RANK"), (solved_total, "PROBLEMS SOLVED"), ("9.20", "CGPA · SVNIT")]
    for i, (n, lab) in enumerate(stats):
        x = 70 + i * 158
        if i:
            b.append(f'<rect x="{x - 18}" y="458" width="1" height="68" fill="#FFFFFF" fill-opacity="0.1"/>')
        b.append(f'<g class="fade" style="animation-delay:{.2 + i * .12:.2f}s">'
                 + t(x, 494, n, 36, "url(#txt)", 800, ls=-.5) + t(x, 522, lab, 11.5, MUTED, 600, True, ls=1.2) + '</g>')

    tx, ty, tw, th = 730, 108, 400, 428
    b.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="18" fill="#0D1117" fill-opacity="0.94"/>')
    b.append(f'<rect x="{tx + .75}" y="{ty + .75}" width="{tw - 1.5}" height="{th - 1.5}" rx="17.25" stroke="url(#term)" stroke-width="1.5"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b.append(f'<circle cx="{tx + 24 + i * 20}" cy="{ty + 26}" r="5.5" fill="{c}"/>')
    b.append(t(tx + tw - 22, ty + 31, "ojas@svnit: ~", 12, DIM, 500, True, "end"))
    b.append(f'<rect x="{tx}" y="{ty + 50}" width="{tw}" height="1" fill="#FFFFFF" fill-opacity="0.07"/>')

    lines = [
        ("cmd", "whoami"),
        ("out", "ojas — b.tech ai · svnit surat '28"),
        ("cmd", "cat achievements.log"),
        ("item", ("Vibe2Ship 2026", "Global Top 20")),
        ("item", ("GSC 2026", "Global Top 106")),
        ("item", ("LeetCode", "Knight · 2048")),
        ("item", ("Codeforces", "Specialist")),
        ("item", ("McKinsey.org", "Forward Fellow")),
        ("item", ("Nexus SVNIT", "Chairperson")),
        ("item", ("IFFCO", "SWE Intern '25")),
        ("cmd", "echo $STATUS"),
        ("ok", "open_to_work --summer-2027 ✓"),
    ]
    y = ty + 84
    clips = []
    for i, (kind, s) in enumerate(lines):
        start = .5 + i * .32
        total = start + (.45 if kind == "cmd" else .3)
        clips.append(f'<clipPath id="tw{i}"><rect x="{tx + 16}" y="{y - 17}" height="24" width="{tw - 32}">'
                     f'<animate attributeName="width" values="0;0;{tw - 32}" keyTimes="0;{start / total:.3f};1" dur="{total:.2f}s" fill="freeze"/></rect></clipPath>')
        d = f' clip-path="url(#tw{i})"'
        if kind == "cmd":
            b.append(f'<g{d}>' + t(tx + 24, y, f'<tspan fill="{EM}">❯</tspan> <tspan fill="{TXT}">{esc(s)}</tspan>', 13, SOFT, 600, True, raw=True) + '</g>')
        elif kind == "out":
            b.append(f'<g{d}>' + t(tx + 24, y, s, 13, MUTED, 400, True) + '</g>')
        elif kind == "ok":
            b.append(f'<g{d}>' + t(tx + 24, y, s, 13, EM, 700, True) + '</g>')
        else:
            k, val = s
            dots = "." * max(2, 37 - len(k) - len(val))
            b.append(f'<g{d}>' + t(tx + 24, y, f'<tspan fill="{AM}">▸</tspan> <tspan fill="{SOFT}">{esc(k)}</tspan>'
                                   f'<tspan fill="#3A424D"> {dots} </tspan><tspan fill="{TXT}" font-weight="700">{esc(val)}</tspan>',
                                   13, SOFT, 400, True, raw=True) + '</g>')
        y += 25 if kind in ("out", "item") and lines[min(i + 1, len(lines) - 1)][0] == "cmd" else 23
    defs += "".join(clips)
    b.append(t(tx + 24, y, f'<tspan fill="{EM}">❯</tspan>', 13, SOFT, 600, True, raw=True))
    b.append(f'<rect class="blink" x="{tx + 42}" y="{y - 12}" width="8" height="16" fill="{EM}"/>')

    b.append('<rect x="40" y="556" width="1120" height="40" rx="12" fill="#FFFFFF" fill-opacity="0.03" stroke="#FFFFFF" stroke-opacity="0.07"/>')
    b.append('<g clip-path="url(#mq)"><g class="marq">'
             + t(60, 581, stack, 12, MUTED, 600, True, ls=1.5, extra=f' textLength="{L}" lengthAdjust="spacing"')
             + t(60 + L, 581, stack, 12, MUTED, 600, True, ls=1.5, extra=f' textLength="{L}" lengthAdjust="spacing"')
             + '</g></g>')
    return doc("hero", W, H, "Ojas Srivastava — Software Engineer, Full-Stack & Applied AI. Open to Summer 2027 SWE internships.",
               "\n  ".join(b), defs, css)


def section(n, title, sub):
    W, H = 1200, 96
    defs = glow("sg", EM, .18)
    b = [
        '<ellipse cx="120" cy="48" rx="260" ry="90" fill="url(#sg)"/>',
        t(40, 58, f"{n:02d}", 16, EM, 700, True, ls=1),
        '<rect x="74" y="36" width="1" height="28" fill="#FFFFFF" fill-opacity="0.18"/>',
        t(92, 60, title, 30, TXT, 800, ls=-.5),
        t(1160, 57, sub.upper(), 12.5, MUTED, 600, True, "end", 1.6),
        '<rect class="grow" x="40" y="78" width="64" height="2" rx="1" fill="url(#acc)"/>',
        band(W, H),
    ]
    css = ".grow { transform-box: fill-box; transform-origin: left; animation: grow 3.6s ease-in-out infinite; } @keyframes grow { 50% { transform: scaleX(2.6); } }"
    return doc(f"section-{n:02d}", W, H, f"{n:02d} — {title}", "\n  ".join(b), defs, css)


def highlights():
    W, H = 1200, 470
    cards = [
        (EM, "VIBE2SHIP 2026", "Global Top 20", ["Solo-built CIVICPULSE AI — a civic PWA", "with Gemini Vision and 6 AI agents."]),
        (CY, "GOOGLE SOLUTION CHALLENGE", "Global Top 106", ["LogiFlow · Technical Co-Lead. ML delay", "prediction for multi-modal logistics."]),
        (OR, "LEETCODE CONTESTS", "Knight · 2048", ["Peak contest rating · top ~2% globally.", "750+ problems · 30+ rated contests."]),
        (BL, "CODEFORCES + CODECHEF", "Specialist", ["Max 1421 on Codeforces · 270+ solved.", "CodeChef 2★ · 118+ solved."]),
        (VI, "MCKINSEY.ORG", "Forward Fellow", ["Selected for McKinsey.org's Forward", "program in problem-solving & leadership."]),
        (AM, "NEXUS SVNIT · AY 2026–27", "Chairperson", ["Elected to lead the DoCSE & DoAI tech", "cell — programs for 500+ students."]),
    ]
    defs = "".join(glow(f"hg{i}", c[0], .2) for i, c in enumerate(cards))
    b = []
    for i, (c, tag, big, desc) in enumerate(cards):
        x, y, w, h = 30 + (i % 3) * 390, 30 + (i // 3) * 220, 360, 190
        b.append(f'<g class="fade" style="animation-delay:{i * .1:.1f}s">')
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#FFFFFF" fill-opacity="0.025"/>')
        b.append(f'<ellipse cx="{x + w - 30}" cy="{y + 20}" rx="150" ry="100" fill="url(#hg{i})"/>')
        b.append(f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="17.5" stroke="{c}" stroke-opacity="0.28"/>')
        b.append(sweep(x + .5, y + .5, w - 1, h - 1, 17.5, c, i * 1.15))
        b.append(f'<rect x="{x + 26}" y="{y}" width="44" height="3" rx="1.5" fill="{c}"/>')
        b.append(t(x + 26, y + 44, tag, 12, c, 700, True, ls=1.4))
        b.append(t(x + w - 24, y + 44, f"{i + 1:02d}", 12, DIM, 600, True, "end"))
        b.append(t(x + 24, y + 96, big, 36, TXT, 800, ls=-.8))
        b.append(t(x + 26, y + 134, desc[0], 14.5, MUTED))
        b.append(t(x + 26, y + 157, desc[1], 14.5, MUTED))
        b.append('</g>')
    return doc("highlights", W, H, "Highlights — Vibe2Ship Global Top 20, GSC Global Top 106, LeetCode Knight 2048, Codeforces Specialist, McKinsey.org Forward Fellow, Chairperson Nexus SVNIT",
               "\n  ".join(b), defs)


def spark(vals, x0, y0, w, h, lo, hi):
    n = len(vals)
    pts = [(x0 + (w * i / (n - 1) if n > 1 else 0), y0 + h - (v - lo) / (hi - lo) * h) for i, v in enumerate(vals)]
    return pts, "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def star(cx, cy, r, fill, op=1, stroke=None):
    import math
    p = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * .45
        a = -math.pi / 2 + k * math.pi / 5
        p.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    s = f' stroke="{stroke}" stroke-opacity=".5"' if stroke else ""
    return f'<polygon points="{" ".join(p)}" fill="{fill}" fill-opacity="{op}"{s}/>'


def cp(lc, cf, lc_solved, lc_contests):
    W, H = 1200, 520
    defs = (glow("lcg0", OR, .16) + glow("cfg0", BL, .18) + glow("ccg0", CC, .16)
            + lin("lcT", OR, AM) + lin("cfT", "#7CC4FF", BL) + lin("ccT", "#F3D9A4", CC)
            + lin("lcA", OR, OR, True, .3, 0) + lin("cfA", BL, BL, True, .3, 0))
    b = []

    x, y, w, h = 30, 30, 680, 460
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#FFFFFF" fill-opacity="0.025"/>')
    b.append(f'<ellipse cx="{x + 120}" cy="{y + 60}" rx="300" ry="180" fill="url(#lcg0)"/>')
    b.append(f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="19.5" stroke="{OR}" stroke-opacity="0.25"/>')
    b.append(t(x + 30, y + 44, "LEETCODE", 13, OR, 700, True, ls=2))
    b.append(f'<circle class="pulse" cx="{x + 140}" cy="{y + 40}" r="6" fill="{EM}" fill-opacity="0.35"/><circle cx="{x + 140}" cy="{y + 40}" r="3" fill="{EM}"/>')
    b.append(t(x + 152, y + 44, "AUTO-SYNCED DAILY", 11, EM, 700, True, ls=1.4))
    b.append(t(x + w - 30, y + 44, "@Oju_Srivastava", 13, DIM, 500, True, "end"))
    b.append(t(x + 26, y + 118, "2048", 72, "url(#lcT)", 800, ls=-2))
    b.append(t(x + 212, y + 88, "PEAK CONTEST RATING", 12, MUTED, 600, True, ls=1.4))
    b.append(t(x + 210, y + 118, "Knight", 30, TXT, 800, ls=-.5))
    cx = x + 30
    for lab in ["Top ~2% globally", f"{lc_solved} solved", f"{lc_contests // 10 * 10}+ rated contests"]:
        s, cw = chip(cx, y + 146, lab, OR)
        b.append(s)
        cx += cw + 10
    gx, gy, gw, gh = x + 60, y + 220, w - 100, 200
    lo, hi = 1350, 2150
    for v in (1400, 1600, 1800, 2000):
        yy = gy + gh - (v - lo) / (hi - lo) * gh
        b.append(f'<rect x="{gx}" y="{yy:.1f}" width="{gw}" height="1" fill="#FFFFFF" fill-opacity="0.06"/>')
        b.append(t(gx - 12, yy + 4, str(v), 11, DIM, 500, True, "end"))
    pts, d = spark(lc, gx, gy, gw, gh, lo, hi)
    b.append(f'<path d="{d} L{pts[-1][0]:.1f} {gy + gh} L{pts[0][0]:.1f} {gy + gh} Z" fill="url(#lcA)"/>')
    b.append(f'<path class="draw" pathLength="1000" d="{d}" stroke="{OR}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    for px, py in pts:
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="{BG}" stroke="{OR}" stroke-width="1.4"/>')
    pi = max(range(len(lc)), key=lambda i: lc[i])
    px, py = pts[pi]
    b.append(f'<circle class="pulse" cx="{px:.1f}" cy="{py:.1f}" r="11" fill="{OR}" fill-opacity="0.3"/><circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{AM}"/>')
    b.append(t(px - 12, py - 16, f"peak {max(lc)}", 12, AM, 700, True, "end"))
    b.append(t(gx, gy + gh + 26, f"rating across {len(lc)} rated contests  ·  {lc[0]} → {max(lc)}", 12, DIM, 500, True))

    x, y, w, h = 730, 30, 440, 220
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#FFFFFF" fill-opacity="0.025"/>')
    b.append(f'<ellipse cx="{x + 90}" cy="{y + 50}" rx="220" ry="130" fill="url(#cfg0)"/>')
    b.append(f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="19.5" stroke="{BL}" stroke-opacity="0.3"/>')
    b.append(t(x + 28, y + 42, "CODEFORCES", 13, BL, 700, True, ls=2))
    b.append(t(x + w - 28, y + 42, "@Oju", 13, DIM, 500, True, "end"))
    b.append(t(x + 24, y + 104, str(max(cf)), 54, "url(#cfT)", 800, ls=-1.5))
    b.append(t(x + 170, y + 80, "MAX RATING", 11.5, MUTED, 600, True, ls=1.4))
    b.append(t(x + 168, y + 106, "Specialist", 24, TXT, 800, ls=-.4))
    s, _ = chip(x + 300, y + 82, "270+ solved", BL, 11.5)
    b.append(s)
    sx, sy, sw, sh = x + 28, y + 132, w - 56, 64
    clo, chi = 300, 1500
    by = sy + sh - (1400 - clo) / (chi - clo) * sh
    b.append(f'<rect x="{sx}" y="{by:.1f}" width="{sw}" height="1" fill="{CY}" fill-opacity="0.35"/>')
    b.append(t(sx, by - 7, "1400 · specialist line", 10.5, CY, 600, True))
    pts, d = spark(cf, sx, sy, sw, sh, clo, chi)
    b.append(f'<path d="{d} L{pts[-1][0]:.1f} {sy + sh} L{pts[0][0]:.1f} {sy + sh} Z" fill="url(#cfA)"/>')
    b.append(f'<path class="draw" pathLength="1000" d="{d}" stroke="{BL}" stroke-width="2" stroke-linejoin="round"/>')
    pi = max(range(len(cf)), key=lambda i: cf[i])
    b.append(f'<circle cx="{pts[pi][0]:.1f}" cy="{pts[pi][1]:.1f}" r="4" fill="#7CC4FF"/>')

    x, y, w, h = 730, 270, 440, 220
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#FFFFFF" fill-opacity="0.025"/>')
    b.append(f'<ellipse cx="{x + 90}" cy="{y + 50}" rx="220" ry="130" fill="url(#ccg0)"/>')
    b.append(f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="19.5" stroke="{CC}" stroke-opacity="0.3"/>')
    b.append(t(x + 28, y + 42, "CODECHEF", 13, CC, 700, True, ls=2))
    b.append(t(x + w - 28, y + 42, "@ojassrivastava", 13, DIM, 500, True, "end"))
    b.append(t(x + 24, y + 104, "2★", 54, "url(#ccT)", 800, ls=-1))
    b.append(t(x + 130, y + 80, "RATED DIVISION", 11.5, MUTED, 600, True, ls=1.4))
    b.append(t(x + 128, y + 106, "2 Star", 24, TXT, 800, ls=-.4))
    s, cw = chip(x + 28, y + 132, "118+ solved", CC, 11.5)
    b.append(s)
    s, _ = chip(x + 28 + cw + 10, y + 132, "11+ rated contests", CC, 11.5)
    b.append(s)
    for k in range(7):
        b.append(star(x + 38 + k * 24, y + 188, 8, CC if k < 2 else "#FFFFFF", 1 if k < 2 else .06, None if k < 2 else "#FFFFFF"))
    b.append(t(x + w - 28, y + 192, "2 of 7 stars", 11, DIM, 500, True, "end"))

    return doc("cp", W, H, f"Competitive programming — LeetCode Knight peak 2048, Codeforces Specialist max {max(cf)}, CodeChef 2 star",
               "\n  ".join(b), defs)


MOTIFS = {
    "route": [(0, 60), (40, 20), (90, 44), (130, 8)],
    "pin": [(10, 50), (60, 10), (110, 40), (70, 70)],
    "pipe": [(0, 40), (45, 40), (90, 10), (130, 40)],
    "plane": [(0, 70), (50, 30), (100, 50), (130, 0)],
    "mandala": [(20, 20), (110, 20), (65, 70), (65, 0)],
    "curve": [(0, 70), (40, 58), (80, 20), (130, 6)],
}


def project(fname, accent, tag, title, sub, metrics, stack, motif):
    W, H = 600, 360
    defs = glow("pg", accent, .22) + lin("pt", "#FFFFFF", accent)
    b = [
        f'<ellipse cx="520" cy="40" rx="260" ry="170" fill="url(#pg)"/>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="23.5" stroke="{accent}" stroke-opacity="0.3"/>',
    ]
    pts = [(440 + px, 34 + py) for px, py in MOTIFS[motif]]
    mpath = "M" + " L".join(f"{x} {y}" for x, y in pts)
    b.append(sweep(.5, .5, W - 1, H - 1, 23.5, accent, sum(map(ord, fname)) % 7, 2.2))
    b.append(f'<path class="dash" d="{mpath}" stroke="{accent}" stroke-opacity="0.55" stroke-width="1.5"/>')
    b.append(particles(mpath + " " + " ".join(f"L{x} {y}" for x, y in reversed(pts[:-1])), "#FFFFFF", 1, 5, 2.4))
    for i, (px, py) in enumerate(pts):
        b.append(f'<circle cx="{px}" cy="{py}" r="{5 if i == len(pts) - 1 else 3.5}" fill="{accent if i == len(pts) - 1 else BG}" stroke="{accent}" stroke-width="1.5"/>')
    b.append(t(36, 56, tag, 12.5, accent, 700, True, ls=1.4))
    b.append(t(34, 116, title, 42, "url(#pt)", 800, ls=-1))
    b.append(t(36, 150, sub, 17.5, SOFT))
    for i, (num, lab) in enumerate(metrics):
        mx = 36 + i * 180
        b.append(f'<rect x="{mx}" y="180" width="166" height="84" rx="14" fill="#FFFFFF" fill-opacity="0.035" stroke="#FFFFFF" stroke-opacity="0.08"/>')
        b.append(t(mx + 18, 222, num, 27, TXT, 800, ls=-.5))
        b.append(t(mx + 18, 247, lab, 11.5, MUTED, 600, True, ls=1))
    b.append(f'<rect x="36" y="290" width="528" height="1" fill="#FFFFFF" fill-opacity="0.08"/>')
    b.append(t(36, 324, stack, 14, MUTED, 500, True))
    return doc(fname.replace(".svg", ""), W, H, f"{title} — {sub}", "\n  ".join(b), defs)


def experience():
    items = [
        ("AY 2026 — 27", "Chairperson", "Nexus SVNIT", AM,
         ["Elected head of the official tech cell for DoCSE & DoAI — own workshops, contests and mentoring for 500+ students.",
          "Two-year path: Member → Social Media Coordinator → Academic Mentor → Technical Representative → Chairperson."]),
        ("2026", "Technical Co-Lead", "Neural Foundry · Google Solution Challenge", CY,
         ["Global Top 106 with LogiFlow — UI/UX head and owner of the railway data pipeline.",
          "Gradient Boosting delay model on 15,650 train-days (MAE 22.7 min) with Pareto time / cost / risk ranking."]),
        ("2026", "Forward Fellow", "McKinsey.org", VI,
         ["Selected for McKinsey.org's Forward program — structured problem-solving, communication and leadership.", ""]),
        ("JUN — JUL 2025", "Software Engineering Intern", "IFFCO · Phulpur", EM,
         ["Built and deployed production tools for the plant operations team, automating 50+ daily enterprise workflows.",
          "Node.js · Express · MySQL · REST APIs · Docker · CI/CD onto internal infrastructure."]),
        ("JUN — AUG 2025", "Technical Lead", "RangRiti · Web Wonders 2025", PK,
         ["Led a four-engineer team shipping a 40+ page cultural-tech marketplace with AI storytelling tools.",
          "Owned backend integration end-to-end, reviewed every PR and shipped to Render."]),
        ("2024 — 2028", "B.Tech, Artificial Intelligence", "SVNIT Surat", BL,
         ["CGPA 9.20 / 10 · algorithms, operating systems, DBMS, computer networks, ML, software engineering.",
          "Executive Member, ACM SVNIT — DSA workshops, coding contests and campus programming events."]),
    ]
    step = 112
    W, H = 1200, 40 + len(items) * step
    defs = glow("eg", EM, .12)
    b = ['<ellipse cx="1050" cy="80" rx="360" ry="220" fill="url(#eg)"/>']
    lx = 236
    b.append(f'<rect x="{lx}" y="56" width="2" height="{(len(items) - 1) * step}" fill="url(#ev)"/>')
    defs += f'<linearGradient id="ev" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{AM}"/><stop offset=".5" stop-color="{EM}"/><stop offset="1" stop-color="{BL}"/></linearGradient>'
    for i, (when, role, org, c, desc) in enumerate(items):
        y = 56 + i * step
        b.append(f'<g class="fade" style="animation-delay:{i * .12:.2f}s">')
        b.append(t(60, y + 5, when, 12.5, c, 700, True, ls=1.2))
        b.append(f'<circle cx="{lx + 1}" cy="{y}" r="9" fill="{c}" fill-opacity="0.18"/><circle cx="{lx + 1}" cy="{y}" r="4.5" fill="{c}"/>')
        b.append(t(270, y + 8, f'<tspan fill="{TXT}" font-weight="800">{esc(role)}</tspan><tspan fill="{c}" font-weight="600" dx="12">{esc(org)}</tspan>', 21, TXT, 800, raw=True))
        b.append(t(270, y + 36, desc[0], 14.5, MUTED))
        if desc[1]:
            b.append(t(270, y + 58, desc[1], 14.5, DIM))
        b.append('</g>')
    return doc("experience", W, H, "Experience and leadership — Nexus SVNIT Chairperson, GSC Technical Co-Lead, McKinsey.org Forward Fellow, IFFCO SWE Intern, RangRiti Technical Lead, SVNIT B.Tech AI",
               "\n  ".join(b), defs)


def now():
    W, H = 1200, 150
    cols = [
        (EM, "NOW BUILDING", "Career Automation Stack", "Internship & Hiring Scouts · OA Forge"),
        (OR, "NOW TRAINING", "Weekly LC & CF rounds", "next: LC Guardian · CF Expert"),
        (CY, "NOW SEEKING", "Summer 2027 SWE internship", "backend · full-stack · applied AI"),
    ]
    defs = "".join(glow(f"ng{i}", c[0], .16) for i, c in enumerate(cols))
    b = []
    for i, (c, tag, head, sub) in enumerate(cols):
        x = 30 + i * 390
        b.append(f'<rect x="{x}" y="25" width="360" height="100" rx="16" fill="#FFFFFF" fill-opacity="0.025"/>')
        b.append(f'<ellipse cx="{x + 40}" cy="40" rx="160" ry="80" fill="url(#ng{i})"/>')
        b.append(f'<rect x="{x + .5}" y="25.5" width="359" height="99" rx="15.5" stroke="{c}" stroke-opacity="0.25"/>')
        b.append(f'<circle class="pulse" cx="{x + 30}" cy="55" r="7" fill="{c}" fill-opacity="0.3" style="animation-delay:{i * .5}s"/><circle cx="{x + 30}" cy="55" r="3.5" fill="{c}"/>')
        b.append(t(x + 46, 60, tag, 12.5, c, 700, True, ls=1.6))
        b.append(t(x + 24, 91, head, 22, TXT, 800, ls=-.4))
        b.append(t(x + 24, 114, sub, 14, MUTED, 500, True))
    return doc("now", W, H, "Now building the Career Automation Stack · training weekly on LeetCode and Codeforces · seeking a Summer 2027 SWE internship",
               "\n  ".join(b), defs)


def footer():
    W, H = 1200, 330
    defs = glow("fa", EM, .2) + glow("fb", CY, .14) + glow("fc", AM, .1)
    b = [
        '<ellipse cx="600" cy="120" rx="520" ry="200" fill="url(#fa)"/>',
        '<ellipse cx="180" cy="300" rx="300" ry="140" fill="url(#fb)"/>',
        '<ellipse cx="1040" cy="300" rx="300" ry="140" fill="url(#fc)"/>',
        '<path class="dash" d="M0 280C200 220 360 320 600 260C840 200 1000 300 1200 240" stroke="url(#acc)" stroke-opacity="0.35" stroke-width="1.5"/>',
        particles("M0 280C200 220 360 320 600 260C840 200 1000 300 1200 240", EM, 5, 14, 2.6),
        band(W, H),
        t(600, 62, "// OPEN TO WORK", 13, EM, 700, True, "middle", 3),
        t(600, 128, "Let’s build something that ships.", 52, "url(#txt)", 800, anchor="middle", ls=-1.5),
        t(600, 172, "Open to Summer 2027 software engineering internships — backend, full-stack and applied AI.", 18.5, SOFT, anchor="middle"),
        t(600, 202, "BENGALURU · HYDERABAD · PUNE · MUMBAI · REMOTE", 12.5, MUTED, 600, True, "middle", 2),
        f'<rect x="400" y="230" width="400" height="48" rx="24" fill="{EM}" fill-opacity="0.1" stroke="{EM}" stroke-opacity="0.45"/>',
        f'<circle class="pulse" cx="432" cy="254" r="8" fill="{EM}" fill-opacity="0.3"/><circle cx="432" cy="254" r="4" fill="{EM}"/>',
        t(612, 260, "srivastavaojas454@gmail.com", 16, TXT, 600, True, "middle"),
        t(600, 306, f"↗  {PORTFOLIO}", 13, CY, 600, True, "middle", 1),
    ]
    return doc("footer", W, H, "Let's build something that ships — open to Summer 2027 SWE internships. srivastavaojas454@gmail.com",
               "\n  ".join(b), defs)


def portfolio():
    tour = json.loads((ROOT / "assets" / "data" / "tour.json").read_text())
    W, H = 1200, 850
    vx, vy, vw, vh = 30, 110, 1140, 712
    slot = 3.4
    T = slot * len(tour)
    a, bfrac, c = 1.2, 100 / len(tour), 100 / len(tour) + 1.2
    css = (f".slide {{ opacity: 0; animation: slide {T:.1f}s linear infinite both; }}"
           f".zoom {{ transform-box: fill-box; transform-origin: center; animation: zoom {T:.1f}s linear infinite both; }}"
           f".prog {{ transform-box: fill-box; transform-origin: left; animation: prog {slot}s linear infinite; }}"
           f"@keyframes slide {{ 0% {{ opacity: 0; }} {a:.2f}% {{ opacity: 1; }} {bfrac:.2f}% {{ opacity: 1; }} {c:.2f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}"
           f"@keyframes zoom {{ 0% {{ transform: scale(1); }} {c:.2f}% {{ transform: scale(1.045); }} 100% {{ transform: scale(1.045); }} }}"
           f"@keyframes prog {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}")
    defs = (glow("pa", CY, .2) + glow("pb", EM, .16)
            + f'<clipPath id="vp"><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="14"/></clipPath>'
            + lin("vfade", BG, BG, True, 0, .85))
    labels = {"": "home", "#brief": "60-second brief", "#experience": "experience", "#projects": "projects",
              "#coding-stats": "live coding stats", "#achievements": "milestones", "#contact": "contact"}
    b = ['<ellipse cx="1000" cy="60" rx="480" ry="240" fill="url(#pa)"/>',
         '<ellipse cx="160" cy="800" rx="420" ry="220" fill="url(#pb)"/>',
         band(W, H)]
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b.append(f'<circle cx="{56 + i * 22}" cy="44" r="6.5" fill="{col}"/>')
    b.append(f'<rect x="140" y="26" width="880" height="36" rx="18" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.1"/>')
    b.append(f'<path d="M162 40h8v10h-8z M164 40v-3a2 2 0 0 1 4 0v3" stroke="{EM}" stroke-width="1.6"/>')
    b.append(f'<rect x="1040" y="26" width="130" height="36" rx="18" fill="{EM}" fill-opacity="0.12" stroke="{EM}" stroke-opacity="0.5"/>')
    b.append(f'<circle class="pulse" cx="1064" cy="44" r="7" fill="{EM}" fill-opacity="0.35"/><circle cx="1064" cy="44" r="3.5" fill="{EM}"/>')
    b.append(t(1080, 49, "LIVE SITE", 12, EM, 700, True, ls=1.4))
    for i in range(len(tour)):
        x0 = 30 + i * (1140 / len(tour))
        segw = 1140 / len(tour) - 8
        b.append(f'<rect x="{x0:.1f}" y="80" width="{segw:.1f}" height="3" rx="1.5" fill="#FFFFFF" fill-opacity="0.1"/>')
        b.append(f'<rect class="slide" style="animation-delay:{i * slot:.1f}s" x="{x0:.1f}" y="80" width="{segw:.1f}" height="3" rx="1.5" fill="url(#acc)"/>')
    b.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="14" fill="#05070A"/>')
    frames, urls, caps = [], [], []
    for i, f in enumerate(tour):
        data = base64.b64encode((ROOT / "assets" / "data" / f["file"]).read_bytes()).decode()
        st = f' class="slide" style="animation-delay:{i * slot:.1f}s"'
        frames.append(f'<g{st}><image class="zoom" style="animation-delay:{i * slot:.1f}s" href="data:image/jpeg;base64,{data}" '
                      f'x="{vx}" y="{vy}" width="{vw}" height="{vh}" preserveAspectRatio="xMidYMid slice"/></g>')
        urls.append(f'<g{st}>' + t(184, 49, f'<tspan fill="{TXT}">{PORTFOLIO}</tspan><tspan fill="{MUTED}">/{esc(f["hash"])}</tspan>', 14, TXT, 500, True, raw=True) + '</g>')
        lab = labels.get(f["hash"], f["hash"].lstrip("#"))
        caps.append(f'<g{st}>' + t(vx + 30, vy + vh - 30, f"{i + 1:02d} / {len(tour):02d}  ·  {lab.upper()}", 13, TXT, 700, True, ls=1.6) + '</g>')
    b.append('<g clip-path="url(#vp)">' + "".join(reversed(frames))
             + f'<rect x="{vx}" y="{vy + vh - 150}" width="{vw}" height="150" fill="url(#vfade)"/></g>')
    b += list(reversed(urls)) + list(reversed(caps))
    b.append(f'<rect x="{vx + .5}" y="{vy + .5}" width="{vw - 1}" height="{vh - 1}" rx="13.5" stroke="#FFFFFF" stroke-opacity="0.12"/>')
    b.append(sweep(vx + .5, vy + .5, vw - 1, vh - 1, 13.5, CY, 0, 2))
    b.append(f'<rect x="{vx + vw - 250}" y="{vy + vh - 56}" width="220" height="38" rx="19" fill="{EM}"/>')
    b.append(t(vx + vw - 140, vy + vh - 31, "OPEN PORTFOLIO  ↗", 13, BG, 800, True, "middle", 1.2))
    return doc("portfolio", W, H, f"Live portfolio preview — {PORTFOLIO}", "\n  ".join(b), defs, css)


def load_data():
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    lc_data = fetch("https://alfa-leetcode-api.onrender.com/Oju_Srivastava/contest") or {}
    lc = [round(p["rating"]) for p in lc_data.get("contestParticipation", []) if p.get("attended")]
    cf_data = fetch("https://codeforces.com/api/user.rating?handle=Oju") or {}
    cf = [r["newRating"] for r in cf_data.get("result", [])]
    solved = (fetch("https://alfa-leetcode-api.onrender.com/Oju_Srivastava/solved") or {}).get("solvedProblem")
    data = {
        "lc": lc if len(lc) >= len(cache.get("lc", [])) and lc else cache.get("lc", LC_FALLBACK),
        "cf": cf if len(cf) >= len(cache.get("cf", [])) and cf else cache.get("cf", CF_FALLBACK),
        "lc_solved": max(solved or 0, cache.get("lc_solved", 764)),
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(data) + "\n")
    return data


def main():
    data = load_data()
    lc, cf, solved = data["lc"], data["cf"], data["lc_solved"]
    lc_solved = f"{solved // 50 * 50}+"
    total = solved + 270 + 118
    total_s = f"{total // 50 * 50:,}+"

    write("hero.svg", hero(total_s))
    write("highlights.svg", highlights())
    write("cp.svg", cp(lc, cf, lc_solved, len(lc)))
    write("experience.svg", experience())
    write("footer.svg", footer())
    write("now.svg", now())
    if (ROOT / "assets" / "data" / "tour.json").exists():
        write("portfolio.svg", portfolio())
    for i, (title, sub) in enumerate([
        ("Highlights", "the short version"),
        ("Portfolio", "live tour · " + PORTFOLIO),
        ("Competitive Programming", "peaks, ratings & daily reps"),
        ("Featured Work", "shipped · deployed · public"),
        ("Experience & Leadership", "industry · leadership · academics"),
        ("Tech Stack", "tools I ship with"),
        ("GitHub Activity", "auto-updated twice a day"),
    ], 1):
        write(f"section-{i:02d}.svg", section(i, title, sub))

    projects = [
        ("work-logiflow.svg", CY, "GSC 2026 · GLOBAL TOP 106", "LogiFlow", "Decision intelligence for multi-modal logistics",
         [("15,650", "TRAIN-DAYS"), ("22.7 min", "DELAY MAE"), ("81%", "WITHIN 30 MIN")], "FastAPI · Next.js · Gradient Boosting · Gemini", "route"),
        ("work-community-hero.svg", EM, "VIBE2SHIP 2026 · GLOBAL TOP 20", "Community Hero", "CIVICPULSE AI — hyperlocal civic reporting PWA",
         [("Solo", "END-TO-END"), ("6", "AI AGENTS"), ("Open311", "CIVIC EXPORT")], "React · Express · Firebase · Gemini 2.5 Flash", "pin"),
        ("work-career-automation.svg", AM, "PRODUCTION · 8 GITHUB ACTIONS", "Career Automation", "Internship Scout · Hiring Scout · OA Forge",
         [("966", "COMPANIES"), ("10.7k+", "CONTACTS"), ("14k+", "OA QUESTIONS")], "Python · Supabase · GitHub Actions · C++ judge", "pipe"),
        ("work-airhelp.svg", VI, "POWERMIND HACKATHON 2026", "AirHelp", "Offline-first AI airport companion",
         [("A*", "INDOOR ROUTING"), ("RAG", "CHROMADB"), ("Voice", "WHISPER + PIPER")], "FastAPI · React · WebSockets · ChromaDB", "plane"),
        ("work-rangriti.svg", PK, "WEB WONDERS 2025 · TECH LEAD", "RangRiti", "Cultural-tech marketplace for Indian art",
         [("40+", "PAGES SHIPPED"), ("4", "ENGINEERS LED"), ("100%", "PRS REVIEWED")], "Node.js · Express · MongoDB · EJS · Render", "mandala"),
        ("work-options-pricing.svg", BL, "QUANT · C++17", "Options Pricing", "Monte Carlo & Black–Scholes for European options",
         [("100k", "GBM PATHS"), ("5", "GREEKS + IV"), ("MT19937", "PRNG")], "C++17 · STL <random> · <cmath> · -O2", "curve"),
    ]
    for p in projects:
        write(p[0], project(*p))
    print("ok", len(lc), len(cf), solved, total_s)


if __name__ == "__main__":
    main()
