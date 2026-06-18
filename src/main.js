import { updateAuthUI } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
  console.log("=== PAGE LOADED ===");
  console.log("Token in localStorage:", localStorage.getItem("jwt") ? "YES" : "NO");
  
  initApp();
});

function initApp() {
  initMenu();
  initSlider();
  updateAuthUI();
}

/* ================= MENU ================= */
function initMenu() {
  const btn = document.getElementById("menu-button");
  const nav = document.getElementById("mob-nav");

  if (!btn || !nav) return;

  btn.addEventListener("click", () => {
    if (nav.style.maxHeight === "0px" || nav.style.maxHeight === "") {
      nav.style.maxHeight = nav.scrollHeight + "px";
    } else {
      nav.style.maxHeight = "0px";
    }
  });
}

/* ================= SLIDER ================= */
let current = 0;
let visible;

function initSlider() {
  const track = document.getElementById("sliderTrack");
  const slides = document.querySelectorAll(".slide-container");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");

  if (!track || slides.length === 0) return;

  function moveSlider() {
    const gap = parseInt(getComputedStyle(track).gap);
    const slideWidth = slides[0].offsetWidth + gap;

    track.style.transform = `translateX(-${current * slideWidth}px)`;
  }

  function updateVisibleCards() {
    if (window.innerWidth < 640) visible = 1;
    else if (window.innerWidth < 1024) visible = 2;
    else visible = 3;

    slides.forEach((slide) => {
      slide.style.flexBasis = `calc((100% - ${(visible - 1) * 32}px) / ${visible})`;
    });

    const max = Math.max(0, slides.length - visible);

    if (current > max) current = max;

    moveSlider();
  }

  nextBtn?.addEventListener("click", () => {
    const max = slides.length - visible;
    if (current < max) current++;
    moveSlider();
  });

  prevBtn?.addEventListener("click", () => {
    if (current > 0) current--;
    moveSlider();
  });

  updateVisibleCards();
  window.addEventListener("resize", updateVisibleCards);
}

/* ================= AUTH ================= */
// Auth functions are now in auth.js