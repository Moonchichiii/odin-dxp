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
