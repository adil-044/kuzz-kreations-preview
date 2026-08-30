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
GUEST_CARD = "https://docs.google.com/forms/d/e/1FAIpQLSe8gEEIcNVgdPCEuFpiiT0xWk4HIZdGW_JE8Sim-rZdKBl1oA/viewform"
RATING = DATA["rating"]
REVIEWS = DATA["reviewsCount"]
HERO = DATA["images"]["hero"]
GS = COPY["googleSites"]

NAV = [
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
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


def head(title: str, desc: str, extra_script: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <meta name="theme-color" content="#1C0920" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;0,6..96,600;1,6..96,500;1,6..96,600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="./styles.css" />
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


def footer(extra: str = "") -> str:
    return f"""  <footer class="site">
    <div class="wrap">
      <div>
        <p class="brand-line">Kuzz Kreations</p>
        <p>{e(ADDRESS)}</p>
        <p><a href="tel:{PHONE_TEL}">{PHONE}</a></p>
      </div>
      <div class="foot-grid">
        <a href="./services.html">Services</a>
        <a href="./gallery.html">Gallery</a>
        <a href="./about.html">About</a>
        <a href="./book.html">Book</a>
        <a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a>
      </div>
      <div class="foot-bottom">
        <span>© <span id="y"></span> Kuzz Kreations</span>
        <span>{RATING}★ · {REVIEWS} Google reviews</span>
      </div>
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
    imgs = DATA["images"]["ig"]
    loc_imgs = [i for i in imgs if "loc" in i.get("caption", "").lower() or "dread" in i.get("caption", "").lower()]
    cards = []
    for i, s in enumerate(locs_svcs):
        img = loc_imgs[i]["file"] if i < len(loc_imgs) else HERO
        cards.append(
            f"""<a class="style-card reveal-child" href="./services.html#{s['id']}">
          <img src="./{img}" alt="{e(s['title'])}" loading="lazy" width="300" height="375" />
          <div class="body"><h3>{e(s['title'])}</h3><p>{e(s['copy'])}</p></div>
        </a>"""
        )
    return "\n          ".join(cards)


def index() -> str:
    return (
        head(
            "Kuzz Kreations | Look & Feel Beautiful — Brantford",
            f"Natural locs, braids, extensions & salon services in Brantford. {RATING}★ Google. 204 Dalhousie St.",
        )
        + preview_bar()
        + nav("")
        + f"""
  <main id="main">
    <section class="hero grain" data-hero aria-label="Hero">
      <div class="hero-media" aria-hidden="true">
        <img src="./{HERO}" alt="" width="2400" height="1500" fetchpriority="high" />
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
        <p class="lead">{e(COPY["home"]["intro"])}</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">Natural locs</p>
          <h2 class="title">DreadLocks</h2>
          <p class="lead">{e(next(s["copy"] for s in COPY["services"] if s["id"] == "locs"))}</p>
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
          <p class="lead">{e(COPY["home"]["salonBlock"])}</p>
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
        )
        + preview_bar()
        + nav("services.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Salon service</p>
        <h1 class="title">{e(locs["pageTitle"])}</h1>
        <p class="lead">{e(COPY["home"]["intro"])}</p>
      </div>
    </header>

    <section class="section" id="locs">
      <div class="wrap">
        <div data-reveal>
          <p class="kicker">Natural locs</p>
          <h2 class="title">{e(locs["sectionTitle"])}</h2>
          <p class="lead">{e(locs["intro"])}</p>
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
    for img in DATA["images"]["ig"]:
        cap = img.get("caption", "").split("\n")[0][:90]
        figures.append(
            f'<figure class="reveal-child"><img src="./{img["file"]}" alt="{e(cap)}" loading="lazy" /><figcaption>Instagram · {e(cap)}</figcaption></figure>'
        )
    for img in DATA["images"]["google"]:
        figures.append(
            f'<figure class="reveal-child"><img src="./{img["file"]}" alt="Kuzz Kreations salon" loading="lazy" /><figcaption>Google · Salon photo</figcaption></figure>'
        )

    return (
        head(
            "Gallery | Kuzz Kreations Brantford",
            "Real locs, braids and salon work from Instagram and Google.",
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
      <div class="wrap masonry">
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
        )
        + preview_bar()
        + nav("about.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">{e(GS["fullServiceHeading"])}</p>
        <h1 class="title">{e(GS["heroTitle"])}</h1>
        <p class="lead">{e(GS["about1"])}</p>
      </div>
    </header>

    <section class="section">
      <div class="wrap split">
        <div class="parallax-wrap" data-parallax>
          <img src="./images/google-0.jpg" alt="Kuzz Kreations salon" loading="lazy" />
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
        head("Contact | Kuzz Kreations Brantford", f"204 Dalhousie St · {PHONE}")
        + preview_bar()
        + nav("contact.html")
        + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap" data-reveal>
        <p class="kicker">Contact</p>
        <h1 class="title">{e(GS["stylistNote"])}</h1>
        <p class="lead">{e(COPY["home"]["bookBlock"])}</p>
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


def book() -> str:
    return (
        head("Book | Kuzz Kreations Brantford", COPY["home"]["bookBlock"][:140])
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
        "about.html": about(),
        "contact.html": contact(),
        "book.html": book(),
    }
    for name, content in pages.items():
        (ROOT / name).write_text(content)
    print("Wrote", ", ".join(pages))
