import Alpine from "alpinejs";

declare global {
  interface Window {
    Alpine: typeof Alpine;
  }
}

window.Alpine = Alpine;

function initHeaderLogic() {
  const header = document.getElementById("site-header");
  const hero = document.querySelector(".hero-section");

  if (!header) return;

  // 1. HERO DETECTION
  if (hero) {
    header.setAttribute("data-has-hero", "true");
  } else {
    // If no hero, clean up attributes so it defaults to solid HTML classes
    header.removeAttribute("data-has-hero");
    header.removeAttribute("data-solid");
    return; // Stop here, no scroll logic needed for non-hero pages
  }

  // 2. SCROLL LOGIC (Only runs if hero exists)
  const applyScrollState = () => {
    // Re-check hero existence in case of dynamic removal
    if (!document.querySelector(".hero-section")) return;

    const isMobileMenuOpen = document.body.style.overflow === "hidden";
    const isScrolled = window.scrollY > 20;

    const shouldBeSolid = isScrolled || isMobileMenuOpen;

    // Only touch DOM if changed
    if (header.getAttribute("data-solid") !== String(shouldBeSolid)) {
      header.setAttribute("data-solid", shouldBeSolid ? "true" : "false");
    }
  };

  applyScrollState();
  window.addEventListener("scroll", applyScrollState, { passive: true });
  window.addEventListener("resize", applyScrollState, { passive: true });
}

document.addEventListener("DOMContentLoaded", () => {
  Alpine.start();
  initHeaderLogic();
});

document.addEventListener("htmx:afterSwap", () => {
  initHeaderLogic();
});
