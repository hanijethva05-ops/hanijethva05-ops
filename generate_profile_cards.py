import os
import urllib.request
import json

USERNAME = "hanijethva05-ops"
os.makedirs("assets", exist_ok=True)

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

user = fetch_json(f"https://api.github.com/users/{USERNAME}")
repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner")

public_repos = user.get("public_repos", 0)
followers = user.get("followers", 0)
total_stars = sum(r.get("stargazers_count", 0) for r in repos)

# Language byte counts across owned repos
lang_totals = {}
for r in repos:
    if r.get("fork"):
        continue
    lang_url = r.get("languages_url")
    if lang_url:
        try:
            ldata = fetch_json(lang_url)
            for k, v in ldata.items():
                lang_totals[k] = lang_totals.get(k, 0) + v
        except Exception:
            pass

sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)[:5]
total_bytes = sum(v for _, v in sorted_langs) or 1

palette = ["#bd93f9", "#ff79c6", "#50fa7b", "#8be9fd", "#ffb86c"]

# 1. Top Header Card (Photo ke top section jaisa)
header_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="230" viewBox="0 0 900 230">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b0d14"/>
      <stop offset="100%" stop-color="#131726"/>
    </linearGradient>
    <linearGradient id="neonLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#bd93f9"/>
      <stop offset="100%" stop-color="#ff79c6"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="896" height="226" rx="18" fill="url(#bgGrad)" stroke="#2b314a" stroke-width="2"/>
  <rect x="2" y="2" width="896" height="4" rx="2" fill="url(#neonLine)"/>

  <text x="34" y="42" fill="#bd93f9" font-family="monospace" font-size="14">@{USERNAME}</text>
  <text x="34" y="84" fill="#ffffff" font-family="sans-serif" font-size="34" font-weight="700">Hani Jethva</text>
  <text x="34" y="114" fill="#a8b2d1" font-family="sans-serif" font-size="16">Aspiring Software Developer &amp; Data Analyst</text>

  <rect x="34" y="136" width="105" height="28" rx="14" fill="#1e1b33" stroke="#bd93f9" stroke-width="1"/>
  <text x="86" y="155" text-anchor="middle" fill="#e2d9ff" font-family="monospace" font-size="12">Python</text>

  <rect x="148" y="136" width="85" height="28" rx="14" fill="#2b192e" stroke="#ff79c6" stroke-width="1"/>
  <text x="190" y="155" text-anchor="middle" fill="#ffd6ee" font-family="monospace" font-size="12">SQL</text>

  <rect x="242" y="136" width="125" height="28" rx="14" fill="#1e1b33" stroke="#bd93f9" stroke-width="1"/>
  <text x="304" y="155" text-anchor="middle" fill="#e2d9ff" font-family="monospace" font-size="12">JavaScript</text>

  <rect x="376" y="136" width="115" height="28" rx="14" fill="#2b192e" stroke="#ff79c6" stroke-width="1"/>
  <text x="433" y="155" text-anchor="middle" fill="#ffd6ee" font-family="monospace" font-size="12">Three.js</text>

  <!-- Right Stats Column -->
  <g font-family="sans-serif" font-size="15" fill="#dce3f7">
    <text x="530" y="62"><tspan fill="#bd93f9" font-weight="700">{public_repos}</tspan> Repositories</text>
    <text x="530" y="96"><tspan fill="#ff79c6" font-weight="700">{total_stars}</tspan> Stars</text>
    <text x="530" y="130"><tspan fill="#bd93f9" font-weight="700">{followers}</tspan> Followers</text>
    <text x="530" y="164"><tspan fill="#ff79c6" font-weight="700">{len(repos)}</tspan> Owned Repos</text>
  </g>

  <!-- Stylized Neon Badge Emblem on Right -->
  <circle cx="795" cy="115" r="58" fill="#171229" stroke="#ff79c6" stroke-width="2"/>
  <circle cx="795" cy="115" r="46" fill="none" stroke="#bd93f9" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="795" y="123" text-anchor="middle" fill="#ffffff" font-family="monospace" font-size="26" font-weight="700">HJ</text>
</svg>"""

with open("assets/header-card.svg", "w", encoding="utf-8") as f:
    f.write(header_svg)

# 2. Language Stack Card (Bottom-Left jaisa)
lang_rows = []
y_pos = 78
for idx, (lang, count) in enumerate(sorted_langs):
    pct = round((count / total_bytes) * 100, 1)
    bar_w = max(8, int((count / total_bytes) * 240))
    color = palette[idx % len(palette)]
    lang_rows.append(f"""
      <text x="24" y="{y_pos}" fill="#e6edf3" font-family="sans-serif" font-size="13" font-weight="600">{lang}</text>
      <text x="386" y="{y_pos}" text-anchor="end" fill="#9ea7c2" font-family="monospace" font-size="12">{pct}%</text>
      <rect x="24" y="{y_pos + 8}" width="362" height="8" rx="4" fill="#1e2336"/>
      <rect x="24" y="{y_pos + 8}" width="{bar_w}" height="8" rx="4" fill="{color}"/>
    """)
    y_pos += 44

lang_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="410" height="310" viewBox="0 0 410 310">
  <rect x="2" y="2" width="406" height="306" rx="16" fill="#0d101b" stroke="#282f47" stroke-width="2"/>
  <text x="24" y="34" fill="#ffffff" font-family="sans-serif" font-size="17" font-weight="700">Language Stack</text>
  <text x="24" y="54" fill="#8b95b5" font-family="sans-serif" font-size="12">Repository byte distribution</text>
  {''.join(lang_rows)}
</svg>"""

with open("assets/lang-card.svg", "w", encoding="utf-8") as f:
    f.write(lang_svg)

# 3. Featured Projects Card (Bottom-Right jaisa)
projects = [
    ("NOVAMART E-Commerce Analysis", "Sales, profitability & customer insights (Excel, SQL, Python, WPS)", "#bd93f9"),
    ("3D Developer Portfolio", "Interactive 3D portfolio built with HTML, CSS, JS, Three.js & GSAP", "#ff79c6"),
    ("AI Resume Analyzer", "Automated resume evaluation & insights workflow", "#bd93f9"),
    ("AI Hand Gesture Control", "Gesture-based interaction & control system", "#ff79c6"),
]

proj_boxes = []
py = 62
for title, desc, accent in projects:
    proj_boxes.append(f"""
      <rect x="22" y="{py}" width="426" height="54" rx="10" fill="#131829" stroke="#262d47" stroke-width="1.2"/>
      <rect x="22" y="{py}" width="5" height="54" rx="2" fill="{accent}"/>
      <text x="38" y="{py + 22}" fill="#ffffff" font-family="sans-serif" font-size="13" font-weight="700">{title}</text>
      <text x="38" y="{py + 41}" fill="#9ca6c7" font-family="sans-serif" font-size="11">{desc}</text>
    """)
    py += 63

proj_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="470" height="325" viewBox="0 0 470 325">
  <rect x="2" y="2" width="466" height="321" rx="16" fill="#0d101b" stroke="#282f47" stroke-width="2"/>
  <text x="22" y="34" fill="#ffffff" font-family="sans-serif" font-size="17" font-weight="700">Featured Projects</text>
  {''.join(proj_boxes)}
</svg>"""

with open("assets/projects-card.svg", "w", encoding="utf-8") as f:
    f.write(proj_svg)

print("Generated SVG cards successfully.")
