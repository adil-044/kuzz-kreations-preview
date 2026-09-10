/**
 * Kuzz Kreations — tracker scaffold (HostGator go-live)
 * Stack stays static HTML/CSS/JS. Fill IDs after Wendy creates accounts.
 * Do NOT load marketing pixels until consent (Canada / PIPEDA-aware).
 *
 * Wire into pages via build_pages.py SCRIPTS when IDs are ready:
 *   <script src="./track.js" defer></script>
 *
 * Events to fire from site.js / book.js:
 *   phone_click, book_click, form_start, generate_lead
 */
(function () {
  var CONFIG = {
    gtmId: "", // e.g. GTM-XXXX
    ga4Id: "", // e.g. G-XXXX (only if not using GTM)
    clarityId: "", // Microsoft Clarity project id
    metaPixelId: "", // only if Meta Ads live
    requireConsent: true,
  };

  function consented() {
    if (!CONFIG.requireConsent) return true;
    try {
      return localStorage.getItem("kuzz_analytics_ok") === "1";
    } catch (e) {
      return false;
    }
  }

  window.kuzzTrack = {
    acceptAnalytics: function () {
      try {
        localStorage.setItem("kuzz_analytics_ok", "1");
      } catch (e) {}
      boot();
    },
    event: function (name, params) {
      if (!consented()) return;
      if (window.dataLayer) window.dataLayer.push(Object.assign({ event: name }, params || {}));
      if (window.gtag) window.gtag("event", name, params || {});
    },
  };

  function inject(src, attrs) {
    var s = document.createElement("script");
    s.src = src;
    s.async = true;
    if (attrs) Object.keys(attrs).forEach(function (k) { s.setAttribute(k, attrs[k]); });
    document.head.appendChild(s);
  }

  function boot() {
    if (!consented()) return;
    if (CONFIG.gtmId) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
      inject("https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(CONFIG.gtmId));
    } else if (CONFIG.ga4Id) {
      inject("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(CONFIG.ga4Id));
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", CONFIG.ga4Id);
    }
    if (CONFIG.clarityId) {
      (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      })(window, document, "clarity", "script", CONFIG.clarityId);
    }
    // Meta Pixel: add only when CONFIG.metaPixelId set + ads live + consent covers marketing
  }

  if (consented()) boot();
})();
