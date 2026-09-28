# Kuzz Kreations — HostGator delivery checklist (SEO + trackers)

**Stack (locked):** static HTML / CSS / JS + GSAP CDN. No framework change.  
**Client:** Wendy · deposit received · preview must be approved before zip.

Preview: https://adil-044.github.io/kuzz-kreations-preview/  
Vault: [[Kuzz Kreations Delivery Lock 2026-08-30]] · [[Conversion Tracking Stack Client Websites 2026-09-10]]

---

## A. Before zip (build)

- [x] Remove orange **preview bar** (`has-preview` / `preview_bar()`) — done in `pack_hostgator.py`
- [x] Wendy copy untouched (`copy.json` wendy blocks)
- [x] Hero = IG `DTDxJLbkQXk` slide 2
- [x] Rebuild: `python3 build_pages.py` then `python3 pack_hostgator.py`
- [x] Locs scroll stage + gallery animations — assets verified in delivery smoke-test

## D. Zip contents (shipped 2026-09-28)

```
Kuzz-Kreations-Website/
  README.md · UPLOAD.txt · docs/SEO-AND-TRACKERS.md
  public_html/
    *.html · css/styles.css · js/* · images/
    .htaccess · robots.txt (live) · sitemap.xml · llms.txt
```

Zip path (vault): `500 - Exports/clients/kuzz-kreations/Kuzz-Kreations-Website-HostGator-2026-09-28.zip`

## B. SEO files in zip

| File | Action |
|---|---|
| `llms.txt` | Ship as-is (canonical domain kuzzkreations.ca) |
| `sitemap.xml` | Ship |
| `robots.txt` | Use **`robots.live.txt` contents** (Allow + Sitemap) — not preview Disallow |
| Pages | Unique title + meta description + canonical + OG + JSON-LD HairSalon |
| Images | Real work alts; compress if HostGator size limit |

Post go-live:

- [ ] Google Search Console → property + sitemap submit  
- [ ] GBP → website URL = live domain · NAP match **204 Dalhousie St**  
- [ ] Spot-check titles on mobile  

## C. Trackers (Canada-aware)

Default stack (playbook): **GTM + GA4 events + Clarity + UTMs**.  
Meta Pixel only if Meta ads live.

- [ ] Wendy Google account → create GA4 (+ GTM preferred)  
- [ ] Clarity project  
- [ ] Copy `track.example.js` → `track.js`, fill IDs  
- [ ] Consent: Privacy blurb or cookies note + analytics accept before load  
- [ ] Events: `phone_click`, `book_click`, `form_start`, `generate_lead`  
- [ ] IG bio / ads use UTMs  
- [ ] Tag Assistant verify on live domain  
- [ ] 1-page “how to read weekly report” for Wendy  

**Do not** ship empty marketing pixels. **Do not** put trackers on GitHub preview while `Disallow: /`.

## D. Zip contents

```
index.html · services.html · gallery.html · about.html · team.html · book.html · contact.html
stylist-*.html (if kept)
styles.css · site.js · book.js · animations.js · track.js (when IDs ready)
images/
llms.txt · sitemap.xml · robots.txt (live version)
UPLOAD.txt (cPanel File Manager steps)
```

## E. Payment gate

Final **$169.50** on go-live (INV-KUZZ-002).
