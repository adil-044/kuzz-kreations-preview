#!/usr/bin/env python3
"""Generate static HTML — Wendy copy verbatim + animation hooks."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data.json").read_text())
COPY = json.loads((ROOT / "copy.json").read_text())

PHONE = "519-209-8803"
PHONE_TEL = "+15192098803"
ADDRESS = "204 Dalhousie St, Brantford, ON N3S 3T7"
MAPS = "https://www.google.com/maps/search/?api=1&query=Kuzz+Kreations+204+Dalhousie+St+Brantford"
FACEBOOK = "https://www.facebook.com/profile.php?id=100078342901677"
INSTAGRAM = "https://www.instagram.com/kuzzkreationshairstyles/"
UPTISEMENT = "https://uptisement.com"
GUEST_CARD = "https://docs.google.com/forms/d/e/1FAIpQLSe8gEEIcNVgdPCEuFpiiT0xWk4HIZdGW_JE8Sim-rZdKBl1oA/viewform"
RATING = DATA["rating"]
REVIEWS = DATA["reviewsCount"]
HERO = DATA["images"]["hero"]
HERO_SRC = f"./{HERO}?v=20260831-wendy"
GALLERY = DATA["images"].get("gallery") or DATA["images"]["ig"] + DATA["images"]["google"]
STYLE_RAIL_IMGS = {
    "locs": "images/ig-DbRdQS7OwNK.jpg",
    "braids": "images/google-5.jpg",
    "extensions": "images/google-1.jpg",
    "crochet": "images/google-2.jpg",
}
# Locs-first scroll showcase — Wendy IG work only (no stock)
LOCS_WORK = [
    img
    for img in (DATA["images"].get("gallery") or [])
    if "loc" in (img.get("caption") or "").lower()
    or img["file"].startswith("images/ig-")
][:5] or [
    {"file": "images/ig-DbRdQS7OwNK.jpg", "caption": "Microlocs transformation"},
    {"file": "images/ig-DTDxJLbkQXk.jpg", "caption": "Healthy locs"},
    {"file": "images/ig-C4ORxdnRf4W.jpg", "caption": "Bridal locs"},
    {"file": "images/ig-CiN0A2cp4j3.jpg", "caption": "Mahogany loc updo"},
    {"file": "images/ig-C5E7jYWRrQJ.jpg", "caption": "Herbal oil steam treatment"},
]
CANONICAL_ORIGIN = "https://kuzzkreations.ca"
GS = COPY["googleSites"]
WENDY = COPY["wendy"]
TEAM = COPY["team"]

NAV = [
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
    ("team.html", "Team"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
    ("book.html", "Book"),
]

SCRIPTS = """
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
  <script src="./site.js"></script>
  <script src="./animations.js"></script>"""


def e(s: str) -> str:
    return html.escape(s or "")


def json_ld() -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "HairSalon",
        "name": "Kuzz Kreations",
        "description": "Natural locs, braids, extensions and salon services in Brantford.",
        "url": CANONICAL_ORIGIN + "/",
        "telephone": PHONE_TEL,
        "image": CANONICAL_ORIGIN + "/images/hero-ig-DTDxJLbkQXk.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "204 Dalhousie St",
            "addressLocality": "Brantford",
            "addressRegion": "ON",
            "postalCode": "N3S 3T7",
            "addressCountry": "CA",
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(RATING),
            "reviewCount": str(REVIEWS),
        },
        "sameAs": [INSTAGRAM, FACEBOOK],
    }
    return (
        '  <script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=True)
        + "\n  </script>"
    )


def head(title: str, desc: str, path: str = "/", extra_script: str = "") -> str:
    url = CANONICAL_ORIGIN + (path if path.startswith("/") else "/" + path)
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <meta name="theme-color" content="#1C0920" />
  <link rel="canonical" href="{e(url)}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{e(url)}" />
  <meta property="og:image" content="{CANONICAL_ORIGIN}/images/hero-ig-DTDxJLbkQXk.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;0,6..96,600;1,6..96,500;1,6..96,600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="./styles.css" />
{json_ld()}
</head>
<body class="has-preview">"""


def preview_bar() -> str:
    return """  <div class="preview-bar" role="status">Preview for Wendy — her copy &amp; photos · tell us what to change before HostGator delivery</div>"""


def nav(current: str) -> str:
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        cls = ' class="btn btn-primary"' if label == "Book" else ""
        items.append(f'<li><a href="./{href}"{cls}{cur}>{label}</a></li>')
    drawer = "\n".join(f'<li><a href="./{h}">{l}</a></li>' for h, l in [("", "Home"), *NAV])
    return f"""  <a class="skip" href="#main">Skip to content</a>
  <header class="nav">
    <a class="logo" href="./">Kuzz <em>Kreations</em></a>
    <nav aria-label="Primary">
      <ul class="nav-desktop">
        {''.join(items)}
      </ul>
    </nav>
    <a class="btn btn-primary nav-book-m" href="./book.html">Book</a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Open menu">☰</button>
  </header>
  <div class="nav-drawer" data-nav-drawer aria-hidden="true">
    <div class="drawer-panel">
      <button class="btn btn-ghost" type="button" data-nav-close>Close</button>
      <ul>
        {drawer}
        <li><a href="tel:{PHONE_TEL}">Call {PHONE}</a></li>
      </ul>
    </div>
  </div>"""


def social_icons() -> str:
    return f"""<div class="social-row" aria-label="Social profiles">
          <a class="social-btn" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" aria-label="Instagram @kuzzkreationshairstyles">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm10 2H7a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm-5 3.5A4.5 4.5 0 1 1 7.5 13 4.5 4.5 0 0 1 12 8.5zm0 2A2.5 2.5 0 1 0 14.5 13 2.5 2.5 0 0 0 12 10.5zM17.8 6.4a1 1 0 1 1-1 1 1 1 0 0 1 1-1z"/></svg>
          </a>
          <a class="social-btn" href="{FACEBOOK}" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 10.5V8.2c0-.8.2-1.2 1.1-1.2H16V4.6h-2.4C10.8 4.6 9 6.2 9 8.8v1.7H7v3.1h2v7.6h4v-7.6h2.7l.3-3.1z"/></svg>
          </a>
          <a class="social-btn" href="{MAPS}" target="_blank" rel="noopener noreferrer" aria-label="Google Maps">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 14.5 9 2.5 2.5 0 0 1 12 11.5z"/></svg>
          </a>
        </div>"""


def footer(extra: str = "") -> str:
    return f"""  <footer class="site">
    <div class="wrap foot-main">
      <div class="foot-brand">
        <p class="brand-line">Kuzz <span>Kreations</span></p>
        <p class="foot-tag">Hair · Beauty · Supplies · Brantford</p>
        <p><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
        <p><a href="{MAPS}" target="_blank" rel="noopener noreferrer">{e(ADDRESS)}</a></p>
      </div>
      <div class="foot-col">
        <p class="foot-heading">Explore</p>
        <nav class="foot-links" aria-label="Footer">
          <a href="./services.html">Services</a>
          <a href="./gallery.html">Gallery</a>
          <a href="./team.html">Team</a>
          <a href="./about.html">About</a>
          <a href="./contact.html">Contact</a>
          <a href="./book.html">Book</a>
        </nav>
      </div>
      <div class="foot-col">
        <p class="foot-heading">Hours</p>
        <ul class="foot-hours">
          <li>Mon–Wed · 9:00 AM – 7:30 PM</li>
          <li>Thu–Fri · 9:00 AM – 7:00 PM</li>
          <li>Sat · 9:00 AM – 5:00 PM</li>
          <li>Sun · Closed</li>
        </ul>
      </div>
      <div class="foot-col">
        <p class="foot-heading">Follow us</p>
        {social_icons()}
        <p class="foot-handle"><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@kuzzkreationshairstyles</a></p>
      </div>
    </div>
    <div class="wrap foot-bottom">
      <p>© <span id="y"></span> Kuzz Kreations · {RATING}★ · {REVIEWS} Google reviews</p>
      <a class="foot-watermark" href="{UPTISEMENT}" target="_blank" rel="noopener noreferrer">
        <img src="./images/uptisement-mark.png" alt="" width="18" height="18" loading="lazy" />
        <span>Website by <strong>Uptisement</strong></span>
      </a>
    </div>
  </footer>
  <div class="mobile-bar" aria-label="Quick actions">
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call</a>
    <a class="btn btn-primary" href="./book.html">Book</a>
  </div>
{SCRIPTS}
{extra}"""


def reviews_block() -> str:
    quotes = []
    for r in DATA["reviews"]:
        if not r.get("text"):
            continue
        text = r["text"].strip()
        if len(text) > 280:
            text = text[:277] + "…"
        quotes.append(
            f'<blockquote class="quote reveal-child"><p>"{e(text)}"</p><footer>— {e(r["name"])} · Google</footer></blockquote>'
        )
    return f"""    <section class="section section-alt" id="reviews">
      <div class="wrap" data-reveal>
        <p class="kicker">Google reviews</p>
        <div class="rating-row">
          <div class="score">{RATING}</div>
          <p class="lead" style="margin:0">{RATING} out of 5 from {REVIEWS} Google reviews · {e(ADDRESS)}</p>
        </div>
        <div class="quotes" data-stagger>
          {''.join(quotes)}
        </div>
      </div>
    </section>"""


def service_cards(featured_first: bool = True) -> str:
    svcs = sorted(COPY["services"], key=lambda s: (0 if s.get("featured") else 1))
    cards = []
    for s in svcs:
        cls = "card reveal-child locs-feature" if s.get("featured") else "card reveal-child"
        link = "./services.html#locs" if s["id"] == "locs" else f'./services.html#{s["id"]}'
        cards.append(
            f"""<article class="{cls}">
            <h3>{e(s["title"])}</h3>
            <p>{e(s["copy"])}</p>
            <a class="card-link" href="{link}">Learn more →</a>
          </article>"""
        )
    return "\n          ".join(cards)


def style_rail() -> str:
    locs_svcs = [s for s in COPY["services"] if s["id"] in ("locs", "braids", "extensions", "crochet")]
    cards = []
    for s in locs_svcs:
        img = STYLE_RAIL_IMGS.get(s["id"], HERO)
        cards.append(
            f"""<a class="style-card reveal-child" href="./services.html#{s['id']}">
          <img src="./{img}" alt="{e(s['title'])}" loading="lazy" width="300" height="375" />
          <div class="body"><h3>{e(s['title'])}</h3><p>{e(s['copy'])}</p></div>
        </a>"""
        )
    return "\n          ".join(cards)


def locs_showcase() -> str:
    """Scroll-driven locs work stage — GSAP ScrollTrigger, same stack."""
    slides = []
    caps = []
    dots = []
    marquee = []
    for i, img in enumerate(LOCS_WORK):
        cap = (img.get("caption") or "Natural locs").split("\n")[0][:80]
        active = " is-active" if i == 0 else ""
        slides.append(
            f"""<figure class="locs-slide{active}" data-locs-slide="{i}">
            <div class="locs-matte">
              <img src="./{img['file']}" alt="{e(cap)}" width="1200" height="1200" {'fetchpriority="high"' if i == 0 else 'loading="lazy"'} />
            </div>
          </figure>"""
        )
        caps.append(
            f"""<div class="locs-cap-row{active}" data-locs-cap="{i}">
            <span class="locs-step">0{i + 1}</span>
            <span class="locs-cap">{e(cap)}</span>
          </div>"""
        )
        dots.append(f'<button type="button" class="locs-dot{active}" data-locs-dot="{i}" aria-label="Show work {i + 1}"></button>')
        marquee.append(
            f'<div class="work-chip"><span class="work-chip-matte"><img src="./{img["file"]}" alt="" loading="lazy" width="160" height="160" /></span><span>{e(cap)}</span></div>'
        )
    return f"""
    <section class="locs-stage" id="locs-work" aria-label="Natural locs work showcase" data-locs-stage>
      <div class="locs-stage-pin">
        <div class="wrap locs-stage-grid">
          <div class="locs-stage-copy" data-reveal>
            <p class="kicker">Signature craft</p>
            <h2 class="title">Natural Locs, in motion</h2>
            <p class="lead">{e(WENDY["naturalLocs"])}</p>
            <p class="locs-hint">Scroll to walk through real client work</p>
            <div class="locs-dots" role="tablist" aria-label="Locs work slides">{"".join(dots)}</div>
            <p class="locs-cta-row">
              <a class="btn btn-primary" href="./gallery.html">Full gallery</a>
              <a class="btn btn-ghost" href="./book.html">Book locs</a>
            </p>
          </div>
          <div class="locs-stage-shell">
            <div class="locs-stage-frame" data-locs-frame>
              {"".join(slides)}
            </div>
            <div class="locs-captions" aria-live="polite">
              {"".join(caps)}
            </div>
            <div class="locs-progress" aria-hidden="true"><span data-locs-progress></span></div>
          </div>
        </div>
      </div>
    </section>
    <div class="work-marquee trust-strip" aria-hidden="true" data-work-marquee>
      <div class="work-marquee-track">
        {"".join(marquee)}
        {"".join(marquee)}
      </div>
    </div>"""


def index() -> str:
    return (
        head(
            "Kuzz Kreations | Look & Feel Beautiful — Brantford",
            f"Natural locs, braids, extensions & salon services in Brantford. {RATING}★ Google. 204 Dalhousie St.",
            "/",
        )
        + preview_bar()
        + nav("")
        + f"""
  <main id="main">
    <section class="hero grain" data-hero aria-label="Hero">
      <div class="hero-media" aria-hidden="true">
        <img src="{HERO_SRC}" alt="Beautiful healthy locs — Kuzz Kreations" width="2400" height="1500" fetchpriority="high" />
      </div>
      <div class="wrap hero-copy">
        <p class="pill" data-hero-item>{e(GS["heroTitle"])}</p>
        <p class="hero-brand" data-hero-item>Kuzz <span>Kreations</span></p>
        <h1 data-hero-item>{e(GS["heroSub"])}</h1>
        <p class="hero-lead" data-hero-item><em>{e(GS["stylistNote"])}</em></p>
        <div class="hero-actions" data-hero-item>
          <a class="btn btn-primary" href="./book.html">Book appointment</a>
          <a class="btn btn-ghost" href="./gallery.html">See our work</a>
        </div>
        <div class="hero-stats" data-hero-item>
          <div><strong>{RATING}★</strong><span>Google rating</span></div>
          <div><strong>{REVIEWS}</strong><span>Google reviews</span></div>
          <div><strong>204</strong><span>Dalhousie St</span></div>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap" data-reveal>
        <p class="kicker">{e(COPY["home"]["treatmentsHeading"])}</p>
        <h2 class="title">{e(GS["fullServiceHeading"])}</h2>
        <p class="lead">{e(WENDY["fullServiceExperience"])}</p>
      </div>
    </section>
"""
        + locs_showcase()
        + f"""
    <section class="section">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">Services rail</p>
          <h2 class="title">Locs, braids &amp; more</h2>
          <p class="lead">Swipe through signature services — locs lead the way.</p>
        </div>
        <div class="style-rail" aria-label="Locs and salon services" data-stagger>
          {style_rail()}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap split">
        <div class="parallax-wrap" data-parallax>
          <img src="./images/ig-DbRdQS7OwNK.jpg" alt="Microlocs at Kuzz Kreations" loading="lazy" width="1200" height="900" />
        </div>
        <div class="copy" data-reveal>
          <p class="kicker">About the salon</p>
          <h2 class="title">{e(GS["heroTitle"])}</h2>
          <p>{e(GS["about1"])}</p>
          <p style="margin-top:1rem">{e(GS["about2"])}</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">Salon service</p>
          <h2 class="title">{e(COPY["home"]["fullServiceHeading"])}</h2>
          <p class="lead" style="margin-bottom:0">Browse our services below.</p>
        </div>
        <div class="card-grid" data-stagger>
          {service_cards()}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap split">
        <div class="copy" data-reveal>
          <p class="kicker">Hair care products</p>
          <p>{e(COPY["home"]["productsIntro"])}</p>
          <h3 class="title" style="font-size:1.75rem;margin-top:1.5rem">{e(COPY["products"]["treatmentsTitle"])}</h3>
          <p>{e(COPY["products"]["treatments"])}</p>
          <h3 class="title" style="font-size:1.75rem;margin-top:1.25rem">{e(COPY["products"]["productsTitle"])}</h3>
          <p>{e(COPY["products"]["products"])}</p>
        </div>
        <div class="parallax-wrap" data-parallax>
          <img src="./images/ig-C5E7jYWRrQJ.jpg" alt="Herbal oil treatment for locs" loading="lazy" />
        </div>
      </div>
    </section>
"""
        + reviews_block()
        + f"""
    <section class="cta-band">
      <div class="wrap" data-reveal>
        <p class="kicker">Book an appointment</p>
        <h2 class="title">We will be happy to assist you</h2>
        <p class="lead">{e(COPY["home"]["bookBlock"])}</p>
        <p style="margin-top:1.25rem">
          <a class="btn btn-primary" href="./book.html">Book now</a>
          <a class="btn btn-ghost" href="{GUEST_CARD}" target="_blank" rel="noopener">Guest card</a>
        </p>
      </div>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def services() -> str:
    locs = COPY["locs"]
    loc_sections = []
    for sec in locs["sections"]:
        loc_sections.append(
            f'<article class="card reveal-child locs-feature"><h3>{e(sec["title"])}</h3><p>{e(sec["copy"])}</p></article>'
        )
    other = [s for s in COPY["services"] if s["id"] != "locs"]
    other_cards = []
    for s in other:
        other_cards.append(
            f'<article class="card reveal-child" id="{s["id"]}"><h3>{e(s["title"])}</h3><p>{e(s["copy"])}</p></article>'
        )
    benefit_cards = []
    for b in locs["benefits"]:
        benefit_cards.append(f'<article class="card reveal-child"><h3>{e(b["title"])}</h3><p>{e(b["copy"])}</p></article>')

    return (
        head(
            "Services | Dreadlocks, Braids, Extensions — Kuzz Kreations",
            "Natural locs, dreadlocks, braids, weave extensions, crochet, Olaplex & color in Brantford.",
            "/services.html",
        )
        + preview_bar()
        + nav("services.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Salon service</p>
        <h1 class="title">{e(locs["pageTitle"])}</h1>
        <p class="lead">{e(WENDY["fullServiceExperience"])}</p>
      </div>
    </header>

    <section class="section" id="locs">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">Natural locs</p>
          <h2 class="title">Natural Locs</h2>
          <p class="lead">{e(WENDY["naturalLocs"])}</p>
        </div>
        <div class="card-grid" data-stagger>
          {chr(10).join(loc_sections)}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap split">
        <div class="parallax-wrap" data-parallax>
          <img src="./images/ig-C4ORxdnRf4W.jpg" alt="Locs styles" loading="lazy" />
        </div>
        <div class="copy" data-reveal>
          <p class="kicker">{e(locs["journeyTitle"])}</p>
          <h2 class="title">{e(locs["benefitsTitle"])}</h2>
          <p>{e(locs["journey"])}</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">{e(locs["benefitsTitle"])}</p>
        </div>
        <div class="card-grid" data-stagger>
          {chr(10).join(benefit_cards)}
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">More services</p>
          <h2 class="title">{e(COPY["home"]["fullServiceHeading"])}</h2>
        </div>
        <div class="card-grid" data-stagger>
          {chr(10).join(other_cards)}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="card-grid" data-stagger>
          <article class="card reveal-child"><h3>Disclaimer</h3><p>{e(locs["disclaimer"])}</p></article>
          <article class="card reveal-child"><h3>Deposits</h3><p>{e(locs["deposits"])}</p></article>
          <article class="card reveal-child"><h3>Consultation</h3><p>{e(locs["consult"])}</p></article>
        </div>
        <p style="margin-top:1.75rem;text-align:center" data-reveal>
          <a class="btn btn-primary" href="./book.html">Book a service</a>
        </p>
      </div>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def gallery() -> str:
    figures = []
    for img in GALLERY:
        cap = (img.get("caption") or "Kuzz Kreations salon work").split("\n")[0][:90]
        label = "Instagram" if img.get("source") == "instagram" else "Google"
        figures.append(
            f'<figure class="gallery-tile reveal-child"><img src="./{img["file"]}" alt="{e(cap)}" loading="lazy" /><figcaption><span class="gallery-src">{label}</span><span class="gallery-cap">{e(cap)}</span></figcaption></figure>'
        )

    return (
        head(
            "Gallery | Kuzz Kreations Brantford",
            "Real locs, braids and salon work from Instagram and Google.",
            "/gallery.html",
        )
        + preview_bar()
        + nav("gallery.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Gallery</p>
        <h1 class="title">See what we've done</h1>
        <p class="lead">Be a part of our social presence! See what we've done and what we're doing next on social Media — <a href="{INSTAGRAM}" target="_blank" rel="noopener" style="color:var(--coral)">@kuzzkreationshairstyles</a></p>
      </div>
    </header>
    <section class="section">
      <div class="wrap masonry" data-stagger data-gallery>
        {''.join(figures)}
      </div>
      <p class="wrap" style="margin-top:1.5rem;text-align:center" data-reveal>
        <a class="btn btn-primary" href="./book.html">Book your style</a>
      </p>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def about() -> str:
    return (
        head(
            "About | Kuzz Kreations Hair & Beauty Salon",
            GS["about1"][:120],
            "/about.html",
        )
        + preview_bar()
        + nav("about.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">{e(GS["fullServiceHeading"])}</p>
        <h1 class="title">{e(GS["heroTitle"])}</h1>
        <p class="lead">{e(WENDY["fullServiceExperience"])}</p>
      </div>
    </header>

    <section class="section">
      <div class="wrap split">
        <div class="parallax-wrap" data-parallax>
          <img src="./images/google-1.jpg" alt="Burgundy loc updo at Kuzz Kreations" loading="lazy" />
        </div>
        <div class="copy" data-reveal>
          <p class="kicker">Our goal</p>
          <h2 class="title">{e(GS["heroSub"])}</h2>
          <p>{e(GS["about2"])}</p>
          <p style="margin-top:1rem">{e(COPY["home"]["salonBlock"])}</p>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap" data-reveal>
        <p class="kicker">Google listing</p>
        <p class="lead">{e(COPY["googleOwner"])}</p>
      </div>
      <div class="wrap card-grid" data-stagger style="margin-top:1.5rem">
        <article class="card reveal-child"><h3>{e(COPY["products"]["treatmentsTitle"])}</h3><p>{e(COPY["products"]["treatments"])}</p></article>
        <article class="card reveal-child"><h3>{e(COPY["products"]["productsTitle"])}</h3><p>{e(COPY["products"]["products"])}</p></article>
        <article class="card reveal-child"><h3>Hair care</h3><p>{e(COPY["home"]["productsIntro"])}</p></article>
      </div>
      <p class="wrap" style="margin-top:1.75rem;text-align:center" data-reveal>
        <a class="btn btn-primary" href="./book.html">Book with us</a>
        <a class="btn btn-ghost" href="{GUEST_CARD}" target="_blank" rel="noopener">Guest card</a>
      </p>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def contact() -> str:
    return (
        head("Contact | Kuzz Kreations Brantford", f"204 Dalhousie St · {PHONE}", "/contact.html")
        + preview_bar()
        + nav("contact.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Contact</p>
        <h1 class="title">{e(GS["stylistNote"])}</h1>
        <p class="lead">{e(COPY["home"]["bookBlock"])}</p>
        <p style="margin-top:1rem"><a class="btn btn-soft" href="./team.html">Meet our stylists</a></p>
      </div>
    </header>
    <section class="section">
      <div class="wrap visit-grid" data-stagger>
        <dl class="info-card reveal-child">
          <dt>Address</dt>
          <dd>{e(ADDRESS)}</dd>
          <dt>Phone</dt>
          <dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
          <dt>Hours</dt>
          <dd>Mon–Wed 9:00 AM – 7:30 PM<br>Thu–Fri 9:00 AM – 7:00 PM<br>Sat 9:00 AM – 5:00 PM<br>Sun closed</dd>
        </dl>
        <dl class="info-card reveal-child">
          <dt>Social</dt>
          <dd><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @kuzzkreationshairstyles</a></dd>
          <dd><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></dd>
          <dt>Directions</dt>
          <dd><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></dd>
          <dt>Guest card</dt>
          <dd><a href="{GUEST_CARD}" target="_blank" rel="noopener">Exclusive offers &amp; discounts</a></dd>
        </dl>
      </div>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def specialty_tags(specialties: list) -> str:
    return " ".join(f'<span class="tag">{e(s)}</span>' for s in specialties)


def stylist_avatar(member: dict, large: bool = False) -> str:
    cls = "stylist-avatar stylist-avatar-lg" if large else "stylist-avatar"
    photo = member.get("photo")
    if photo:
        return f'<img class="{cls}" src="./{photo}" alt="{e(member["name"])}" loading="lazy" />'
    return f'<div class="{cls}" aria-hidden="true">{e(member.get("initials", "?"))}</div>'


def team_cards() -> str:
    cards = []
    for member in TEAM["members"]:
        slug = member["id"]
        badge = (
            '<span class="pill pill-soft">Profile coming soon</span>'
            if member.get("placeholder")
            else ""
        )
        cards.append(
            f"""<article class="stylist-card reveal-child">
          <a class="stylist-card-link" href="./{slug}.html" aria-label="View {e(member['name'])} profile">
            {stylist_avatar(member)}
            <div class="stylist-card-body">
              {badge}
              <h2>{e(member["name"])}</h2>
              <p class="stylist-role">{e(member["role"])}</p>
              <div class="tag-row">{specialty_tags(member["specialties"])}</div>
              <span class="card-link">View profile →</span>
            </div>
          </a>
          <a class="btn btn-soft stylist-book" href="./book.html?stylist={slug}">Book with {e(member["name"])}</a>
        </article>"""
        )
    return "\n        ".join(cards)


def team() -> str:
    return (
        head(
            "Our Team | Kuzz Kreations Brantford",
            "Meet the stylists at Kuzz Kreations — natural locs, braids, extensions and salon services in Brantford.",
            "/team.html",
        )
        + preview_bar()
        + nav("team.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Our stylists</p>
        <h1 class="title">{e(TEAM["pageTitle"])}</h1>
        <p class="lead">{e(TEAM["intro"])}</p>
        <p class="note team-note">{e(TEAM["placeholderNote"])}</p>
      </div>
    </header>
    <section class="section">
      <div class="wrap team-grid" data-stagger>
        {team_cards()}
      </div>
      <p class="wrap" style="margin-top:2rem;text-align:center" data-reveal>
        <a class="btn btn-primary" href="./book.html">Book any stylist</a>
        <a class="btn btn-ghost" href="./contact.html">Questions? Contact us</a>
      </p>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def stylist_profile(member: dict) -> str:
    slug = member["id"]
    others = [m for m in TEAM["members"] if m["id"] != slug]
    other_links = "".join(
        f'<a class="stylist-mini" href="./{m["id"]}.html">{stylist_avatar(m)}<span>{e(m["name"])}</span></a>'
        for m in others[:3]
    )
    badge = (
        '<p class="pill pill-soft" style="display:inline-block;margin-bottom:1rem">Profile coming soon</p>'
        if member.get("placeholder")
        else ""
    )
    return (
        head(
            f"{member['name']} | Kuzz Kreations Team",
            f"Book {member['name']} at Kuzz Kreations Brantford — {', '.join(member['specialties'][:2])}.",
            f"/{member['id']}.html",
        )
        + preview_bar()
        + nav("team.html")
        + f"""
  <main id="main">
    <header class="page-hero stylist-hero">
      <div class="wrap stylist-hero-grid" data-reveal>
        {stylist_avatar(member, large=True)}
        <div>
          {badge}
          <p class="kicker">Kuzz Kreations stylist</p>
          <h1 class="title">{e(member["name"])}</h1>
          <p class="stylist-role">{e(member["role"])}</p>
          <div class="tag-row" style="margin-top:1rem">{specialty_tags(member["specialties"])}</div>
          <div class="hero-actions" style="margin-top:1.5rem">
            <a class="btn btn-primary" href="./book.html?stylist={slug}">Book with {e(member["name"])}</a>
            <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call salon</a>
          </div>
        </div>
      </div>
    </header>
    <section class="section section-alt">
      <div class="wrap split">
        <div class="copy" data-reveal>
          <p class="kicker">About</p>
          <p>{e(member["bio"])}</p>
          <p style="margin-top:1rem;color:var(--muted)">{e(COPY["locs"]["consult"])}</p>
        </div>
        <div class="card reveal-child">
          <h3>Book this stylist</h3>
          <p>Send a text with your service, date, and preferred time. Mention <strong>{e(member["name"])}</strong> so we match you with the right chair.</p>
          <p style="margin-top:1rem"><a class="btn btn-primary" href="./book.html?stylist={slug}">Request appointment</a></p>
          <p class="note" style="margin-top:1rem">{e(COPY["locs"]["deposits"])}</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="wrap" data-reveal>
        <p class="kicker">More stylists</p>
        <h2 class="title" style="font-size:1.75rem">Meet the rest of the team</h2>
        <div class="stylist-mini-row" style="margin-top:1.25rem">
          {other_links}
          <a class="btn btn-ghost" href="./team.html">View all team</a>
        </div>
      </div>
    </section>
  </main>
"""
        + footer()
        + "\n</body>\n</html>\n"
    )


def book() -> str:
    return (
        head("Book | Kuzz Kreations Brantford", COPY["home"]["bookBlock"][:140], "/book.html")
        + preview_bar()
        + nav("book.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Book an appointment</p>
        <h1 class="title">Schedule your visit</h1>
        <p class="lead">{e(COPY["home"]["bookBlock"])}</p>
      </div>
    </header>
    <div class="wrap book-layout">
      <div class="book-panel" data-reveal>
        <h2>Request by text</h2>
        <p class="note">{e(COPY["locs"]["deposits"])}</p>
        <form class="form" id="book-form" novalidate>
          <div class="field"><label for="name">Full name</label><input id="name" name="name" autocomplete="name" required placeholder="Your name" /></div>
          <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" required placeholder="Mobile number" /></div>
          <div class="field"><label for="email">Email (optional)</label><input id="email" name="email" type="email" autocomplete="email" placeholder="you@email.com" /></div>
          <div class="field">
            <label for="stylist">Preferred stylist</label>
            <select id="stylist" name="stylist">
              <option value="">No preference — first available</option>
              {''.join(f'<option value="{e(m["id"])}">{e(m["name"])}</option>' for m in TEAM["members"])}
            </select>
          </div>
          <div class="field">
            <label for="service">Service</label>
            <select id="service" name="service" required>
              <option value="">Select a service</option>
              <option>Natural locs — starter / install</option>
              <option>Natural locs — retighten / maintain</option>
              <option>Micro locs</option>
              <option>DreadLocks / loc styles</option>
              <option>Hot oil / herbal steam treatment</option>
              <option>Braids extensions</option>
              <option>Men's braids</option>
              <option>Crochet braids</option>
              <option>Hair extensions / weave</option>
              <option>Hair cut &amp; color</option>
              <option>Olaplex treatment</option>
              <option>Perm relaxer</option>
              <option>Consultation</option>
            </select>
          </div>
          <div class="field"><label for="date">Preferred date</label><input id="date" name="date" type="date" required /></div>
          <div class="field">
            <label for="time">Preferred time</label>
            <select id="time" name="time" required>
              <option value="">Select a window</option>
              <option>Morning (9–12)</option>
              <option>Afternoon (12–4)</option>
              <option>Evening (4–close)</option>
              <option>Saturday anytime</option>
            </select>
          </div>
          <div class="field"><label for="notes">Notes</label><textarea id="notes" name="notes" placeholder="Send pictures in advance for a more exact cost…"></textarea></div>
          <div class="form-actions">
            <button class="btn btn-primary" type="submit">Send booking text</button>
            <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a>
          </div>
          <p class="form-status" id="status" role="status" aria-live="polite"></p>
        </form>
      </div>
      <aside class="book-panel" data-reveal data-reveal-delay="0.08">
        <h2>Salon policy</h2>
        <p class="note">{e(COPY["locs"]["disclaimer"])}</p>
        <p style="margin-top:1rem;color:var(--muted)">{e(COPY["locs"]["consult"])}</p>
        <p style="margin-top:1.25rem"><a class="btn btn-soft" href="{GUEST_CARD}" target="_blank" rel="noopener">Guest card</a></p>
        <ul style="margin:1.25rem 0 0;padding-left:1.1rem;color:var(--muted);font-size:0.92rem">
          <li>{e(ADDRESS)}</li>
          <li>Mon–Wed 9–7:30 · Thu–Fri 9–7 · Sat 9–5</li>
        </ul>
      </aside>
    </div>
  </main>
"""
        + footer("\n  <script src=\"./book.js\"></script>")
        + "\n</body>\n</html>\n"
    )


if __name__ == "__main__":
    pages = {
        "index.html": index(),
        "services.html": services(),
        "gallery.html": gallery(),
        "team.html": team(),
        "about.html": about(),
        "contact.html": contact(),
        "book.html": book(),
    }
    for member in TEAM["members"]:
        pages[f"{member['id']}.html"] = stylist_profile(member)
    for name, content in pages.items():
        (ROOT / name).write_text(content)
    print("Wrote", ", ".join(pages))
