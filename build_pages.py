#!/usr/bin/env python3
"""Generate static HTML pages for Kuzz Kreations preview."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data.json").read_text())

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

NAV = [
    ("services.html", "Services"),
    ("gallery.html", "Gallery"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
    ("book.html", "Book"),
]


def e(s: str) -> str:
    return html.escape(s or "")


def head(title: str, desc: str, page: str = "") -> str:
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
    return """  <div class="preview-bar" role="status">Preview — share this link with Wendy · changes update here before HostGator delivery</div>"""


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


def footer() -> str:
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
  <script src="./site.js"></script>"""


def reviews_block() -> str:
    quotes = []
    for r in DATA["reviews"]:
        if not r.get("text"):
            continue
        text = r["text"].strip()
        if len(text) > 220:
            text = text[:217] + "…"
        quotes.append(
            f'<blockquote class="quote"><p>"{e(text)}"</p><footer>— {e(r["name"])} · Google</footer></blockquote>'
        )
    return f"""    <section class="section section-alt" id="reviews">
      <div class="wrap">
        <p class="kicker">Google reviews</p>
        <div class="rating-row">
          <div class="score">{RATING}</div>
          <p class="lead" style="margin:0">Out of 5 from {REVIEWS} Google reviews · 204 Dalhousie St, Brantford</p>
        </div>
        <div class="quotes">
          {''.join(quotes)}
        </div>
      </div>
    </section>"""


def index() -> str:
    locs_imgs = [i for i in DATA["images"]["ig"] if "loc" in i.get("caption", "").lower() or "dread" in i.get("caption", "").lower()][:4]
    rail = []
    services = [
        ("Natural Locs", "Simple dreadlock hairstyles using natural castor oil — for longer, thicker hair.", locs_imgs[0]["file"] if locs_imgs else HERO, "#locs"),
        ("Starter & micro locs", "Two-strand twists, comb twists, or micro locs — your loc journey starts here.", locs_imgs[1]["file"] if len(locs_imgs) > 1 else HERO, "services.html#locs"),
        ("Loc maintenance", "Retightens, interlocking, hot oil treatments — castor, olive, avocado & hemp oils.", locs_imgs[2]["file"] if len(locs_imgs) > 2 else HERO, "services.html#locs-care"),
        ("Braids & extensions", "Knotless box, cornrows, weave extensions — protective styles for healthy growth.", "images/ig-CITtsmLn-Hf.jpg", "services.html#braids"),
    ]
    for title, blurb, img, href in services:
        rail.append(f"""<a class="style-card" href="{href}">
          <img src="./{img}" alt="{e(title)}" loading="lazy" width="300" height="375" />
          <div class="body"><h3>{e(title)}</h3><p>{e(blurb)}</p></div>
        </a>""")

    return head(
        "Kuzz Kreations | Natural Locs & Hair Salon Brantford",
        "Natural locs, micro locs, braids & extensions in Brantford. 4.7★ on Google. Book Wendy at 204 Dalhousie St.",
    ) + preview_bar() + nav("") + """
  <main id="main">
    <section class="hero" aria-label="Hero">
      <div class="hero-media" aria-hidden="true">
        <img src="./""" + HERO + """" alt="" width="2400" height="1500" fetchpriority="high" />
      </div>
      <div class="wrap hero-copy">
        <p class="pill">Brantford · Natural locs specialists</p>
        <p class="hero-brand">Look &amp; Feel <span>Beautiful</span></p>
        <h1>Natural locs &amp; textured hair — the best service, the best styles.</h1>
        <div class="hero-actions">
          <a class="btn btn-primary" href="./book.html">Book appointment</a>
          <a class="btn btn-ghost" href="./gallery.html">See locs work</a>
        </div>
        <div class="hero-stats">
          <div><strong>""" + str(RATING) + """★</strong><span>Google rating</span></div>
          <div><strong>""" + str(REVIEWS) + """</strong><span>Google reviews</span></div>
          <div><strong>Locs</strong><span>Our specialty</span></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker">Natural locs</p>
        <h2 class="title">Your loc journey — done with care</h2>
        <p class="lead">Natural locs are a highly tweakable, extremely versatile hairstyle. Whether you're starting dreadlocks on natural hair, re-styling existing locs, or enjoying the freedom of leaving your hair alone — we meet you where you are.</p>
        <div class="style-rail" aria-label="Locs services">
          """ + "\n          ".join(rail) + """
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap split">
        <img src="./images/ig-DbRdQS7OwNK.jpg" alt="Microlocs transformation at Kuzz Kreations" loading="lazy" width="1200" height="900" />
        <div class="copy">
          <p class="kicker">Why clients drive in</p>
          <h2 class="title">"You can't just let anyone put their hands in your hair."</h2>
          <p>At Kuzz Kreations Hair and Beauty Salon, our goal is to make you shine like a star. We create flattering, contemporary looks — specializing in natural locs, versatile styles for everyday life, and finished work you can trust in the chair.</p>
          <p style="margin-top:1rem">We believe you are your best accessory. Full-service experience: hair extensions, treatments, cornrows, color, and natural locs — with castor-oil care, clear communication, and a relaxing room.</p>
          <p style="margin-top:1.25rem"><a class="btn btn-primary" href="./about.html">About the salon</a></p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker">Full service</p>
        <h2 class="title">More than locs — one roof</h2>
        <div class="card-grid">
          <article class="card locs-feature">
            <div class="icon">L</div>
            <h3>Natural locs</h3>
            <p>Simple dreadlock hairstyles using natural castor oil which can enhance hair growth, for longer and thicker hair.</p>
            <a class="card-link" href="./services.html#locs">Explore locs →</a>
          </article>
          <article class="card">
            <div class="icon">B</div>
            <h3>Braids &amp; twists</h3>
            <p>Braids hairstyles and different types of twists for guys and women to ensure healthy hair growth.</p>
            <a class="card-link" href="./services.html#braids">Explore braids →</a>
          </article>
          <article class="card">
            <div class="icon">W</div>
            <h3>Weave extensions</h3>
            <p>Let our weave extensions do their magic — a protective way of boosting your style.</p>
            <a class="card-link" href="./services.html#weaves">Explore weaves →</a>
          </article>
          <article class="card">
            <div class="icon">C</div>
            <h3>Color &amp; care</h3>
            <p>Balayage and ombré blends, Olaplex bond building, silk press, and healthy relaxer technique.</p>
            <a class="card-link" href="./services.html#color">Explore more →</a>
          </article>
        </div>
      </div>
    </section>
""" + reviews_block() + """
    <section class="cta-band">
      <div class="wrap">
        <p class="kicker">Book</p>
        <h2 class="title">Ready for your locs appointment?</h2>
        <p class="lead">Call the salon on <a href="tel:""" + PHONE_TEL + """" style="color:var(--coral)">""" + PHONE + """</a> or use our online guest card for exclusive offers.</p>
        <p style="margin-top:1.25rem">
          <a class="btn btn-primary" href="./book.html">Book now</a>
          <a class="btn btn-ghost" href=\"""" + GUEST_CARD + """" target="_blank" rel="noopener">Guest card</a>
        </p>
      </div>
    </section>
  </main>
""" + footer() + "\n</body>\n</html>\n"


def services() -> str:
    return head(
        "Services | Natural Locs, Braids, Weaves — Kuzz Kreations",
        "Natural locs, micro locs, braids, weave extensions, crochet, color & Olaplex in Brantford. Consultation free.",
    ) + preview_bar() + nav("services.html") + """
  <main id="main">
    <header class="page-hero">
      <div class="wrap">
        <p class="kicker">Services</p>
        <h1 class="title">Our full service experience</h1>
        <p class="lead">Brantford's salon for natural locs, micro locs, braids, weave extensions, crochet braids, color, and textured-hair care. All prices are starting prices — final cost confirmed at booking.</p>
      </div>
    </header>

    <section class="section" id="locs">
      <div class="wrap">
        <p class="kicker">Natural locs</p>
        <h2 class="title">Locs hairstyles</h2>
        <p class="lead">Natural locs are highly tweakable and extremely versatile — starter twists on short hair, micro locs, comb twists, restyles, and retightens with healthy-hair care.</p>
        <div class="card-grid">
          <article class="card locs-feature"><h3>How to start dreadlocks</h3><p>The health of your hair is the most important part of your loc journey. With the right care and time you can two-strand twist starter locs on short hair, single braids on natural hair, or comb twist styles.</p></article>
          <article class="card locs-feature"><h3>Micro locs &amp; short styles</h3><p>Short crochet micro locs and fine locs for detail and styling freedom. Healthy-looking locs start with proper care, patience, and consistency.</p></article>
          <article class="card locs-feature"><h3>Loc styles &amp; updos</h3><p>Wear them up, wear them down, curl them, crimp them, and even color them. Whether your locks are long or short we can make your locs style look great.</p></article>
          <article class="card locs-feature"><h3>Loc styles for men</h3><p>We do locs with care, class, and passion — using the best products with integrity for your loc styles. Hair texture plays a big role in how to loc your hair.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="locs-care">
      <div class="wrap split">
        <img src="./images/ig-C5E7jYWRrQJ.jpg" alt="Herbal oil steam treatment for locs" loading="lazy" />
        <div class="copy">
          <p class="kicker">Loc care</p>
          <h2 class="title">Castor oil hot oil treatment</h2>
          <p>Our castor oil hot oil treatment moisturizes locs, deeply penetrates all layers of the hair follicle, and with its high omega-9 fatty acid content helps prevent the scalp from drying out and supports healthy growth.</p>
          <p style="margin-top:1rem">Best oils for locs: castor oil, olive oil, avocado oil &amp; hemp oil. Herbal oil steam treatments encourage blood flow, hydrate locs, and help minimize dandruff.</p>
        </div>
      </div>
    </section>

    <section class="section" id="braids">
      <div class="wrap">
        <p class="kicker">Braids</p>
        <h2 class="title">Braids, twists &amp; men's styles</h2>
        <div class="card-grid">
          <article class="card"><h3>Braids extensions</h3><p>Braids hairstyles and different types of twists — protective styles that stay sharp.</p></article>
          <article class="card"><h3>Men's braids</h3><p>Men braids styles the way you want them, with care to ensure healthy hair growth and style.</p></article>
          <article class="card"><h3>Cornrows</h3><p>Classic and creative cornrow patterns for women and men.</p></article>
          <article class="card"><h3>Crochet braids</h3><p>Healthy hair care begins with an exfoliating cleanse to remove product build up — then latch-hook crochet styles.</p></article>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="weaves">
      <div class="wrap">
        <p class="kicker">Extensions</p>
        <h2 class="title">Weave extensions</h2>
        <p class="lead">Let our weave extensions do their magic — a protective way of boosting your style.</p>
        <div class="card-grid">
          <article class="card"><h3>Sew-in / weft</h3><p>Full-head weaves from <strong style="color:var(--gold)">$200+</strong> (starting price).</p></article>
          <article class="card"><h3>Microlink / micro ring</h3><p>Braidless options from <strong style="color:var(--gold)">$185+</strong> (starting price).</p></article>
          <article class="card"><h3>Clip-ins</h3><p>Flexible length for events — call for current options.</p></article>
        </div>
      </div>
    </section>

    <section class="section" id="color">
      <div class="wrap">
        <p class="kicker">Color &amp; care</p>
        <h2 class="title">Cut, color, press &amp; repair</h2>
        <div class="card-grid">
          <article class="card"><h3>Hair cut &amp; color</h3><p>Make a dramatic color change from soft balayage and ombré blends in natural hues of blonde, brown and red.</p></article>
          <article class="card"><h3>Olaplex treatments</h3><p>Rejuvenate your hair with our penetrating treatment that repairs damaged hair and fights frizzy hair. Olaplex bond building — eco-friendly developments for growth and thickness.</p></article>
          <article class="card"><h3>Perm relaxer</h3><p>We provide the best relaxer technique for healthy hair — without compromising your texture goals.</p></article>
        </div>
        <p style="margin-top:1.75rem"><a class="btn btn-primary" href="./book.html">Book a service</a></p>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <p class="kicker">Policy</p>
        <div class="card-grid">
          <article class="card"><h3>Consultation</h3><p>Consultation is free. Send pictures in advance for a more exact cost. All prices are starting prices.</p></article>
          <article class="card"><h3>Deposits</h3><p>A deposit of $50 is mandatory with all services — deducted from your total at checkout. Full refund within 24 hours of booking.</p></article>
        </div>
      </div>
    </section>
  </main>
""" + footer() + "\n</body>\n</html>\n"


def gallery() -> str:
    figures = []
    for img in DATA["images"]["ig"]:
        cap = img.get("caption", "").split("\n")[0][:80]
        tag = "Instagram" if img["source"] == "instagram" else "Google"
        figures.append(
            f'<figure><img src="./{img["file"]}" alt="{e(cap)}" loading="lazy" /><figcaption>{e(tag)} · {e(cap)}</figcaption></figure>'
        )
    for img in DATA["images"]["google"]:
        figures.append(
            f'<figure><img src="./{img["file"]}" alt="Kuzz Kreations salon work" loading="lazy" /><figcaption>Google · Salon photo</figcaption></figure>'
        )

    return head(
        "Gallery | Locs & Hair Work — Kuzz Kreations Brantford",
        "Real locs, braids and salon work from Kuzz Kreations Instagram and Google — Brantford textured hair.",
    ) + preview_bar() + nav("gallery.html") + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap">
        <p class="kicker">Gallery</p>
        <h1 class="title">Real work from the chair</h1>
        <p class="lead">Photos from <a href="{INSTAGRAM}" target="_blank" rel="noopener" style="color:var(--coral)">@kuzzkreationshairstyles</a> and our Google listing — locs first, then braids and salon styles.</p>
      </div>
    </header>
    <section class="section">
      <div class="wrap masonry">
        {''.join(figures)}
      </div>
      <p class="wrap" style="margin-top:1.5rem;text-align:center">
        <a class="btn btn-primary" href="./book.html">Book your style</a>
      </p>
    </section>
  </main>
""" + footer() + "\n</body>\n</html>\n"


def about() -> str:
    owner = (
        "Brantford's premiere salon for color, cuts, cornrow styles, braid extensions, "
        "weave extensions, dreadlocks, micro locs, crochet braids and other natural styles. "
        "We're a full-service beauty salon dedicated to genuine customer care — excellent service, "
        "quality products, and an enjoyable atmosphere at fair value. We maintain a friendly, fair, "
        "and creative work environment that respects diversity, ideas, and hard work."
    )
    return head(
        "About | Kuzz Kreations Hair Salon Brantford",
        "Meet Kuzz Kreations — Brantford textured-hair salon. Natural locs, braids, extensions, and Olaplex care.",
    ) + preview_bar() + nav("about.html") + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap">
        <p class="kicker">About</p>
        <h1 class="title">A full service experience</h1>
        <p class="lead">{e(owner)}</p>
      </div>
    </header>

    <section class="section">
      <div class="wrap split">
        <img src="./images/google-0.jpg" alt="Kuzz Kreations salon" loading="lazy" />
        <div class="copy">
          <p class="kicker">The salon</p>
          <h2 class="title">Best-in-class customer experience</h2>
          <p>At Kuzz Kreations we believe in delivering best-in-class customer experience — some of the best stylists in our Brantford salon, high-quality products, and a relaxing ambiance.</p>
          <p style="margin-top:1rem">We make sure our products contain the finest ingredients formulated for all types of hair, customized to the right services and products for your needs.</p>
        </div>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <p class="kicker">Products</p>
        <div class="card-grid">
          <article class="card"><h3>Olaplex bond building</h3><p>Keeping up with the latest eco-friendly developments in the beauty industry — for hair growth and thickness that keeps hair healthy all year long.</p></article>
          <article class="card"><h3>Clean hair care</h3><p>Hydrating and nourishing collection — safer high-performing hair care without harmful ingredients.</p></article>
          <article class="card"><h3>Castor &amp; herbal oils</h3><p>Castor oil, olive, avocado and hemp — core to our loc maintenance and hot oil treatments.</p></article>
        </div>
        <p style="margin-top:1.75rem">
          <a class="btn btn-primary" href="./book.html">Book with us</a>
          <a class="btn btn-ghost" href="{GUEST_CARD}" target="_blank" rel="noopener">Guest card</a>
        </p>
      </div>
    </section>
  </main>
""" + footer() + "\n</body>\n</html>\n"


def contact() -> str:
    return head(
        "Contact | Kuzz Kreations Brantford",
        "Visit Kuzz Kreations at 204 Dalhousie St, Brantford. Call 519-209-8803. Mon–Sat.",
    ) + preview_bar() + nav("contact.html") + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap">
        <p class="kicker">Contact</p>
        <h1 class="title">Visit the salon</h1>
        <p class="lead">Need to speak with a specific stylist? Call or book — we're happy to assist.</p>
      </div>
    </header>
    <section class="section">
      <div class="wrap visit-grid">
        <dl class="info-card">
          <dt>Address</dt>
          <dd>{e(ADDRESS)}</dd>
          <dt>Phone</dt>
          <dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
          <dt>Hours</dt>
          <dd>Mon–Wed 9:00 AM – 7:30 PM<br>Thu–Fri 9:00 AM – 7:00 PM<br>Sat 9:00 AM – 5:00 PM<br>Sun closed</dd>
        </dl>
        <dl class="info-card">
          <dt>Social</dt>
          <dd><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @kuzzkreationshairstyles</a></dd>
          <dd><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></dd>
          <dt>Directions</dt>
          <dd><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></dd>
          <dt>Guest card</dt>
          <dd><a href="{GUEST_CARD}" target="_blank" rel="noopener">Join for offers &amp; discounts</a></dd>
        </dl>
      </div>
      <p style="margin-top:1.5rem;text-align:center">
        <a class="btn btn-primary" href="./book.html">Book appointment</a>
      </p>
    </section>
  </main>
""" + footer() + "\n</body>\n</html>\n"


def book() -> str:
    return head(
        "Book Appointment | Kuzz Kreations Brantford",
        "Book natural locs, braids, weaves or treatments at Kuzz Kreations. Text request to 519-209-8803.",
    ) + preview_bar() + nav("book.html") + f"""
  <main id="main">
    <header class="page-hero">
      <div class="wrap">
        <p class="kicker">Book</p>
        <h1 class="title">Book an appointment</h1>
        <p class="lead">If you'd like to book with us, call the salon on <a href="tel:{PHONE_TEL}" style="color:var(--coral)">{PHONE}</a> — or send a booking text below. Wendy confirms by phone.</p>
      </div>
    </header>
    <div class="wrap book-layout">
      <div class="book-panel">
        <h2>Request by text</h2>
        <p class="note">$50 deposit required — refundable within 24 hours of booking. Consultation is free.</p>
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
              <option>Loc styles / updos</option>
              <option>Hot oil / herbal steam treatment</option>
              <option>Knotless box braids</option>
              <option>Braids with extensions</option>
              <option>Men's braids / cornrows</option>
              <option>Crochet braids</option>
              <option>Sew-in / weave</option>
              <option>Microlink extensions</option>
              <option>Color / balayage</option>
              <option>Silk press / cut</option>
              <option>Olaplex / treatment</option>
              <option>Relaxer</option>
              <option>Consult / other</option>
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
          <div class="field"><label for="notes">Notes</label><textarea id="notes" name="notes" placeholder="Hair length, loc stage, photos sent, kids…"></textarea></div>
          <div class="form-actions">
            <button class="btn btn-primary" type="submit">Send booking text</button>
            <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call salon</a>
          </div>
          <p class="form-status" id="status" role="status" aria-live="polite"></p>
        </form>
      </div>
      <aside class="book-panel">
        <h2>Starting prices</h2>
        <p class="note">From the salon's current list — final quote after consult.</p>
        <table class="price-table">
          <thead><tr><th>Service</th><th>From</th></tr></thead>
          <tbody>
            <tr><td>Full head weave (no closure)</td><td>$200+</td></tr>
            <tr><td>Micro ring extensions</td><td>$185+</td></tr>
            <tr><td>Loc consult</td><td>Free</td></tr>
            <tr><td>Deposit (all services)</td><td>$50</td></tr>
          </tbody>
        </table>
        <p style="margin-top:1.25rem"><a class="btn btn-soft" href="{GUEST_CARD}" target="_blank" rel="noopener">Guest card</a></p>
        <ul style="margin:1.25rem 0 0;padding-left:1.1rem;color:var(--muted);font-size:0.92rem">
          <li>Mon–Wed 9–7:30 · Thu–Fri 9–7 · Sat 9–5 · Sun closed</li>
          <li>{e(ADDRESS)}</li>
        </ul>
      </aside>
    </div>
  </main>
""" + footer() + "\n  <script src=\"./book.js\"></script>\n</body>\n</html>\n"


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
