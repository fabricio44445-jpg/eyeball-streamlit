import base64
import hashlib
import html
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

ROOT = Path(__file__).parent
ASSETS = ROOT / "outputs" / "eyeball-redesign" / "assets"

# ---------------------------------------------------------------------------
# Creator data
# ---------------------------------------------------------------------------

FRENCH_CREATORS = [
    {"name": "Tesla Riviera",      "category": "EVs, Tesla and electromobility",          "audience": "~61.6K",  "url": "https://www.youtube.com/@TeslaRiviera",                               "image": "tesla-riviera.webp"},
    {"name": "Petit Copeau",       "category": "Woodworking, DIY and construction",        "audience": "~111K",   "url": "https://www.youtube.com/@petitcopeau",                                 "image": "petit-copeau.webp"},
    {"name": "Pascal Into The Wild","category": "Overlanding, 4x4 and outdoor travel",    "audience": "~68.3K",  "url": "https://www.youtube.com/@pascalintothewild",                           "image": "pascal-wild.webp"},
    {"name": "Baptiste Pitois",    "category": "Automotive builds and mechanics",          "audience": "~330K",   "url": "https://www.youtube.com/@BaptistePitois/videos",                       "image": "baptiste-pitois.webp"},
    {"name": "Jojol",              "category": "Consumer tech and product reviews",        "audience": "~2.6M",   "url": "https://www.youtube.com/@jojol",                                       "image": "jojol.webp"},
    {"name": "Amixem",             "category": "Entertainment, comedy and big concepts",   "audience": "~9.35M",  "url": "https://www.youtube.com/@Amixem",                                      "image": "amixem.webp"},
]

DE_CREATORS = [
    {"name": "MATTIN2",            "category": "Tech reviews, gadgets and consumer electronics",    "audience": "N/A",    "url": "https://www.youtube.com/@MATTIN2"},
    {"name": "Sibbershusum",       "category": "Farm life, agriculture and rural living",           "audience": "~110K",  "url": "https://www.youtube.com/@Sibbershusum/videos"},
    {"name": "commaik",            "category": "Home renovation, garden, DIY and smart home",       "audience": "N/A",    "url": "https://www.youtube.com/@commaik/videos"},
    {"name": "simon42",            "category": "Smart home, Home Assistant and automation",         "audience": "N/A",    "url": "https://www.youtube.com/@simon42/videos"},
    {"name": "RevealRabbit",       "category": "Tech unboxing and product reviews",                 "audience": "~160K",  "url": "https://www.youtube.com/@RevealRabbit/videos"},
    {"name": "NerdsHeaven",        "category": "Consumer tech, reviews and nerd culture",           "audience": "~230K",  "url": "https://www.youtube.com/@NerdsHeaven-de/videos"},
    {"name": "Womoblog",           "category": "Motorhome life, travel and van living",             "audience": "N/A",    "url": "https://www.youtube.com/@Womoblog/videos"},
    {"name": "MrTogi",             "category": "DIY, crafts and hands-on builds",                   "audience": "N/A",    "url": "https://www.youtube.com/@MrTogi/videos"},
    {"name": "mr.motovlogs",       "category": "Motorcycles, moto travel and vlogs",                "audience": "N/A",    "url": "https://www.youtube.com/@mr.motovlogs/videos"},
    {"name": "HomeBuildSolution",  "category": "Home building, construction and DIY",               "audience": "N/A",    "url": "https://www.youtube.com/c/HomeBuildSolution/videos"},
    {"name": "bergbrise",          "category": "Camping, vanlife, 4x4 and off-grid travel",         "audience": "N/A",    "url": "https://www.youtube.com/@bergbrise/videos"},
]

US_CREATORS = [
    {"name": "JoelsterG4K",        "category": "Consumer tech, gaming and entertainment reviews",   "audience": "~60.6K",  "url": "https://www.youtube.com/@JoelsterG4k/videos",                         "image": "joelster-g4k.webp"},
    {"name": "This Smart House",   "category": "Smart homes, Home Assistant and automation",        "audience": "~33.8K",  "url": "https://www.youtube.com/@ThisSmartHouse",                              "image": "this-smart-house.webp"},
    {"name": "Viny B",             "category": "Engineering, fabrication and project builds",       "audience": "~114K",   "url": "https://www.youtube.com/@VinyB57/videos",                             "image": "viny-b.webp"},
    {"name": "DoItYourselfDad",    "category": "DIY, repairs and practical home projects",          "audience": "~187K",   "url": "https://www.youtube.com/@DoItYourselfDad/videos",                     "image": "do-it-yourself-dad.webp"},
    {"name": "The 10 Acre Woods",  "category": "Farm life, animal rescue and family education",     "audience": "~56.9K",  "url": "https://www.youtube.com/channel/UCirFhr1Yk2ULP5cniE96S1g/videos",     "image": "ten-acre-woods.webp"},
    {"name": "Wanderer001 Reviews","category": "In-depth tech and smart-home reviews",              "audience": "~35.4K",  "url": "https://www.youtube.com/@Wanderer001_Reviews/videos",                 "image": "wanderer-reviews.webp"},
    {"name": "Shiny Tech Things",  "category": "Tech repair, servers, AI builds and reviews",      "audience": "~50.1K",  "url": "https://www.youtube.com/@ShinyTechThings/videos",                     "image": "shiny-tech-things.webp"},
    {"name": "Don Does Stuff",     "category": "Repairs, renovation and hands-on how-to projects",  "audience": "~2.01K",  "url": "https://www.youtube.com/@DonDoesStuff/videos",                        "image": "don-does-stuff.webp"},
]

TIKTOK_NA = [
    {"name": "GiftGecko",      "category": "Daily Amazon finds and product discovery",    "audience": "~582K",  "url": "https://www.tiktok.com/@giftgecko"},
    {"name": "ModernHomestead","category": "Homesteading, farming and rural family life",  "audience": "~220K",  "url": "https://www.tiktok.com/@modernhomestead"},
    {"name": "Nate Petroski",  "category": "Off-grid homesteading and outdoor living",    "audience": "~3.8M",  "url": "https://www.tiktok.com/@natepetroski"},
]

TIKTOK_DE = [
    {"name": "Dan Fuchs",          "category": "Life hacks, tips and household tricks",       "audience": "N/A", "url": "https://www.tiktok.com/@dan_fuchs"},
    {"name": "Fantastic Günter",   "category": "Entertainment and lifestyle content",         "audience": "N/A", "url": "https://www.tiktok.com/@fantastic_guenter"},
    {"name": "Flotomation",        "category": "Smart home, HomeKit and Home Assistant",      "audience": "N/A", "url": "https://www.tiktok.com/@flotomation"},
]

TIKTOK_FR = [
    {"name": "Picassiete",         "category": "Product tests and deals — Action & Lidl",    "audience": "N/A", "url": "https://www.tiktok.com/@picassiete"},
    {"name": "BricoTest",          "category": "DIY product tests and tool reviews",          "audience": "N/A", "url": "https://www.tiktok.com/@moela9581"},
]

BRANDS = [
    {
        "name": "EcoFlow",
        "category": "Portable power stations, solar panels and energy solutions for home and outdoor use.",
        "url": "https://www.ecoflow.com/us",
        "content_url": "https://drive.google.com/file/d/1bgYUxnAf5rwypqKgCXAqyQ1LCdCV9Bfb/view?usp=share_link",
    },
    {
        "name": "Reolink",
        "category": "Smart home security cameras, NVR systems and AI-powered surveillance solutions.",
        "url": "https://reolink.com/",
        "content_url": "https://drive.google.com/file/d/1QvJJYlo0rXcYBoOiL2DwhjijAe6QS8r_/view?usp=share_link",
    },
]

VIDEOS = {
    "Keynotes": [
        ("Keynote 01", "https://www.youtube.com/watch?v=fZW3RDq4nIM"),
        ("Keynote 02", "https://www.youtube.com/watch?v=eWRLxKudr8M"),
        ("Keynote 03", "https://www.dailymotion.com/video/x9xmnxk"),
    ],
    "Films": [
        ("Film 01", "https://www.youtube.com/watch?v=2Z_2iRpPPTc"),
        ("Film 02", "https://www.youtube.com/watch?v=5r9VJU6gmhY&t=44s"),
        ("Film 03", "https://www.youtube.com/watch?v=W9zfstsFmgQ"),
        ("Film 04", "https://www.youtube.com/watch?v=_zRGUiUX7E8"),
    ],
    "Music video": [
        ("Music video", "https://www.youtube.com/watch?v=i7d7g_h9ckw"),
    ],
    "Livestreams": [
        ("Livestream 01", "https://www.youtube.com/watch?v=1D_8tj3BgJ4"),
        ("Livestream 02", "https://www.youtube.com/watch?v=lVCghazyWpY"),
        ("Livestream 03", "https://www.youtube.com/watch?v=K4byp2Fr9p4&t=1821s"),
    ],
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Palette of muted dark colours for SVG avatars
_AVATAR_COLORS = [
    "#2a4a6b", "#3d5a3e", "#6b3a2a", "#4a3a6b",
    "#5a4a2a", "#2a5a5a", "#6b2a4a", "#3a4a5a",
]


def _svg_avatar(name: str) -> str:
    """Generate a base64 SVG circle-avatar with the creator's initials."""
    words = name.split()
    initials = (words[0][0] + (words[-1][0] if len(words) > 1 else "")).upper()
    idx = int(hashlib.md5(name.encode()).hexdigest(), 16) % len(_AVATAR_COLORS)
    color = _AVATAR_COLORS[idx]
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150">'
        f'<circle cx="75" cy="75" r="75" fill="{color}"/>'
        f'<text x="75" y="93" text-anchor="middle" fill="#e8e4db" '
        f'font-size="52" font-family="Georgia,serif" font-weight="400">{initials}</text>'
        f'</svg>'
    )
    encoded = base64.b64encode(svg.encode()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def image_data(filename: str) -> str:
    """Return base64 data-URI for a webp asset, or an SVG placeholder."""
    path = ASSETS / filename
    if not path.exists():
        name = filename.replace(".webp", "").replace("-", " ").replace("_", " ")
        return _svg_avatar(name)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def send_enquiry(name: str, email: str, phone: str, subject: str, message: str) -> None:
    config = st.secrets["email"]
    recipient = config.get("recipient", config["username"])
    mail = EmailMessage()
    mail["Subject"] = f"New Eyeball enquiry: {subject or 'Project enquiry'}"
    mail["From"] = config["username"]
    mail["To"] = recipient
    mail["Reply-To"] = email
    mail.set_content(
        f"Name: {name}\nEmail: {email}\nPhone: {phone or 'Not provided'}\n"
        f"Subject: {subject or 'Not provided'}\n\n{message}"
    )
    context = ssl.create_default_context()
    host = config.get("host", "smtp.gmail.com")
    port = int(config.get("port", 465))
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(config["username"], config["password"])
        server.send_message(mail)


def email_is_configured() -> bool:
    try:
        return "email" in st.secrets
    except StreamlitSecretNotFoundError:
        return False


# ---------------------------------------------------------------------------
# Card builders
# ---------------------------------------------------------------------------

def _yt_card(creator: dict) -> str:
    img = image_data(creator.get("image") or (creator["name"].lower().replace(" ", "-") + ".webp"))
    return (
        f'<a class="creator-card" href="{creator["url"]}" target="_blank" rel="noopener noreferrer">'
        f'<img src="{img}" alt="{html.escape(creator["name"])} profile">'
        f'<h3>{html.escape(creator["name"])}</h3>'
        f'<p>{html.escape(creator["category"])}</p>'
        f'<strong>{creator["audience"]}</strong>'
        f'<span>YouTube subscribers</span>'
        f'</a>'
    )


_TIKTOK_SVG = (
    '<svg class="tt-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5'
    ' 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01'
    'a6.33 6.33 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34'
    ' 6.34 6.34 0 0 0 6.33-6.34V8.69a8.18 8.18 0 0 0 4.78 1.52V6.75a4.85 4.85 0 0 1-1.01-.06z"/>'
    '</svg>'
)


def _tt_card(creator: dict) -> str:
    return (
        f'<a class="tt-card" href="{creator["url"]}" target="_blank" rel="noopener noreferrer">'
        f'{_TIKTOK_SVG}'
        f'<h3>{html.escape(creator["name"])}</h3>'
        f'<p>{html.escape(creator["category"])}</p>'
        f'<strong>{creator["audience"]}</strong>'
        f'<span class="tt-label">TikTok followers</span>'
        f'</a>'
    )


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Fabrice Klohoun | Global New Media and KOL Marketing",
    page_icon=".",
    layout="wide",
    initial_sidebar_state="collapsed",
)

hero_fallback = image_data("hero-studio.webp")
portrait      = image_data("fabrice-portrait.webp")

# ---------------------------------------------------------------------------
# CSS + Nav + Hero
# ---------------------------------------------------------------------------

st.markdown(f"""
<style>
:root {{
  --ink: #161715;
  --paper: #f2eee5;
  --ll: rgba(242,238,229,.22);
  --ld: rgba(22,23,21,.22);
}}
html {{ scroll-behavior: smooth; }}
body, .stApp {{ background: var(--paper); color: var(--ink); }}
.stApp, button, input, textarea {{ font-family: Arial, Helvetica, sans-serif; }}
header[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {{ display:none!important; }}
.block-container {{ max-width:none; padding:0; }}

/* NAV */
.eb-nav {{
  position:fixed; z-index:999; inset:0 0 auto 0; min-height:76px;
  padding:0 4vw; display:flex; align-items:center; justify-content:space-between;
  background:rgba(22,23,21,.94); color:var(--paper);
  border-bottom:1px solid var(--ll); backdrop-filter:blur(14px);
}}
.eb-brand {{ color:var(--paper)!important; font-size:1.35rem; font-weight:800; letter-spacing:-.05em; text-decoration:none!important; }}
.eb-links {{ display:flex; align-items:center; gap:2rem; }}
.eb-links a {{ color:var(--paper)!important; font-size:.72rem; letter-spacing:.12em; text-decoration:none!important; text-transform:uppercase; }}
.eb-cta {{ border:1px solid var(--paper); padding:.8rem 1.1rem; }}

/* HERO */
.hero {{ position:relative; min-height:100vh; overflow:hidden; background:var(--ink) url("{hero_fallback}") center/cover; color:var(--paper); }}
.hero-vid {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
.hero-vid iframe {{ position:absolute; top:50%; left:50%; width:max(100vw,177.78vh); height:max(56.25vw,100vh); border:0; transform:translate(-50%,-50%); }}
.hero-shade {{ position:absolute; inset:0; background:linear-gradient(90deg,rgba(22,23,21,.86),rgba(22,23,21,.18) 72%); }}
.hero-copy {{ position:absolute; z-index:2; left:7vw; bottom:11vh; max-width:920px; }}
.eyebrow, .sec-label {{ font-size:.7rem; letter-spacing:.17em; text-transform:uppercase; }}
.stApp .hero h1, .stApp .sec-title, .stApp .about-title, .stApp .contact-title {{
  font-family:Georgia,"Times New Roman",serif!important; font-weight:400; letter-spacing:-.045em;
}}
.hero h1 {{ margin:1.4rem 0 2.4rem; font-size:clamp(4rem,9vw,9rem); line-height:.88; }}
.hero-actions {{ display:flex; align-items:center; gap:2rem; }}
.light-btn {{ display:inline-block; padding:1rem 1.4rem; background:var(--paper); color:var(--ink)!important; font-size:.72rem; font-weight:700; letter-spacing:.12em; text-decoration:none!important; text-transform:uppercase; }}
.txt-link {{ padding-bottom:.35rem; border-bottom:1px solid currentColor; color:inherit!important; font-size:.76rem; letter-spacing:.1em; text-decoration:none!important; text-transform:uppercase; }}

/* SECTIONS */
.sec {{ padding:8rem 7vw; }}
.sec-dark {{ background:var(--ink); color:var(--paper); }}
.about-grid {{ display:grid; grid-template-columns:1fr 3fr; gap:3rem; }}
.about-title {{ max-width:1050px; margin:0 0 4rem; font-size:clamp(2.6rem,5vw,5.5rem); line-height:1.02; }}
.about-detail {{ max-width:650px; margin-left:34%; line-height:1.7; }}
.sec-heading {{ display:flex; align-items:end; justify-content:space-between; gap:2rem; margin-bottom:4rem; }}
.stApp .sec-title {{ margin:0; font-size:clamp(3rem,6vw,6rem)!important; }}
.mkt-intro {{ max-width:720px; margin:-1rem 0 4rem auto; color:rgba(242,238,229,.72); line-height:1.7; }}
.aud-note {{ font-size:.64rem; letter-spacing:.12em; text-transform:uppercase; }}

/* MARKET BLOCKS */
.mkt-block + .mkt-block {{ margin-top:7rem; padding-top:5rem; border-top:1px solid var(--ll); }}
.mkt-hdr {{ display:flex; align-items:end; justify-content:space-between; gap:2rem; margin-bottom:3.5rem; }}
.mkt-hdr h3 {{ margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.5rem,4.5vw,4.75rem); font-weight:400; letter-spacing:-.04em; }}

/* YT CREATOR CARDS */
.yt-grid-6 {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:3rem 1.5rem; }}
.yt-grid-4 {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:3rem 1.5rem; row-gap:4.5rem; }}
.creator-card {{ color:var(--paper)!important; text-align:center; text-decoration:none!important; }}
.creator-card img {{ width:min(150px,100%); aspect-ratio:1; margin:0 auto 1.4rem; border:1px solid var(--ll); border-radius:50%; object-fit:cover; }}
.creator-card h3 {{ min-height:2.5em; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:1.2rem; font-weight:400; }}
.creator-card p {{ min-height:3.8em; color:rgba(242,238,229,.62); font-size:.78rem; line-height:1.55; }}
.creator-card strong {{ display:block; font-family:Georgia,"Times New Roman",serif; font-size:1.7rem; font-weight:400; }}
.creator-card span {{ color:rgba(242,238,229,.56); font-size:.58rem; letter-spacing:.1em; text-transform:uppercase; }}

/* TIKTOK CARDS */
.tt-grid-3 {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:2rem; }}
.tt-grid-2 {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:2rem; }}
.tt-card {{ display:flex; flex-direction:column; align-items:center; text-align:center; color:var(--paper)!important; text-decoration:none!important; padding:1.8rem 1rem; border:1px solid var(--ll); transition:border-color .2s; }}
.tt-card:hover {{ border-color:rgba(242,238,229,.55); }}
.tt-icon {{ width:44px; height:44px; margin:0 auto 1.1rem; fill:var(--paper); opacity:.75; }}
.tt-card h3 {{ margin:0 0 .5rem; font-family:Georgia,"Times New Roman",serif; font-size:1.1rem; font-weight:400; }}
.tt-card p {{ color:rgba(242,238,229,.62); font-size:.78rem; line-height:1.55; margin:0 0 .8rem; flex-grow:1; }}
.tt-card strong {{ display:block; font-family:Georgia,"Times New Roman",serif; font-size:1.5rem; font-weight:400; }}
.tt-label {{ color:rgba(242,238,229,.56); font-size:.58rem; letter-spacing:.1em; text-transform:uppercase; }}
.tt-sub-hdr {{ font-size:.65rem; letter-spacing:.16em; text-transform:uppercase; color:rgba(242,238,229,.5); margin:0 0 1.5rem; }}
.tt-block + .tt-block {{ margin-top:3rem; padding-top:3rem; border-top:1px solid var(--ll); }}

/* BRANDS */
.brands-sec {{ padding:8rem 7vw; background:var(--paper); color:var(--ink); }}
.brand-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:2rem; margin-top:4rem; }}
.brand-card {{ border:1px solid var(--ld); padding:2.5rem; }}
.brand-card h3 {{ margin:0 0 .6rem; font-family:Georgia,"Times New Roman",serif; font-size:2.2rem; font-weight:400; letter-spacing:-.03em; }}
.brand-card p {{ color:rgba(22,23,21,.6); font-size:.85rem; line-height:1.65; margin:0 0 1.6rem; max-width:420px; }}
.brand-links {{ display:flex; gap:1.5rem; }}
.brand-link {{ font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; color:var(--ink)!important; text-decoration:none!important; border-bottom:1px solid var(--ink); padding-bottom:.2rem; }}

/* VIDEO */
.vid-heading {{ padding:8rem 7vw 2rem; }}
div[data-testid="stTabs"] {{ padding:0 7vw 7rem; }}
div[data-testid="stTabs"] button {{ letter-spacing:.08em; text-transform:uppercase; }}
div[data-testid="stVideo"] {{ background:var(--ink); }}
.vid-name {{ margin:.5rem 0 1.7rem; font-family:Georgia,"Times New Roman",serif; font-size:1.25rem; }}

/* CONTACT */
.contact-shell {{ padding:8rem 7vw 2rem; background:var(--ink); color:var(--paper); }}
.stApp .contact-title {{ max-width:900px; margin:1rem 0 2rem; font-size:clamp(3rem,6vw,6.5rem)!important; line-height:.96; }}
.contact-intro {{ max-width:700px; color:rgba(242,238,229,.7); line-height:1.7; }}
.contact-profile {{ display:flex; align-items:center; gap:1rem; margin-top:2.5rem; }}
.contact-profile img {{ width:88px; height:88px; border-radius:50%; object-fit:cover; }}
.contact-profile strong {{ display:block; font-family:Georgia,"Times New Roman",serif; font-size:1.25rem; font-weight:400; }}
.contact-profile span {{ color:rgba(242,238,229,.56); font-size:.62rem; letter-spacing:.1em; text-transform:uppercase; }}
.contact-anchor {{ height:1px; margin-top:-1px; background:var(--ink); }}
div[data-testid="stForm"] {{ margin:0; padding:2rem 7vw 8rem; border:0; border-radius:0; background:var(--ink); }}
div[data-testid="stForm"] label, div[data-testid="stForm"] p {{ color:var(--paper)!important; }}
div[data-testid="stForm"] input, div[data-testid="stForm"] textarea {{ color:var(--paper); border-color:var(--ll); background:transparent; }}
div[data-testid="stForm"] button {{ width:100%; border:0; border-radius:0; background:var(--paper); color:var(--ink); font-weight:700; letter-spacing:.1em; text-transform:uppercase; }}

/* FOOTER */
.site-footer {{ display:flex; justify-content:space-between; padding:2rem 4vw; background:var(--paper); font-size:.68rem; letter-spacing:.1em; text-transform:uppercase; }}

/* RESPONSIVE */
@media(max-width:1200px) and (min-width:821px) {{
  .yt-grid-6 {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .yt-grid-4 {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
}}
@media(max-width:820px) {{
  .eb-nav {{ min-height:68px; }}
  .eb-links a:not(.eb-cta) {{ display:none; }}
  .hero-copy {{ left:6vw; right:6vw; }}
  .hero-actions {{ align-items:flex-start; flex-direction:column; }}
  .sec {{ padding:6rem 6vw; }}
  .about-grid {{ grid-template-columns:1fr; }}
  .about-detail {{ margin-left:0; }}
  .sec-heading {{ display:block; }}
  .sec-title {{ margin-top:2rem; }}
  .mkt-intro {{ margin:2rem 0 3.5rem; }}
  .mkt-block + .mkt-block {{ margin-top:5rem; padding-top:4rem; }}
  .mkt-hdr {{ display:block; }}
  .mkt-hdr h3 {{ margin-top:1.5rem; }}
  .yt-grid-6, .yt-grid-4 {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:3rem 1.25rem; row-gap:3rem; }}
  .tt-grid-3, .tt-grid-2 {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
  .brand-grid {{ grid-template-columns:1fr; }}
  .creator-card h3, .creator-card p {{ min-height:0; }}
  .vid-heading, .contact-shell {{ padding:6rem 6vw 2rem; }}
  div[data-testid="stTabs"] {{ padding:0 6vw 5rem; }}
  div[data-testid="stForm"] {{ padding:2rem 6vw 6rem; }}
  .site-footer {{ flex-direction:column; gap:1rem; }}
}}
</style>

<nav class="eb-nav">
  <a class="eb-brand" href="#top">EYEBALL.</a>
  <div class="eb-links">
    <a href="#about">About</a>
    <a href="#creators">Creators</a>
    <a href="#brands">Brands</a>
    <a href="#videos">Videos</a>
    <a class="eb-cta" href="#contact">Connect</a>
  </div>
</nav>

<section class="hero" id="top">
  <div class="hero-vid">
    <iframe src="https://www.youtube-nocookie.com/embed/w4dZOI2VA0s?autoplay=1&mute=1&controls=0&loop=1&playlist=w4dZOI2VA0s&playsinline=1&rel=0&disablekb=1"
      title="Background film" allow="autoplay; encrypted-media" tabindex="-1"></iframe>
  </div>
  <div class="hero-shade"></div>
  <div class="hero-copy">
    <p class="eyebrow">Global New Media + KOL Marketing / Shenzhen</p>
    <h1>See the world<br>in different ways.</h1>
    <div class="hero-actions">
      <a class="light-btn" href="#creators">Explore the network</a>
      <a class="txt-link" href="#contact">Start a project ↗</a>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------
st.markdown("""
<section class="sec" id="about">
  <div class="about-grid">
    <div class="sec-label">01 &nbsp; About</div>
    <div>
      <h2 class="about-title">Fabrice helps consumer technology brands grow globally through creators, content and culture.</h2>
      <div class="about-detail">
        <p>He is a global new media and KOL marketing leader with experience building international creator programs, managing multicultural content teams and leading brand communications across North America, Europe and Asia.</p>
        <p>His work connects social strategy, product launches, livestreams, community building and data-led ROI optimization. He currently manages a 20+ person social, KOL and creative team and has helped scale creator partnerships, brand visibility and channel revenue for major Chinese consumer technology companies.</p>
        <p>With a master's degree in Software Engineering focused on Big Data, Fabrice combines analytical decision-making with hands-on strengths in photography, filmmaking, public speaking and cross-cultural storytelling.</p>
        <a class="txt-link" href="https://www.instagram.com/fabriceraw" target="_blank">Follow @fabriceraw ↗</a>
      </div>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Creator network
# ---------------------------------------------------------------------------

fr_cards = "".join(_yt_card(c) for c in FRENCH_CREATORS)
de_cards = "".join(_yt_card(c) for c in DE_CREATORS)
us_cards = "".join(_yt_card(c) for c in US_CREATORS)
tt_na    = "".join(_tt_card(c) for c in TIKTOK_NA)
tt_de    = "".join(_tt_card(c) for c in TIKTOK_DE)
tt_fr    = "".join(_tt_card(c) for c in TIKTOK_FR)

st.markdown(f"""
<section class="sec sec-dark" id="creators">

  <div class="sec-heading">
    <div class="sec-label">02 &nbsp; Creator network</div>
    <h2 class="sec-title">Creators in house.</h2>
  </div>

  <!-- YouTube · France -->
  <div class="mkt-block">
    <div class="mkt-hdr">
      <div class="sec-label">YouTube · France</div>
      <h3>French market.</h3>
    </div>
    <div class="mkt-intro">
      <p>A ready-to-activate French creator bench spanning technology, mobility, craftsmanship, automotive and entertainment.</p>
      <p class="aud-note">Approximate YouTube audience, June 2026.</p>
    </div>
    <div class="yt-grid-6">{fr_cards}</div>
  </div>

  <!-- YouTube · Germany -->
  <div class="mkt-block">
    <div class="mkt-hdr">
      <div class="sec-label">YouTube · Germany</div>
      <h3>German market.</h3>
    </div>
    <div class="mkt-intro">
      <p>A curated German roster covering smart home, home automation, DIY, outdoor living, camping, tech reviews and hands-on builds.</p>
      <p class="aud-note">Approximate YouTube audience, June 2026. N/A = not publicly indexed.</p>
    </div>
    <div class="yt-grid-4">{de_cards}</div>
  </div>

  <!-- YouTube · US -->
  <div class="mkt-block">
    <div class="mkt-hdr">
      <div class="sec-label">YouTube · United States</div>
      <h3>US market.</h3>
    </div>
    <div class="mkt-intro">
      <p>A practical US-market roster covering consumer technology, smart homes, engineering builds, DIY, repairs, product reviews and family-focused rural content.</p>
      <p class="aud-note">Approximate YouTube audience, June 2026.</p>
    </div>
    <div class="yt-grid-4">{us_cards}</div>
  </div>

  <!-- TikTok -->
  <div class="mkt-block">
    <div class="mkt-hdr">
      <div class="sec-label">TikTok · Global</div>
      <h3>TikTok network.</h3>
    </div>
    <div class="mkt-intro">
      <p>Short-form creators across North America, Germany and France — from off-grid homesteading and smart home automation to product discovery and hands-on DIY tests.</p>
      <p class="aud-note">Approximate TikTok audience, June 2026. N/A = not publicly indexed.</p>
    </div>

    <div class="tt-block">
      <p class="tt-sub-hdr">North America</p>
      <div class="tt-grid-3">{tt_na}</div>
    </div>

    <div class="tt-block">
      <p class="tt-sub-hdr">Germany</p>
      <div class="tt-grid-3">{tt_de}</div>
    </div>

    <div class="tt-block">
      <p class="tt-sub-hdr">France</p>
      <div class="tt-grid-2">{tt_fr}</div>
    </div>
  </div>

</section>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Brand partners
# ---------------------------------------------------------------------------

brand_cards = "".join(
    f'<div class="brand-card">'
    f'<h3>{html.escape(b["name"])}</h3>'
    f'<p>{html.escape(b["category"])}</p>'
    f'<div class="brand-links">'
    f'<a class="brand-link" href="{b["url"]}" target="_blank" rel="noopener noreferrer">Visit brand ↗</a>'
    f'<a class="brand-link" href="{b["content_url"]}" target="_blank" rel="noopener noreferrer">View content ↗</a>'
    f'</div></div>'
    for b in BRANDS
)

st.markdown(f"""
<section class="brands-sec" id="brands">
  <div class="sec-heading">
    <div class="sec-label">03 &nbsp; Brand partners</div>
    <h2 class="sec-title" style="font-family:Georgia,serif;font-weight:400;letter-spacing:-.045em;">Brands we&rsquo;ve built for.</h2>
  </div>
  <div class="mkt-intro" style="color:rgba(22,23,21,.65);margin-left:auto;margin-top:-1rem;margin-bottom:0;">
    <p>A selection of consumer technology brands worked with across campaign strategy, creator activations, content production and global KOL rollouts.</p>
  </div>
  <div class="brand-grid">{brand_cards}</div>
</section>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Video library
# ---------------------------------------------------------------------------

st.markdown("""
<section class="vid-heading" id="videos">
  <div class="sec-heading">
    <div class="sec-label">04 &nbsp; Video library</div>
    <h2 class="sec-title">Stories in motion.</h2>
  </div>
</section>
""", unsafe_allow_html=True)

tabs = st.tabs(list(VIDEOS))
for tab, (category, videos) in zip(tabs, VIDEOS.items()):
    with tab:
        columns = st.columns(3)
        for index, (label, url) in enumerate(videos):
            with columns[index % 3]:
                if "dailymotion.com" in url:
                    st.markdown(
                        '<iframe src="https://www.dailymotion.com/embed/video/x9xmnxk" '
                        'style="width:100%;aspect-ratio:16/9;border:0" '
                        'allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.video(url)
                st.markdown(f'<p class="vid-name">{html.escape(label)}</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

st.markdown(f"""
<div class="contact-anchor" id="contact"></div>
<section class="contact-shell">
  <div class="sec-label">05 &nbsp; Contact</div>
  <p class="eyebrow" style="margin-top:4rem">Build global attention</p>
  <h2 class="contact-title">Let&rsquo;s turn strategy into influence and growth.</h2>
  <p class="contact-intro">Get in touch about global social media strategy, KOL and creator partnerships, product launches, content production, livestreams or international brand growth.</p>
  <div class="contact-profile">
    <img src="{portrait}" alt="Portrait of Fabrice Klohoun">
    <div>
      <strong>Fabrice Klohoun</strong>
      <span>Global New Media + KOL Marketing<br>Shenzhen, China</span>
    </div>
  </div>
</section>
""", unsafe_allow_html=True)

with st.form("project_enquiry", clear_on_submit=True):
    first, second = st.columns(2)
    name    = first.text_input("Name")
    email   = second.text_input("Email")
    phone   = first.text_input("Phone")
    subject = second.text_input("Subject")
    message = st.text_area("Message", height=150)
    submitted = st.form_submit_button("Send enquiry")

    if submitted:
        if not name or not email or not message:
            st.error("Please provide your name, email and message.")
        elif not email_is_configured():
            st.warning(
                "Email delivery is not configured yet. Add the email settings described "
                "in README.md to the Streamlit app secrets."
            )
            mail_subject = html.escape(subject or "Project enquiry", quote=True)
            st.markdown(
                f'<a href="mailto:klohounfabrice@gmail.com?subject={mail_subject}">Email Fabrice directly</a>',
                unsafe_allow_html=True,
            )
        else:
            try:
                send_enquiry(name, email, phone, subject, message)
                st.success("Thank you. Your enquiry has been sent.")
            except (OSError, smtplib.SMTPException) as exc:
                st.error(f"The message could not be sent. Please email klohounfabrice@gmail.com. ({exc})")

st.markdown("""
<div class="site-footer">
  <strong>EYEBALL.</strong>
  <span>Global new media + KOL marketing</span>
  <span>&copy; 2026 Eyeball</span>
</div>
""", unsafe_allow_html=True)
