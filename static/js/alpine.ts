import collapse from "@alpinejs/collapse";
import Alpine from "alpinejs";

Alpine.plugin(collapse);

declare global {
  interface Window {
    Alpine: typeof Alpine;
  }
}
window.Alpine = Alpine;

const HEADER_ID = "site-header";
const HERO_SELECTOR = ".hero-section";
const SOLID_AT_PX = 12;

// Avoid double-binding (HTMX + BFCache + hot reload)
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

function applyHeaderState(): void {
  const header = getHeader();
  if (!header) return;

  const hero = hasHero();
  header.toggleAttribute("data-has-hero", hero);

  // If no hero on this page, header should be solid always.
  if (!hero) {
    setSolid(header, true);
    return;
  }

  // If mobile menu is open, force solid for legibility.
  if (menuOpen(header)) {
    setSolid(header, true);
    return;
  }

  // Correct, reliable scroll source:
  const y = window.scrollY || 0;

  // Desired behavior:
  // - At top of hero (y <= SOLID_AT_PX) => NOT solid
  // - After scrolling down => solid
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

  // Run immediately + again on next paint (mobile viewport settling)
  applyHeaderState();
  requestAnimationFrame(applyHeaderState);

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", applyHeaderState, { passive: true });

  // BFCache restore (Safari/iOS)
  window.addEventListener("pageshow", () => requestAnimationFrame(applyHeaderState), { passive: true });

  // HTMX navigations / swaps
  document.body.addEventListener("htmx:afterSwap", () => requestAnimationFrame(applyHeaderState));
  document.body.addEventListener("htmx:afterSettle", () => requestAnimationFrame(applyHeaderState));
}

document.addEventListener("DOMContentLoaded", () => {
  Alpine.start();
  bindHeader();
});
