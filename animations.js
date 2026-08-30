(function () {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;
  gsap.registerPlugin(ScrollTrigger);

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) {
    document.querySelectorAll("[data-reveal], .reveal-child").forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
      el.style.filter = "none";
    });
    return;
  }

  // Hero load sequence
  const hero = document.querySelector("[data-hero]");
  if (hero) {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
    tl.fromTo(
      hero.querySelector(".hero-media img"),
      { scale: 1.12, yPercent: -4 },
      { scale: 1, yPercent: 0, duration: 1.4 }
    );
    tl.from(
      hero.querySelectorAll("[data-hero-item]"),
      { opacity: 0, y: 32, filter: "blur(6px)", stagger: 0.1, duration: 0.9 },
      "-=0.9"
    );
  }

  // Hero parallax on scroll
  const heroImg = document.querySelector(".hero-media img");
  if (heroImg && hero) {
    gsap.to(heroImg, {
      yPercent: 12,
      ease: "none",
      scrollTrigger: {
        trigger: hero,
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });
  }

  // Generic scroll reveals
  gsap.utils.toArray("[data-reveal]").forEach((el, i) => {
    gsap.fromTo(
      el,
      { opacity: 0.2, y: 28, filter: "blur(5px)" },
      {
        opacity: 1,
        y: 0,
        filter: "blur(0px)",
        duration: 0.95,
        delay: Number(el.dataset.revealDelay || 0),
        ease: "power3.out",
        scrollTrigger: {
          trigger: el,
          start: "top 88%",
          toggleActions: "play none none none",
        },
      }
    );
  });

  // Stagger children in grids
  gsap.utils.toArray("[data-stagger]").forEach((wrap) => {
    const kids = wrap.querySelectorAll(".reveal-child");
    if (!kids.length) return;
    gsap.fromTo(
      kids,
      { opacity: 0, y: 22, scale: 0.98 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.7,
        stagger: 0.08,
        ease: "power2.out",
        scrollTrigger: {
          trigger: wrap,
          start: "top 85%",
          toggleActions: "play none none none",
        },
      }
    );
  });

  // Split / parallax images
  gsap.utils.toArray("[data-parallax]").forEach((wrap) => {
    const img = wrap.querySelector("img");
    if (!img) return;
    gsap.fromTo(
      img,
      { yPercent: -8, scale: 1.08 },
      {
        yPercent: 8,
        scale: 1,
        ease: "none",
        scrollTrigger: {
          trigger: wrap,
          start: "top bottom",
          end: "bottom top",
          scrub: true,
        },
      }
    );
  });

  // Style rail hint animation
  const rail = document.querySelector(".style-rail");
  if (rail && rail.scrollWidth > rail.clientWidth) {
    gsap.to(rail, {
      scrollLeft: 80,
      duration: 1.2,
      ease: "power1.inOut",
      yoyo: true,
      repeat: 1,
      repeatDelay: 0.4,
      delay: 1.5,
    });
  }

  // Nav shrink on scroll
  const nav = document.querySelector(".nav");
  if (nav) {
    ScrollTrigger.create({
      start: "top -40",
      onUpdate: (self) => {
        nav.classList.toggle("nav-scrolled", self.scroll() > 40);
      },
    });
  }

  // Gallery figures
  gsap.utils.toArray(".masonry figure").forEach((fig, i) => {
    gsap.fromTo(
      fig,
      { opacity: 0, y: 20, scale: 0.97 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.65,
        delay: (i % 4) * 0.05,
        ease: "power2.out",
        scrollTrigger: {
          trigger: fig,
          start: "top 92%",
          toggleActions: "play none none none",
        },
      }
    );
  });

  // Counter pulse on rating
  const score = document.querySelector(".score");
  if (score) {
    gsap.fromTo(
      score,
      { scale: 0.85, opacity: 0 },
      {
        scale: 1,
        opacity: 1,
        duration: 0.8,
        ease: "back.out(1.4)",
        scrollTrigger: { trigger: score, start: "top 90%" },
      }
    );
  }
})();
