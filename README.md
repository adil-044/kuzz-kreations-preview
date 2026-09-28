# Kuzz Kreations — client preview (dev)

**Live preview:** https://adil-044.github.io/kuzz-kreations-preview/

Static HTML/CSS/JS + GSAP for Wendy. Orange preview bar stays on GitHub Pages only.

## HostGator delivery (Wendy zip)

```bash
python3 build_pages.py      # refresh HTML from copy.json if needed
python3 pack_hostgator.py   # builds dist/ + zip (strips preview bar)
```

Output:

- `dist/Kuzz-Kreations-Website/` — guided folder (`README.md`, `UPLOAD.txt`, `docs/`, `public_html/`)
- `dist/Kuzz-Kreations-Website-HostGator-YYYY-MM-DD.zip` — send this to Wendy

Upload **only** contents of `public_html/` into HostGator `public_html`.

## Preview content

- Copy: Wendy-approved locs + kuzzkreations.ca / Google Sites (`copy.json`)
- Photos: Instagram + Google listing (`images/`)
- Facts: 4.7★ / 53 reviews · 204 Dalhousie St
- SEO service landings + Services nav dropdown
- Delivery SEO notes: `DELIVERY-SEO-TRACKERS.md`
