import collapse from "@alpinejs/collapse";
import Alpine from "alpinejs";

Alpine.plugin(collapse);

declare global {
  interface Window {
    Alpine: typeof Alpine;
    scrollPastHero?: () => void;
  }
}
window.Alpine = Alpine;

// --- Countdown component (global, used by CountdownBlock) ---
Alpine.data("countdown", (expiryRaw: string) => ({
  expiry: 0,
  expired: false,
  days: "00",
  hours: "00",
  minutes: "00",
  seconds: "00",
  _timer: null as number | null,

  init() {
    // Parse safely (supports ISO, and also "YYYY-MM-DD HH:MM:SS")
    const normalized = (expiryRaw || "").includes("T")
      ? expiryRaw
      : (expiryRaw || "").replace(" ", "T");

    const ts = new Date(normalized).getTime();
    this.expiry = Number.isFinite(ts) ? ts : 0;

    this.tick();
    this._timer = window.setInterval(() => this.tick(), 1000);
  },

  tick() {
    if (!this.expiry) {
      this.expired = true;
      this.days = this.hours = this.minutes = this.seconds = "00";
      if (this._timer) window.clearInterval(this._timer);
      return;
    }

    const now = Date.now();
    const dist = this.expiry - now;

    if (dist <= 0) {
      this.expired = true;
      this.days = this.hours = this.minutes = this.seconds = "00";
      if (this._timer) window.clearInterval(this._timer);
      return;
    }

    this.days = Math.floor(dist / (1000 * 60 * 60 * 24))
      .toString()
      .padStart(2, "0");

    this.hours = Math.floor((dist % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      .toString()
      .padStart(2, "0");

    this.minutes = Math.floor((dist % (1000 * 60 * 60)) / (1000 * 60))
      .toString()
      .padStart(2, "0");

    this.seconds = Math.floor((dist % (1000 * 60)) / 1000)
      .toString()
      .padStart(2, "0");
  },
}));

const HEADER_ID = "site-header";
const HERO_SELECTOR = ".hero-section";
const SOLID_AT_PX = 12;
const ROOT = document.documentElement;

let bound = false;

function getHeader(): HTMLElement | null {
  return document.getElementById(HEADER_ID) as HTMLElement | null;
}

function hasHero(): boolean {
  return Boolean(document.querySelector(HERO_SELECTOR));
}

function menuOpen(header: HTMLElement): boolean {
  return header.getAttribute("data-menu-open") === "true";
}

function setSolid(header: HTMLElement, solid: boolean): void {
  header.setAttribute("data-solid", solid ? "true" : "false");
}

function setHeaderHeightVar(): void {
  const header = getHeader();
  if (!header) return;
  ROOT.style.setProperty("--header-h", `${header.offsetHeight}px`);
}

function applyHeaderState(): void {
  const header = getHeader();
  if (!header) return;

  setHeaderHeightVar();

  const hero = hasHero();
  header.toggleAttribute("data-has-hero", hero);

  if (!hero) {
    setSolid(header, true);
    return;
  }

  if (menuOpen(header)) {
    setSolid(header, true);
    return;
  }

  const y = window.scrollY || 0;
  setSolid(header, y > SOLID_AT_PX);
}

function bindHeader(): void {
  if (bound) return;
  bound = true;

  const prefersReducedMotion =
    window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;

  let ticking = false;

  const onScroll = () => {
    if (prefersReducedMotion) {
      applyHeaderState();
      return;
    }
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      applyHeaderState();
      ticking = false;
    });
  };

  applyHeaderState();
  requestAnimationFrame(applyHeaderState);

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", applyHeaderState, { passive: true });
  window.addEventListener(
    "pageshow",
    () => requestAnimationFrame(applyHeaderState),
    { passive: true },
  );

  document.body.addEventListener("htmx:afterSwap", () =>
    requestAnimationFrame(applyHeaderState),
  );
  document.body.addEventListener("htmx:afterSettle", () =>
    requestAnimationFrame(applyHeaderState),
  );
}

function scrollPastHero(): void {
  const hero = document.querySelector(HERO_SELECTOR) as HTMLElement | null;
  if (!hero) return;

  const heroBottom = hero.getBoundingClientRect().bottom + window.scrollY;
  window.scrollTo({ top: heroBottom, behavior: "smooth" });
}

window.scrollPastHero = scrollPastHero;

// --- ANALYTICS LOADER ---
function loadScripts() {
  console.log("🚀 User consented. Loading Analytics & Third-party scripts...");

  // Example: Google Analytics (GTM)
  // You can replace this with the actual GTM snippet provided by Google
  /*
  const gtmId = 'GTM-XXXXXX'; // Replace with real ID
  (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer', gtmId);
  */

  // Example: HubSpot
  /*
  const script = document.createElement('script');
  script.src = "//js.hs-scripts.com/YOUR_HUB_ID.js";
  script.async = true;
  document.body.appendChild(script);
  */
}

function initAnalytics() {
  // 1. Check if already accepted in the past
  if (localStorage.getItem("odin_cookie_consent") === "accepted") {
    loadScripts();
  }

  // 2. Listen for the live "Accept" click
  window.addEventListener("cookie-consent-granted", () => {
    loadScripts();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  Alpine.start();
  bindHeader();
  initAnalytics();
});

/* ================================
   GSAP Arc Carousel (CMS-safe)
   ================================ */

type MousePos = { x: number; y: number };

const lerp = (start: number, end: number, amt: number) =>
  (1 - amt) * start + amt * end;

const prefersReducedMotion = () =>
  window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;

class ArcSliderItem {
  DOM: { el: HTMLElement; layers: NodeListOf<HTMLElement> };
  index: number;
  length: number;
  extra: number;

  width = 320;
  height = 420;
  padding = 40;
  widthTotal = 0;
  x = 0;
  r = 0;

  hover = false;

  rendered = {
    txPrev: 0,
    tyPrev: 0,
    txCur: 0,
    tyCur: 0,
  };

  constructor(el: HTMLElement, index: number, length: number) {
    this.DOM = {
      el,
      layers: el.querySelectorAll<HTMLElement>(".slider-layer"),
    };

    this.DOM.layers.forEach((layer) => {
      if (!layer.dataset.range) layer.dataset.range = "0";
    });

    this.index = index;
    this.length = length;
    this.extra = 0;

    this.initEvents();
  }

  initEvents() {
    this.DOM.el.addEventListener("mouseenter", () => (this.hover = true));
    this.DOM.el.addEventListener("mouseleave", () => {
      this.hover = false;
      this.rendered.txPrev = 0;
      this.rendered.tyPrev = 0;

      // reset layers smoothly
      this.DOM.layers.forEach((layer) => {
        gsap.to(layer, { duration: 0.45, x: 0, y: 0, ease: "power2.out" });
      });
    });
  }

   onResize(viewportWidth: number) {
    // FIX: Optimized dimensions for Mobile (Fits iPhone/Android screens comfortably)

    // Mobile: 200px wide x 280px tall (Small Poster)
    // Desktop: 280px wide x 400px tall (Standard Poster)
    this.width = viewportWidth < 768 ? 200 : 280;
    this.height = viewportWidth < 768 ? 280 : 400;

    // Tighter spacing on mobile
    this.padding = viewportWidth < 768 ? 15 : 40;

    this.widthTotal = (this.width + this.padding) * this.length;
    this.x = (this.width + this.padding) * this.index;

    // Adjust arc radius: Flatter on mobile to prevent extreme distortion/overflow
    this.r = viewportWidth * (viewportWidth < 768 ? 3 : 2.5);

    this.DOM.el.style.width = `${this.width}px`;
    this.DOM.el.style.height = `${this.height}px`;
    this.DOM.el.style.marginTop = `${-this.height / 2}px`;
    this.DOM.el.style.marginLeft = `${-this.width / 2}px`;

    this.extra = 0;
  }

  update(
    scrollCurrent: number,
    direction: "left" | "right",
    viewportWidth: number,
    viewportHeight: number,
    mousepos: MousePos,
    isMobile: boolean,
  ) {
    const n = this.x - scrollCurrent - this.extra;

    let h = Math.asin(n / this.r) * (180 / Math.PI);

    if (Number.isNaN(h)) {
      this.DOM.el.style.opacity = "0";
      h = 0;
    } else {
      this.DOM.el.style.opacity = "1";
    }

    const a = this.r - Math.cos((h * Math.PI) / 180) * this.r;

    // arc + slight rotation
    this.DOM.el.style.transform = `translate3d(${n}px, ${a}px, 0) rotate(${h * 0.5}deg)`;

    // infinite loop boundaries
    const cardBuffer = this.width * 2;
    const boundary = viewportWidth / 2 + cardBuffer;

    const isBefore = n < -boundary;
    const isAfter = n > boundary;

    if (direction === "right" && isBefore) {
      this.extra -= this.widthTotal;
    } else if (direction === "left" && isAfter) {
      this.extra += this.widthTotal;
    }

    // parallax hover (desktop only)
    if (this.hover && !isMobile) {
      const tx = (mousepos.x - viewportWidth / 2) * 0.05;
      const ty = (mousepos.y - viewportHeight / 2) * 0.05;

      this.rendered.txCur = tx;
      this.rendered.tyCur = ty;

      this.rendered.txPrev = lerp(this.rendered.txPrev, this.rendered.txCur, 0.1);
      this.rendered.tyPrev = lerp(this.rendered.tyPrev, this.rendered.tyCur, 0.1);

      this.DOM.layers.forEach((layer) => {
        const range = Number.parseFloat(layer.dataset.range ?? "0") || 0;
        gsap.set(layer, {
          x: this.rendered.txPrev * range * 4,
          y: this.rendered.tyPrev * range * 4,
        });
      });
    }
  }
}

class ArcSlider {
  container: HTMLElement;
  wrapper: HTMLElement;
  medias: NodeListOf<HTMLElement>;
  items: ArcSliderItem[] = [];

  viewportWidth = 0;
  viewportHeight = 0;
  isMobile = false;

  mousepos: MousePos = { x: 0, y: 0 };

  scroll = {
    current: 0,
    target: 0,
    last: 0,
    ease: 0.08,
  };

  isDown = false;
  startX = 0;
  scrollPos = 0;

  rafId: number | null = null;
  isRunning = false;

  io?: IntersectionObserver;
  isVisible = true;

  // mousemove throttling
  private mouseRAF: number | null = null;
  private pendingMouse: MousePos | null = null;

  constructor(container: HTMLElement) {
    this.container = container;

    const wrapper = container.querySelector(".slider-wrapper") as HTMLElement | null;
    const medias = container.querySelectorAll<HTMLElement>(".slider-media");

    if (!wrapper || medias.length === 0) {
      // nothing to do
      this.wrapper = container;
      this.medias = medias;
      return;
    }

    this.wrapper = wrapper;
    this.medias = medias;

    this.init();
  }

  init() {
    // reduced motion: do not start
    if (prefersReducedMotion()) return;

    this.createMedias();
    this.onResize();
    this.addEvents();
    this.setupVisibilityPause();
    this.start();
  }

  createMedias() {
    const originalList = Array.from(this.medias);
    const minItems = 12;

    if (originalList.length > 0 && originalList.length < minItems) {
      const repeatCount = Math.ceil(minItems / originalList.length);
      const fragment = document.createDocumentFragment();

      for (let i = 0; i < repeatCount - 1; i++) {
        originalList.forEach((item) => fragment.appendChild(item.cloneNode(true)));
      }

      this.wrapper.appendChild(fragment);
      this.medias = this.wrapper.querySelectorAll<HTMLElement>(".slider-media");
    }

    const all = Array.from(this.medias);
    this.items = all.map((el, i) => new ArcSliderItem(el, i, all.length));
  }

  onResize = () => {
    const rect = this.container.getBoundingClientRect();
    this.viewportWidth = rect.width;
    this.viewportHeight = rect.height;
    this.isMobile = this.viewportWidth < 768;

    this.items.forEach((item) => item.onResize(this.viewportWidth));
  };

  onDown = (x: number) => {
    this.isDown = true;
    this.startX = x;
    this.scrollPos = this.scroll.target;
  };

  onMove = (x: number) => {
    if (!this.isDown) return;
    const dist = (this.startX - x) * 1.5;
    this.scroll.target = this.scrollPos + dist;
  };

  onUp = () => {
    this.isDown = false;
  };

  addEvents() {
    // mouse dragging
    this.container.addEventListener("mousedown", (e) => this.onDown(e.clientX));
    window.addEventListener("mousemove", (e) => this.onMove(e.clientX));
    window.addEventListener("mouseup", this.onUp);

    // touch dragging
    this.container.addEventListener(
      "touchstart",
      (e) => this.onDown(e.touches[0].clientX),
      { passive: true },
    );
    window.addEventListener(
      "touchmove",
      (e) => this.onMove(e.touches[0].clientX),
      { passive: true },
    );
    window.addEventListener("touchend", this.onUp);

    // mouse parallax (throttled)
    this.container.addEventListener("mousemove", (ev) => {
      const rect = this.container.getBoundingClientRect();
      this.pendingMouse = { x: ev.clientX - rect.left, y: ev.clientY - rect.top };

      if (this.mouseRAF) return;
      this.mouseRAF = requestAnimationFrame(() => {
        if (this.pendingMouse) this.mousepos = this.pendingMouse;
        this.pendingMouse = null;
        this.mouseRAF = null;
      });
    });

    window.addEventListener("resize", this.onResize);

    // prevent clicks if dragging
    this.container.addEventListener(
      "click",
      (e) => {
        if (Math.abs(this.scroll.last - this.scroll.target) > 5) e.preventDefault();
      },
      true,
    );
  }

  setupVisibilityPause() {
    // Pause when tab hidden
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) this.stop();
      else this.start();
    });

    // Pause when carousel offscreen
    this.io = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        this.isVisible = Boolean(entry?.isIntersecting);

        if (!this.isVisible) this.stop();
        else this.start();
      },
      { threshold: 0.05 },
    );

    this.io.observe(this.container);
  }

  start() {
    if (this.isRunning) return;
    if (document.hidden) return;
    if (!this.isVisible) return;

    this.isRunning = true;
    this.update();
  }

  stop() {
    this.isRunning = false;
    if (this.rafId) cancelAnimationFrame(this.rafId);
    this.rafId = null;
  }

  update = () => {
    if (!this.isRunning) return;

    this.scroll.current = lerp(this.scroll.current, this.scroll.target, this.scroll.ease);

    const direction: "left" | "right" =
      this.scroll.current > this.scroll.last ? "right" : "left";

    this.items.forEach((item) =>
      item.update(
        this.scroll.current,
        direction,
        this.viewportWidth,
        this.viewportHeight,
        this.mousepos,
        this.isMobile,
      ),
    );

    this.scroll.last = this.scroll.current;
    this.rafId = requestAnimationFrame(this.update);
  };
}

/* Init helpers (multi-carousel + HTMX safe) */
function initArcCarousels(root: ParentNode = document) {
  const carousels = root.querySelectorAll<HTMLElement>("[data-gsap-carousel]");

  carousels.forEach((el) => {
    if ((el as any).__arcInit) return;
    (el as any).__arcInit = true;

    // only init if gsap exists
    if (typeof (window as any).gsap === "undefined") return;

    new ArcSlider(el);
  });
}

/* Boot on load + HTMX swaps */
document.addEventListener("DOMContentLoaded", () => initArcCarousels());
document.body.addEventListener("htmx:afterSwap", (e: any) => initArcCarousels(e.target));
