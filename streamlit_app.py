import base64
import html
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

ROOT = Path(__file__).parent
ASSETS = ROOT / "outputs" / "eyeball-redesign" / "assets"

FRENCH_CREATORS = [
    {
        "name": "Tesla Riviera",
        "category": "EVs, Tesla and electromobility",
        "audience": "~61.6K",
        "url": "https://www.youtube.com/@TeslaRiviera",
        "image": "tesla-riviera.webp",
    },
    {
        "name": "Petit Copeau",
        "category": "Woodworking, DIY and construction",
        "audience": "~111K",
        "url": "https://www.youtube.com/@petitcopeau",
        "image": "petit-copeau.webp",
    },
    {
        "name": "Pascal Into The Wild",
        "category": "Overlanding, 4x4 and outdoor travel",
        "audience": "~68.3K",
        "url": "https://www.youtube.com/@pascalintothewild",
        "image": "pascal-wild.webp",
    },
    {
        "name": "Baptiste Pitois",
        "category": "Automotive builds and mechanics",
        "audience": "~330K",
        "url": "https://www.youtube.com/@BaptistePitois/videos",
        "image": "baptiste-pitois.webp",
    },
    {
        "name": "Jojol",
        "category": "Consumer tech and product reviews",
        "audience": "~2.6M",
        "url": "https://www.youtube.com/@jojol",
        "image": "jojol.webp",
    },
    {
        "name": "Amixem",
        "category": "Entertainment, comedy and big concepts",
        "audience": "~9.35M",
        "url": "https://www.youtube.com/@Amixem",
        "image": "amixem.webp",
    },
]

US_CREATORS = [
    {
        "name": "JoelsterG4K",
        "category": "Consumer tech, gaming and entertainment reviews",
        "audience": "~60.6K",
        "url": "https://www.youtube.com/@JoelsterG4k/videos",
        "image": "joelster-g4k.webp",
    },
    {
        "name": "This Smart House",
        "category": "Smart homes, Home Assistant and automation",
        "audience": "~33.8K",
        "url": "https://www.youtube.com/@ThisSmartHouse",
        "image": "this-smart-house.webp",
    },
    {
        "name": "Viny B",
        "category": "Engineering, fabrication and project builds",
        "audience": "~114K",
        "url": "https://www.youtube.com/@VinyB57/videos",
        "image": "viny-b.webp",
    },
    {
        "name": "DoItYourselfDad",
        "category": "DIY, repairs and practical home projects",
        "audience": "~187K",
        "url": "https://www.youtube.com/@DoItYourselfDad/videos",
        "image": "do-it-yourself-dad.webp",
    },
    {
        "name": "The 10 Acre Woods",
        "category": "Farm life, animal rescue and family education",
        "audience": "~56.9K",
        "url": "https://www.youtube.com/channel/UCirFhr1Yk2ULP5cniE96S1g/videos",
        "image": "ten-acre-woods.webp",
    },
    {
        "name": "Wanderer001 Reviews",
        "category": "In-depth tech and smart-home reviews",
        "audience": "~35.4K",
        "url": "https://www.youtube.com/@Wanderer001_Reviews/videos",
        "image": "wanderer-reviews.webp",
    },
    {
        "name": "Shiny Tech Things",
        "category": "Tech repair, servers, AI builds and reviews",
        "audience": "~50.1K",
        "url": "https://www.youtube.com/@ShinyTechThings/videos",
        "image": "shiny-tech-things.webp",
    },
    {
        "name": "Don Does Stuff",
        "category": "Repairs, renovation and hands-on how-to projects",
        "audience": "~2.01K",
        "url": "https://www.youtube.com/@DonDoesStuff/videos",
        "image": "don-does-stuff.webp",
    },
]

GERMAN_CREATORS = [
    {
        "name": "MATTIN",
        "category": "Outdoor adventure, survival and entertainment",
        "audience": "~656K",
        "url": "https://www.youtube.com/@MATTIN2",
        "image": "de-mattin.webp",
    },
    {
        "name": "Sibbershusum",
        "category": "Farming, machinery and rural family life",
        "audience": "~110K",
        "url": "https://www.youtube.com/@Sibbershusum/videos",
        "image": "de-sibbershusum.webp",
    },
    {
        "name": "commaik",
        "category": "Renovation, gardens, DIY and smart homes",
        "audience": "~24K",
        "url": "https://www.youtube.com/@commaik/videos",
        "image": "de-commaik.webp",
    },
    {
        "name": "simon42",
        "category": "Home Assistant, smart homes and tech tutorials",
        "audience": "~203K",
        "url": "https://www.youtube.com/@simon42/videos",
        "image": "de-simon42.webp",
    },
    {
        "name": "Reveal Rabbit",
        "category": "Consumer technology, cameras, drones and reviews",
        "audience": "~160K",
        "url": "https://www.youtube.com/@RevealRabbit/videos",
        "image": "de-reveal-rabbit.webp",
    },
    {
        "name": "NerdsHeaven.de",
        "category": "Gadgets, mystery boxes and retro technology",
        "audience": "~230K",
        "url": "https://www.youtube.com/@NerdsHeaven-de/videos",
        "image": "de-nerds-heaven.webp",
    },
    {
        "name": "Womo.blog",
        "category": "Motorhomes, vanlife, travel and DIY",
        "audience": "~72.3K",
        "url": "https://www.youtube.com/@Womoblog/videos",
        "image": "de-womoblog.webp",
    },
    {
        "name": "Mr. Togi",
        "category": "Power stations, solar and camping technology",
        "audience": "~84.9K",
        "url": "https://www.youtube.com/@MrTogi/videos",
        "image": "de-mr-togi.webp",
    },
    {
        "name": "Mr. Moto",
        "category": "Tractors, workshop projects and firewood",
        "audience": "~105K",
        "url": "https://www.youtube.com/@mr.motovlogs/videos",
        "image": "de-mr-moto.webp",
    },
    {
        "name": "Home Build Solution",
        "category": "Construction, renovation and building projects",
        "audience": "~111K",
        "url": "https://www.youtube.com/c/HomeBuildSolution/videos",
        "image": "de-home-build-solution.webp",
    },
    {
        "name": "bergbrise-camping",
        "category": "Camping, vanlife, 4x4 and off-grid technology",
        "audience": "~72.6K",
        "url": "https://www.youtube.com/@bergbrise/videos",
        "image": "de-bergbrise.webp",
    },
]

TIKTOK_CREATORS = {
    "North America": [
        {
            "name": "Gift Gecko",
            "category": "Amazon finds and product discovery",
            "audience": "~582.4K",
            "url": "https://www.tiktok.com/@giftgecko",
            "image": "tt-giftgecko.webp",
        },
        {
            "name": "Modern Homestead",
            "category": "Homesteading, building, animals and outdoors",
            "audience": "~243.9K",
            "url": "https://www.tiktok.com/@modernhomestead",
            "image": "tt-modern-homestead.webp",
        },
        {
            "name": "Nate Petroski",
            "category": "Off-grid homesteading and outdoor living",
            "audience": "~3.8M",
            "url": "https://www.tiktok.com/@natepetroski",
            "image": "tt-nate-petroski.webp",
        },
    ],
    "Germany": [
        {
            "name": "Dan Fuchs",
            "category": "Life hacks, household tips and cleaning",
            "audience": "~313.1K",
            "url": "https://www.tiktok.com/@dan_fuchs",
            "image": "tt-dan-fuchs.webp",
        },
        {
            "name": "fantastic_guenter",
            "category": "Creative solutions for everyday problems",
            "audience": "~166.5K",
            "url": "https://www.tiktok.com/@fantastic_guenter",
            "image": "tt-fantastic-guenter.webp",
        },
        {
            "name": "flotomation",
            "category": "Home Assistant, automation and smart homes",
            "audience": "~8.1K",
            "url": "https://www.tiktok.com/@flotomation",
            "image": "tt-flotomation.webp",
        },
    ],
    "France": [
        {
            "name": "Picassiete",
            "category": "Product tests and buying advice",
            "audience": "~361.6K",
            "url": "https://www.tiktok.com/@picassiete",
            "image": "tt-picassiete.webp",
        },
        {
            "name": "BricoTest Officiel",
            "category": "High-tech tests, tips and product discovery",
            "audience": "~661.7K",
            "url": "https://www.tiktok.com/@moela9581",
            "image": "tt-bricotest.webp",
        },
    ],
}

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


def image_data(filename: str) -> str:
    path = ASSETS / filename
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
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone or 'Not provided'}\n"
        f"Subject: {subject or 'Not provided'}\n\n"
        f"{message}"
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


st.set_page_config(
    page_title="Fabrice Klohoun | Global New Media and KOL Marketing",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

hero_fallback = image_data("hero-studio.webp")
portrait = image_data("fabrice-portrait.webp")
ecoflow_preview = image_data("ecoflow-content-preview.webp")
reolink_preview = image_data("reolink-content-preview.webp")

st.markdown(
    f"""
    <style>
    :root {{
      --ink: #161715;
      --paper: #f2eee5;
      --line-light: rgba(242, 238, 229, .22);
      --line-dark: rgba(22, 23, 21, .22);
      --glass-light: rgba(255, 255, 255, .12);
      --glass-dark: rgba(10, 12, 11, .34);
    }}
    html {{ scroll-behavior: smooth; }}
    body, .stApp {{ background: var(--paper); color: var(--ink); }}
    .stApp, button, input, textarea {{ font-family: Arial, Helvetica, sans-serif; }}
    header[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {{
      display: none !important;
    }}
    .block-container {{
      max-width: none;
      padding: 0;
    }}
    .eyeball-nav {{
      position: fixed;
      z-index: 999;
      inset: 0 0 auto 0;
      min-height: 76px;
      padding: 0 4vw;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(22, 23, 21, .94);
      color: var(--paper);
      border-bottom: 1px solid var(--line-light);
      backdrop-filter: blur(14px);
    }}
    .eyeball-brand {{
      color: var(--paper) !important;
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -.05em;
      text-decoration: none !important;
    }}
    .eyeball-links {{ display: flex; align-items: center; gap: 2rem; }}
    .eyeball-links a {{
      color: var(--paper) !important;
      font-size: .72rem;
      letter-spacing: .12em;
      text-decoration: none !important;
      text-transform: uppercase;
    }}
    .eyeball-links .nav-cta {{ border: 1px solid var(--paper); padding: .8rem 1.1rem; }}
    .hero {{
      position: relative;
      min-height: 100vh;
      overflow: hidden;
      background: var(--ink) url("{hero_fallback}") center / cover;
      color: var(--paper);
    }}
    .hero-video {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    .hero-video iframe {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: max(100vw, 177.78vh);
      height: max(56.25vw, 100vh);
      border: 0;
      transform: translate(-50%, -50%);
    }}
    .hero-shade {{
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg, rgba(22,23,21,.86), rgba(22,23,21,.18) 72%);
    }}
    .hero-copy {{
      position: absolute;
      z-index: 2;
      left: 7vw;
      bottom: 11vh;
      max-width: 920px;
    }}
    .eyebrow, .section-label {{
      font-size: .7rem;
      letter-spacing: .17em;
      text-transform: uppercase;
    }}
    .stApp .hero h1, .stApp .section-title, .stApp .about-title, .stApp .contact-title {{
      font-family: Georgia, "Times New Roman", serif !important;
      font-weight: 400;
      letter-spacing: -.045em;
    }}
    .hero h1, .section-dark .section-title, .contact-title {{
      color: transparent;
      background: linear-gradient(145deg, #ffffff 8%, #f2eee5 48%, #aaa79f 100%);
      -webkit-background-clip: text;
      background-clip: text;
      filter: drop-shadow(0 12px 22px rgba(0,0,0,.28));
    }}
    .about-title, .brands-section .section-title, .video-heading .section-title {{
      color: transparent;
      background: linear-gradient(145deg, #101210 10%, #3f413d 54%, #8c8e87 100%);
      -webkit-background-clip: text;
      background-clip: text;
      filter: drop-shadow(0 12px 20px rgba(22,23,21,.16));
    }}
    .hero h1 {{
      margin: 1.4rem 0 2.4rem;
      font-size: clamp(4rem, 9vw, 9rem);
      line-height: .88;
    }}
    .hero-actions {{ display: flex; align-items: center; gap: 2rem; }}
    .light-button {{
      display: inline-block;
      padding: 1rem 1.4rem;
      background: var(--paper);
      color: var(--ink) !important;
      font-size: .72rem;
      font-weight: 700;
      letter-spacing: .12em;
      text-decoration: none !important;
      text-transform: uppercase;
    }}
    .text-link {{
      padding-bottom: .35rem;
      border-bottom: 1px solid currentColor;
      color: inherit !important;
      font-size: .76rem;
      letter-spacing: .1em;
      text-decoration: none !important;
      text-transform: uppercase;
    }}
    .section {{ padding: 8rem 7vw; }}
    .section-dark {{ background: var(--ink); color: var(--paper); }}
    .about-grid {{ display: grid; grid-template-columns: 1fr 3fr; gap: 3rem; }}
    .about-title {{
      max-width: 1050px;
      margin: 0 0 4rem;
      font-size: clamp(2.6rem, 5vw, 5.5rem);
      line-height: 1.02;
    }}
    .about-detail {{ max-width: 650px; margin-left: 34%; line-height: 1.7; }}
    .section-heading {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 2rem;
      margin-bottom: 4rem;
    }}
    .stApp .section-title {{ margin: 0; font-size: clamp(3rem, 6vw, 6rem) !important; }}
    .market-intro {{
      max-width: 720px;
      margin: -1rem 0 4rem auto;
      color: rgba(242,238,229,.72);
      line-height: 1.7;
    }}
    .audience-note {{ font-size: .64rem; letter-spacing: .12em; text-transform: uppercase; }}
    .creator-grid {{ display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 3rem 1.5rem; }}
    .market-block {{
      display: block;
      margin-top: 1rem;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,.16);
      border-radius: 24px;
      background:
        linear-gradient(135deg, rgba(255,255,255,.11), rgba(255,255,255,.025) 45%, rgba(0,0,0,.16)),
        var(--glass-dark);
      box-shadow: inset 0 1px 0 rgba(255,255,255,.18), 0 20px 45px rgba(0,0,0,.2);
      backdrop-filter: blur(18px) saturate(130%);
    }}
    .market-summary {{
      display: grid;
      grid-template-columns: minmax(120px, .55fr) 2fr auto;
      align-items: center;
      gap: 2rem;
      padding: 2.5rem 2rem;
      cursor: pointer;
      list-style: none;
    }}
    .market-summary::-webkit-details-marker {{ display: none; }}
    .market-summary h3 {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(2.5rem, 4.5vw, 4.75rem);
      font-weight: 400;
      letter-spacing: -.04em;
      text-shadow: 0 2px 0 rgba(255,255,255,.14), 0 14px 25px rgba(0,0,0,.28);
    }}
    .accordion-icon {{
      position: relative;
      width: 2rem;
      height: 2rem;
      border: 1px solid var(--line-light);
      border-radius: 50%;
    }}
    .accordion-icon::before,
    .accordion-icon::after {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: .8rem;
      height: 1px;
      background: var(--paper);
      content: "";
      transform: translate(-50%, -50%);
      transition: transform .2s ease;
    }}
    .accordion-icon::after {{ transform: translate(-50%, -50%) rotate(90deg); }}
    details[open] > .market-summary .accordion-icon::after {{ transform: translate(-50%, -50%) rotate(0); }}
    .market-content {{ padding: 1rem 2rem 5rem; border-top: 1px solid rgba(255,255,255,.1); }}
    .us-creator-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); row-gap: 4.5rem; }}
    .de-creator-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); row-gap: 4.5rem; }}
    .tiktok-block {{ margin-top: 4rem; }}
    .tiktok-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); row-gap: 4.5rem; }}
    .creator-card {{ color: var(--paper) !important; text-align: center; text-decoration: none !important; }}
    .creator-card img {{
      width: min(150px, 100%);
      aspect-ratio: 1;
      margin: 0 auto 1.4rem;
      border: 1px solid var(--line-light);
      border-radius: 50%;
      object-fit: cover;
    }}
    .creator-card h3 {{
      min-height: 2.5em;
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 1.2rem;
      font-weight: 400;
      text-shadow: 0 8px 18px rgba(0,0,0,.28);
    }}
    .creator-card p {{ min-height: 3.8em; color: rgba(242,238,229,.62); font-size: .78rem; line-height: 1.55; }}
    .creator-card strong {{ display: block; font-family: Georgia, "Times New Roman", serif; font-size: 1.7rem; font-weight: 400; text-shadow: 0 8px 18px rgba(0,0,0,.3); }}
    .creator-card span {{ color: rgba(242,238,229,.56); font-size: .58rem; letter-spacing: .1em; text-transform: uppercase; }}
    .video-section {{ padding-bottom: 3rem; }}
    .brands-section {{ padding: 8rem 7vw; border-bottom: 1px solid var(--line-dark); }}
    .brand-intro {{ max-width: 720px; margin: -1rem 0 4rem auto; line-height: 1.7; opacity: .72; }}
    .brand-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2rem; }}
    .brand-card {{ padding: 2rem; border: 1px solid var(--line-dark); background: rgba(255,255,255,.22); }}
    .brand-wordmark {{
      margin: 0 0 1rem;
      font-size: clamp(2.5rem, 5vw, 5rem);
      font-weight: 800;
      letter-spacing: -.06em;
    }}
    .brand-card p {{ max-width: 580px; min-height: 3.4em; line-height: 1.6; }}
    .brand-links {{ display: flex; gap: 1.5rem; margin: 1.5rem 0; }}
    .brand-links a {{ color: var(--ink) !important; }}
    .brand-media {{
      position: relative;
      display: block;
      aspect-ratio: 16 / 9;
      overflow: hidden;
      background: var(--ink);
    }}
    .brand-media img {{ width: 100%; height: 100%; object-fit: cover; transition: transform .35s ease; }}
    .brand-media--portrait img {{ object-fit: contain; }}
    .brand-media:hover img {{ transform: scale(1.025); }}
    .brand-play {{
      position: absolute;
      right: 1rem;
      bottom: 1rem;
      padding: .75rem 1rem;
      background: var(--paper);
      color: var(--ink);
      font-size: .65rem;
      font-weight: 700;
      letter-spacing: .1em;
      text-transform: uppercase;
    }}
    .video-heading {{ padding: 8rem 7vw 2rem; }}
    div[data-testid="stTabs"] {{ padding: 0 7vw 7rem; }}
    div[data-testid="stTabs"] button {{ letter-spacing: .08em; text-transform: uppercase; }}
    div[data-testid="stVideo"] {{ background: var(--ink); }}
    .video-name {{ margin: .5rem 0 1.7rem; font-family: Georgia, "Times New Roman", serif; font-size: 1.25rem; }}
    .contact-shell {{
      padding: 8rem 7vw 2rem;
      background: var(--ink);
      color: var(--paper);
    }}
    .stApp .contact-title {{ max-width: 900px; margin: 1rem 0 2rem; font-size: clamp(3rem, 6vw, 6.5rem) !important; line-height: .96; }}
    .contact-intro {{ max-width: 700px; color: rgba(242,238,229,.7); line-height: 1.7; }}
    .contact-profile {{ display: flex; align-items: center; gap: 1rem; margin-top: 2.5rem; }}
    .contact-profile img {{ width: 88px; height: 88px; border-radius: 50%; object-fit: cover; }}
    .contact-profile strong {{ display: block; font-family: Georgia, "Times New Roman", serif; font-size: 1.25rem; font-weight: 400; }}
    .contact-profile span {{ color: rgba(242,238,229,.56); font-size: .62rem; letter-spacing: .1em; text-transform: uppercase; }}
    .contact-anchor {{
      height: 1px;
      margin-top: -1px;
      background: var(--ink);
    }}
    div[data-testid="stForm"] {{
      margin: 0;
      padding: 2rem 7vw 8rem;
      border: 0;
      border-radius: 0;
      background: var(--ink);
    }}
    div[data-testid="stForm"] label, div[data-testid="stForm"] p {{ color: var(--paper) !important; }}
    div[data-testid="stForm"] input, div[data-testid="stForm"] textarea {{
      color: var(--paper);
      border-color: var(--line-light);
      background: transparent;
    }}
    div[data-testid="stForm"] button {{
      width: 100%;
      border: 0;
      border-radius: 0;
      background: var(--paper);
      color: var(--ink);
      font-weight: 700;
      letter-spacing: .1em;
      text-transform: uppercase;
    }}
    .site-footer {{
      display: flex;
      justify-content: space-between;
      padding: 2rem 4vw;
      background: var(--paper);
      font-size: .68rem;
      letter-spacing: .1em;
      text-transform: uppercase;
    }}
    @media (max-width: 1120px) and (min-width: 821px) {{
      .creator-grid, .us-creator-grid, .de-creator-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
    }}
    @media (max-width: 820px) {{
      .eyeball-nav {{ min-height: 68px; }}
      .eyeball-links a:not(.nav-cta) {{ display: none; }}
      .hero-copy {{ left: 6vw; right: 6vw; }}
      .hero-actions {{ align-items: flex-start; flex-direction: column; }}
      .section {{ padding: 6rem 6vw; }}
      .about-grid {{ grid-template-columns: 1fr; }}
      .about-detail {{ margin-left: 0; }}
      .section-heading {{ display: block; }}
      .section-title {{ margin-top: 2rem; }}
      .market-intro {{ margin: 2rem 0 3.5rem; }}
      .market-summary {{ grid-template-columns: 1fr auto; gap: .7rem 1rem; padding: 2rem 1.25rem; }}
      .market-summary .section-label {{ grid-column: 1; }}
      .market-summary h3 {{ grid-column: 1; }}
      .market-summary .accordion-icon {{ grid-column: 2; grid-row: 1 / span 2; }}
      .market-content {{ padding: .5rem 1.25rem 4rem; }}
      .creator-grid, .us-creator-grid, .de-creator-grid, .tiktok-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 3rem 1.25rem; }}
      .creator-card h3, .creator-card p {{ min-height: 0; }}
      .brands-section {{ padding: 6rem 6vw; }}
      .brand-intro {{ margin: 2rem 0 3rem; }}
      .brand-grid {{ grid-template-columns: 1fr; }}
      .brand-card p {{ min-height: 0; }}
      .video-heading, .contact-shell {{ padding: 6rem 6vw 2rem; }}
      div[data-testid="stTabs"] {{ padding: 0 6vw 5rem; }}
      div[data-testid="stForm"] {{ padding: 2rem 6vw 6rem; }}
      .site-footer {{ flex-direction: column; gap: 1rem; }}
    }}
    </style>
    <nav class="eyeball-nav">
      <a class="eyeball-brand" href="#top">EYEBALL.</a>
      <div class="eyeball-links">
        <a href="#about">About</a>
        <a href="#creators">Creators</a>
        <a href="#brands">Brands</a>
        <a href="#videos">Videos</a>
        <a class="nav-cta" href="#contact">Connect</a>
      </div>
    </nav>
    <section class="hero" id="top">
      <div class="hero-video">
        <iframe
          src="https://www.youtube-nocookie.com/embed/w4dZOI2VA0s?autoplay=1&mute=1&controls=0&loop=1&playlist=w4dZOI2VA0s&playsinline=1&rel=0&disablekb=1"
          title="Background film by Fabrice"
          allow="autoplay; encrypted-media"
          tabindex="-1">
        </iframe>
      </div>
      <div class="hero-shade"></div>
      <div class="hero-copy">
        <p class="eyebrow">Global New Media + KOL Marketing / Shenzhen</p>
        <h1>See the world<br>in different ways.</h1>
        <div class="hero-actions">
          <a class="light-button" href="#creators">Explore the network</a>
          <a class="text-link" href="#contact">Start a project ↗</a>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="section" id="about">
  <div class="about-grid">
    <div class="section-label">01 &nbsp; About</div>
    <div>
      <h2 class="about-title">Fabrice helps consumer technology brands grow globally through creators, content and culture.</h2>
      <div class="about-detail">
        <p>He is a global new media and KOL marketing leader with experience building international creator programs, managing multicultural content teams and leading brand communications across North America, Europe and Asia.</p>
        <p>His work connects social strategy, product launches, livestreams, community building and data-led ROI optimization. He currently manages a 20+ person social, KOL and creative team and has helped scale creator partnerships, brand visibility and channel revenue for major Chinese consumer technology companies.</p>
        <p>With a master's degree in Software Engineering focused on Big Data, Fabrice combines analytical decision-making with hands-on strengths in photography, filmmaking, public speaking and cross-cultural storytelling.</p>
        <a class="text-link" href="https://www.instagram.com/fabriceraw" target="_blank">Follow @fabriceraw ↗</a>
      </div>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

def creator_cards(creators: list[dict[str, str]], platform: str = "YouTube") -> str:
    audience_label = "subscribers" if platform == "YouTube" else "followers"
    return "".join(
    f"""
    <a class="creator-card" href="{creator['url']}" target="_blank" rel="noopener noreferrer">
      <img src="{image_data(creator['image'])}" alt="{html.escape(creator['name'])} channel profile">
      <h3>{html.escape(creator['name'])}</h3>
      <p>{html.escape(creator['category'])}</p>
      <strong>{creator['audience']}</strong>
      <span>{platform} {audience_label}</span>
    </a>
    """
        for creator in creators
    )


french_creator_cards = creator_cards(FRENCH_CREATORS)
german_creator_cards = creator_cards(GERMAN_CREATORS)
us_creator_cards = creator_cards(US_CREATORS)
tiktok_creator_cards = creator_cards(
    [
        creator
        for regional_creators in TIKTOK_CREATORS.values()
        for creator in regional_creators
    ],
    "TikTok",
)

st.markdown(
    f"""
    <section class="section section-dark" id="creators">
      <div class="section-heading">
        <div class="section-label">02 &nbsp; Creator network</div>
        <h2 class="section-title">Creators in house.</h2>
      </div>
      <details class="market-block">
        <summary class="market-summary">
          <div class="section-label">France</div>
          <h3>French market.</h3>
          <span class="accordion-icon" aria-hidden="true"></span>
        </summary>
        <div class="market-content">
          <div class="market-intro">
            <p>A ready-to-activate French creator bench spanning technology, mobility, craftsmanship, automotive and entertainment. Open a profile to review the channel and find its public business contact details.</p>
            <p class="audience-note">Approximate YouTube audience, June 2026.</p>
          </div>
          <div class="creator-grid">{french_creator_cards}</div>
        </div>
      </details>
      <details class="market-block">
        <summary class="market-summary">
          <div class="section-label">Germany</div>
          <h3>German market.</h3>
          <span class="accordion-icon" aria-hidden="true"></span>
        </summary>
        <div class="market-content">
          <div class="market-intro">
            <p>A broad German YouTube network across outdoor adventure, farming, construction, smart homes, gadgets, solar technology, camping and vanlife.</p>
            <p class="audience-note">Approximate YouTube audience, June 2026.</p>
          </div>
          <div class="creator-grid de-creator-grid">{german_creator_cards}</div>
        </div>
      </details>
      <details class="market-block">
        <summary class="market-summary">
          <div class="section-label">United States</div>
          <h3>US market.</h3>
          <span class="accordion-icon" aria-hidden="true"></span>
        </summary>
        <div class="market-content">
          <div class="market-intro">
            <p>A practical US-market roster covering consumer technology, smart homes, engineering builds, DIY, repairs, product reviews and family-focused rural content.</p>
            <p class="audience-note">Approximate YouTube audience, June 2026.</p>
          </div>
          <div class="creator-grid us-creator-grid">{us_creator_cards}</div>
        </div>
      </details>
      <details class="market-block tiktok-block">
        <summary class="market-summary">
          <div class="section-label">Short-form network</div>
          <h3>TikTok creators.</h3>
          <span class="accordion-icon" aria-hidden="true"></span>
        </summary>
        <div class="market-content">
          <div class="market-intro">
            <p>Fast-moving TikTok talent across North America, Germany and France, covering product discovery, homesteading, life hacks, smart homes and consumer technology.</p>
            <p class="audience-note">Approximate TikTok audience, June 2026.</p>
          </div>
          <div class="creator-grid tiktok-grid">{tiktok_creator_cards}</div>
        </div>
      </details>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <section class="brands-section" id="brands">
      <div class="section-heading">
        <div class="section-label">03 &nbsp; Brand work</div>
        <h2 class="section-title">Built with leading brands.</h2>
      </div>
      <p class="brand-intro">Selected creator-led content produced for global consumer technology brands, from portable energy storytelling to smart-security short-form campaigns.</p>
      <div class="brand-grid">
        <article class="brand-card">
          <h3 class="brand-wordmark">EcoFlow</h3>
          <p>Portable power and clean-energy campaign content created to translate product capability into practical, creator-led stories.</p>
          <div class="brand-links">
            <a class="text-link" href="https://www.ecoflow.com/us" target="_blank">Visit brand ↗</a>
            <a class="text-link" href="https://drive.google.com/file/d/1bgYUxnAf5rwypqKgCXAqyQ1LCdCV9Bfb/view" target="_blank">Open video ↗</a>
          </div>
          <a class="brand-media" href="https://drive.google.com/file/d/1bgYUxnAf5rwypqKgCXAqyQ1LCdCV9Bfb/view" target="_blank" rel="noopener noreferrer" aria-label="Play EcoFlow campaign content">
            <img src="{ecoflow_preview}" alt="Preview frame from EcoFlow campaign content">
            <span class="brand-play">Play preview ↗</span>
          </a>
        </article>
        <article class="brand-card">
          <h3 class="brand-wordmark">Reolink</h3>
          <p>Short-form smart-security content designed to demonstrate real product use, installation value and everyday peace of mind.</p>
          <div class="brand-links">
            <a class="text-link" href="https://reolink.com/" target="_blank">Visit brand ↗</a>
            <a class="text-link" href="https://drive.google.com/file/d/1QvJJYlo0rXcYBoOiL2DwhjijAe6QS8r_/view" target="_blank">Open video ↗</a>
          </div>
          <a class="brand-media brand-media--portrait" href="https://drive.google.com/file/d/1QvJJYlo0rXcYBoOiL2DwhjijAe6QS8r_/view" target="_blank" rel="noopener noreferrer" aria-label="Play Reolink short-form campaign content">
            <img src="{reolink_preview}" alt="Preview frame from Reolink short-form campaign content">
            <span class="brand-play">Play preview ↗</span>
          </a>
        </article>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="video-heading" id="videos">
      <div class="section-heading">
        <div class="section-label">04 &nbsp; Video library</div>
        <h2 class="section-title">Stories in motion.</h2>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

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
                st.markdown(f'<p class="video-name">{html.escape(label)}</p>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="contact-anchor" id="contact"></div>
    <section class="contact-shell">
      <div class="section-label">05 &nbsp; Contact</div>
      <p class="eyebrow" style="margin-top:4rem">Build global attention</p>
      <h2 class="contact-title">Let's turn strategy into influence and growth.</h2>
      <p class="contact-intro">Get in touch about global social media strategy, KOL and creator partnerships, product launches, content production, livestreams or international brand growth.</p>
      <div class="contact-profile">
        <img src="{portrait}" alt="Portrait of Fabrice Klohoun">
        <div>
          <strong>Fabrice Klohoun</strong>
          <span>Global New Media + KOL Marketing<br>Shenzhen, China</span>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.form("project_enquiry", clear_on_submit=True):
    first, second = st.columns(2)
    name = first.text_input("Name")
    email = second.text_input("Email")
    phone = first.text_input("Phone")
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
                f'<a href="mailto:klohounfabrice@gmail.com?subject={mail_subject}">'
                "Email Fabrice directly</a>",
                unsafe_allow_html=True,
            )
        else:
            try:
                send_enquiry(name, email, phone, subject, message)
                st.success("Thank you. Your enquiry has been sent.")
            except (OSError, smtplib.SMTPException) as exc:
                st.error(f"The message could not be sent. Please email klohounfabrice@gmail.com. ({exc})")

st.markdown(
    """
<div class="site-footer">
  <strong>EYEBALL.</strong>
  <span>Global new media + KOL marketing</span>
  <span>© 2026 Eyeball</span>
</div>
""",
    unsafe_allow_html=True,
)
