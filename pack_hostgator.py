#!/usr/bin/env python3
"""Build a clean HostGator delivery folder + zip for Wendy.

Run from repo root:
  python3 pack_hostgator.py

Output:
  dist/Kuzz-Kreations-Website/
  dist/Kuzz-Kreations-Website-HostGator-YYYY-MM-DD.zip
"""
from __future__ import annotations

import re
import shutil
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
PKG_NAME = "Kuzz-Kreations-Website"
TODAY = date.today().isoformat()

HTML_PAGES = [
    "index.html",
    "services.html",
    "gallery.html",
    "team.html",
    "about.html",
    "contact.html",
    "book.html",
    "locs.html",
    "braids-extensions.html",
    "braids-for-men.html",
    "weave-extensions.html",
    "crochet-braids.html",
    "hair-color.html",
    "olaplex.html",
    "relaxer.html",
    "stylist-1.html",
    "stylist-2.html",
    "stylist-3.html",
    "stylist-4.html",
]

ASSET_JS = ["site.js", "book.js", "animations.js", "track.example.js"]


README = f"""# Kuzz Kreations — website delivery

**Client:** Wendy · Kuzz Kreations Hair & Beauty Salon  
**Domain:** https://kuzzkreations.ca  
**Address:** 204 Dalhousie St, Brantford, ON N3S 3T7 · **519-209-8803**  
**Packed:** {TODAY} · Uptisement

This zip is the **live HostGator site**. Preview orange bar is removed. Live `robots.txt` allows Google.

---

## Start here (Wendy)

1. Read **`UPLOAD.txt`** — step-by-step cPanel upload.
2. Upload **everything inside `public_html/`** into your HostGator **`public_html`** folder (or the folder your domain points to).
3. Visit https://kuzzkreations.ca and click Home → Services → Locs → Book → Gallery → Contact.
4. Optional later: tracking IDs — see **`docs/SEO-AND-TRACKERS.md`**.

You do **not** need to upload `README.md`, `UPLOAD.txt`, or `docs/` to the server. Those are guides for you.

---

## Folder map

```
Kuzz-Kreations-Website/
├── README.md                 ← this file
├── UPLOAD.txt                ← HostGator / cPanel steps
├── docs/
│   └── SEO-AND-TRACKERS.md   ← Search Console + analytics (after go-live)
└── public_html/              ← UPLOAD THIS FOLDER’S CONTENTS TO HOSTGATOR
    ├── index.html            ← home
    ├── services.html
    ├── locs.html … relaxer.html   ← SEO service pages
    ├── gallery.html · team.html · about.html · contact.html · book.html
    ├── stylist-1.html … stylist-4.html
    ├── css/
    │   └── styles.css
    ├── js/
    │   ├── site.js
    │   ├── book.js
    │   ├── animations.js
    │   └── track.example.js  ← rename to track.js when IDs ready
    ├── images/               ← salon photos
    ├── .htaccess             ← redirects old URLs (dreads.html → locs.html)
    ├── robots.txt            ← live (Allow + Sitemap)
    ├── sitemap.xml
    └── llms.txt
```

---

## What this site includes

- Locs-first home, gallery, team, about, contact, SMS book form
- Clickable service SEO pages (Natural Locs, Braids, Men’s Braids, Weave, Crochet, Color, Olaplex, Relaxer)
- Services dropdown in the main nav
- Old-site redirects via `.htaccess` (keeps Google links working)

---

## Need a change?

Text Adil / Uptisement with the page name and what to change. Do not edit HTML by hand unless you are comfortable — easy to break layout.

**Support:** uptisement.com
"""

UPLOAD = """# How to upload Kuzz Kreations to HostGator (cPanel)

Time: about 10–15 minutes. Use a computer (not phone).

## Before you start

1. Unzip **Kuzz-Kreations-Website-HostGator-….zip** on your computer.
2. Open the folder **Kuzz-Kreations-Website**.
3. You will upload only what is **inside** the **public_html** folder.

## Steps

1. Log in to **HostGator** → open **cPanel**.
2. Open **File Manager**.
3. Go to **public_html** (or the directory your domain kuzzkreations.ca uses).
4. **Backup first (important):**
   - Select current files (old site).
   - Compress / download a zip backup, OR rename the old folder to `old-site-backup`.
5. Upload the **contents** of this package’s `public_html/` folder:
   - All `.html` files
   - Folders: `css/`, `js/`, `images/`
   - Files: `.htaccess`, `robots.txt`, `sitemap.xml`, `llms.txt`
6. If File Manager asks to overwrite — yes, after your backup.
7. Make sure **index.html** is in public_html (not inside another nested folder).
8. Visit https://kuzzkreations.ca — hard refresh (Ctrl+Shift+R / Cmd+Shift+R).

## Quick checks after upload

- [ ] Home loads with plum / coral design
- [ ] **Services** in the top menu shows a dropdown on hover (desktop)
- [ ] https://kuzzkreations.ca/locs.html opens
- [ ] https://kuzzkreations.ca/dreads.html redirects to locs (old link)
- [ ] Book page form / call button works
- [ ] Photos load on Gallery

## Common mistakes

| Mistake | Fix |
|---|---|
| Uploaded the outer zip folder so URL is /Kuzz-Kreations-Website/public_html/ | Move files up into public_html root |
| Forgot `.htaccess` | Re-upload `.htaccess` (enable “Show Hidden Files” in File Manager) |
| Old cache | Hard refresh or try phone data |

## Still stuck?

Email or text Uptisement with a screenshot of File Manager showing public_html.
"""

SEO_DOC = """# SEO + trackers (after the site is live)

Do this **after** HostGator upload looks good.

## Search

1. Google Search Console → add https://kuzzkreations.ca
2. Submit sitemap: `https://kuzzkreations.ca/sitemap.xml`
3. Google Business Profile → website = https://kuzzkreations.ca
4. NAP must match: **204 Dalhousie St, Brantford, ON N3S 3T7** · **519-209-8803**

## Analytics (optional — ask Uptisement)

Default stack: GTM + GA4 + Microsoft Clarity + UTMs.  
Canada: consent before marketing cookies when required.

1. Create GA4 (and GTM if preferred) on Wendy’s Google account
2. Copy `js/track.example.js` → `js/track.js` and fill IDs
3. Add to pages (Uptisement can do this):  
   `<script src="./js/track.js" defer></script>`
4. Events already hooked as no-ops in `site.js`: phone / book / lead

**Do not** ship empty Meta Pixel unless ads are running.

## Old URLs (already in .htaccess)

| Old | New |
|---|---|
| dreads.html | locs.html |
| braidsextensions.html | braids-extensions.html |
| weave_extensions.html | weave-extensions.html |
| crochetbraids.html | crochet-braids.html |
| service.html | services.html |
| contactus.html | contact.html |
"""


def live_html(raw: str) -> str:
    """Strip preview chrome and point assets at css/ + js/."""
    out = raw
    out = out.replace('<body class="has-preview">', "<body>")
    out = re.sub(
        r'\s*<div class="preview-bar"[^>]*>.*?</div>\s*',
        "\n",
        out,
        count=1,
        flags=re.S,
    )
    out = re.sub(
        r'href="\./styles\.css(?:\?[^"]*)?"',
        'href="./css/styles.css?v=20260928"',
        out,
    )
    out = out.replace('src="./site.js"', 'src="./js/site.js"')
    out = out.replace('src="./animations.js"', 'src="./js/animations.js"')
    out = out.replace('src="./book.js"', 'src="./js/book.js"')
    out = out.replace('src="./track.js"', 'src="./js/track.js"')
    out = out.replace('src="./track.example.js"', 'src="./js/track.example.js"')
    return out


def assert_source() -> None:
    missing = [p for p in HTML_PAGES if not (ROOT / p).exists()]
    if missing:
        raise SystemExit(f"Missing pages (run build_pages.py first): {missing}")
    for js in ASSET_JS:
        if not (ROOT / js).exists():
            raise SystemExit(f"Missing {js}")
    if not (ROOT / "styles.css").exists():
        raise SystemExit("Missing styles.css")
    if not (ROOT / "images").is_dir():
        raise SystemExit("Missing images/")


def pack() -> Path:
    assert_source()
    DIST.mkdir(exist_ok=True)
    pkg = DIST / PKG_NAME
    if pkg.exists():
        shutil.rmtree(pkg)

    site = pkg / "public_html"
    (pkg / "docs").mkdir(parents=True)
    (site / "css").mkdir(parents=True)
    (site / "js").mkdir(parents=True)

    (pkg / "README.md").write_text(README)
    (pkg / "UPLOAD.txt").write_text(UPLOAD)
    (pkg / "docs" / "SEO-AND-TRACKERS.md").write_text(SEO_DOC)

    for name in HTML_PAGES:
        html = live_html((ROOT / name).read_text(encoding="utf-8"))
        (site / name).write_text(html, encoding="utf-8")

    shutil.copy2(ROOT / "styles.css", site / "css" / "styles.css")
    for js in ASSET_JS:
        shutil.copy2(ROOT / js, site / "js" / js)

    shutil.copytree(ROOT / "images", site / "images")
    shutil.copy2(ROOT / ".htaccess", site / ".htaccess")
    shutil.copy2(ROOT / "robots.live.txt", site / "robots.txt")
    shutil.copy2(ROOT / "sitemap.xml", site / "sitemap.xml")
    shutil.copy2(ROOT / "llms.txt", site / "llms.txt")

    # Optional: leave a short note in public_html for tech-savvy clients
    (site / "UPLOAD-NOTE.txt").write_text(
        "These files belong in HostGator public_html.\n"
        "Guides are one level up: ../README.md and ../UPLOAD.txt\n"
    )

    zip_path = DIST / f"Kuzz-Kreations-Website-HostGator-{TODAY}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in pkg.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(DIST))

    print(f"Packed: {pkg}")
    print(f"Zip:    {zip_path}")
    print(f"Size:   {zip_path.stat().st_size / 1e6:.1f} MB")
    return zip_path


if __name__ == "__main__":
    pack()
