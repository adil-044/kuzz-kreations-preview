(function () {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;
  gsap.registerPlugin(ScrollTrigger);

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) {
    document.querySelectorAll("[data-reveal], .reveal-child, .locs-slide").forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
      el.style.filter = "none";
    });
    document.querySelectorAll(".locs-slide").forEach((el, i) => {
      if (i === 0) el.classList.add("is-active");
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

  // Locs scroll stage — pin + scrub through real work
  const stage = document.querySelector("[data-locs-stage]");
  if (stage) {
    const slides = gsap.utils.toArray("[data-locs-slide]", stage);
    const dots = gsap.utils.toArray("[data-locs-dot]", stage);
    const progress = stage.querySelector("[data-locs-progress]");
    const pin = stage.querySelector(".locs-stage-pin");

    const setActive = (index) => {
      slides.forEach((slide, i) => {
        slide.classList.toggle("is-active", i === index);
      });
      dots.forEach((dot, i) => {
        dot.classList.toggle("is-active", i === index);
      });
    };

    if (slides.length > 1 && pin) {
      const total = slides.length;
      ScrollTrigger.create({
        trigger: stage,
        start: "top top",
        end: () => "+=" + window.innerHeight * (total * 0.85),
        pin: pin,
        scrub: 0.65,
        anticipatePin: 1,
        onUpdate: (self) => {
          const idx = Math.min(total - 1, Math.floor(self.progress * total));
          setActive(idx);
          if (progress) progress.style.transform = `scaleX(${self.progress})`;
        },
      });

      // Soft Ken Burns on active frame image
      slides.forEach((slide) => {
        const img = slide.querySelector("img");
        if (!img) return;
        gsap.fromTo(
          img,
          { scale: 1.08 },
          {
            scale: 1,
            ease: "none",
            scrollTrigger: {
              trigger: stage,
              start: "top top",
              end: () => "+=" + window.innerHeight * (total * 0.85),
              scrub: true,
            },
          }
        );
      });
    }

    dots.forEach((dot) => {
      dot.addEventListener("click", () => {
        const i = Number(dot.getAttribute("data-locs-dot") || 0);
        setActive(i);
        if (progress) progress.style.transform = `scaleX(${(i + 0.5) / slides.length})`;
      });
    });
  }

  // Infinite work marquee
  const marquee = document.querySelector("[data-work-marquee] .work-marquee-track");
  if (marquee) {
    const half = marquee.scrollWidth / 2;
    gsap.to(marquee, {
      x: -half,
      duration: 28,
      ease: "none",
      repeat: -1,
      modifiers: {
        x: gsap.utils.unitize((x) => parseFloat(x) % -half),
      },
    });
  }

  // Generic scroll reveals
  gsap.utils.toArray("[data-reveal]").forEach((el) => {
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
      { opacity: 0, y: 36, scale: 0.96, rotate: 0.4 },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        rotate: 0,
        duration: 0.75,
        stagger: 0.09,
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
      scrollLeft: 100,
      duration: 1.35,
      ease: "power1.inOut",
      yoyo: true,
      repeat: 1,
      repeatDelay: 0.35,
      delay: 1.2,
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

  // Gallery figures — clip reveal
  gsap.utils.toArray(".masonry figure, .gallery-tile").forEach((fig, i) => {
    gsap.fromTo(
      fig,
      { opacity: 0, y: 28, clipPath: "inset(12% 8% 12% 8% round 12px)" },
      {
        opacity: 1,
        y: 0,
        clipPath: "inset(0% 0% 0% 0% round 12px)",
        duration: 0.8,
        delay: (i % 4) * 0.06,
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
