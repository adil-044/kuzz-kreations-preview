(function () {
  const y = document.getElementById("y");
  if (y) y.textContent = new Date().getFullYear();

  const toggle = document.querySelector("[data-nav-toggle]");
  const drawer = document.querySelector("[data-nav-drawer]");
  const closeBtn = document.querySelector("[data-nav-close]");
  if (toggle && drawer) {
    const open = () => {
      drawer.classList.add("open");
      drawer.setAttribute("aria-hidden", "false");
      toggle.setAttribute("aria-expanded", "true");
    };
    const close = () => {
      drawer.classList.remove("open");
      drawer.setAttribute("aria-hidden", "true");
      toggle.setAttribute("aria-expanded", "false");
    };
    toggle.addEventListener("click", open);
    closeBtn?.addEventListener("click", close);
    drawer.addEventListener("click", (e) => {
      if (e.target === drawer) close();
    });
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  }

  // Conversion hooks — no-op until track.js loaded with IDs + consent
  const ping = (name, params) => {
    if (window.kuzzTrack && typeof window.kuzzTrack.event === "function") {
      window.kuzzTrack.event(name, params || {});
    }
  };
  document.querySelectorAll('a[href^="tel:"]').forEach((a) => {
    a.addEventListener("click", () => ping("phone_click", { link_url: a.href }));
  });
  document.querySelectorAll('a[href*="book.html"]').forEach((a) => {
    a.addEventListener("click", () => ping("book_click", { link_url: a.getAttribute("href") }));
  });
})();
