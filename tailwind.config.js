/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./izdelki/**/*.html",
    "./novice/**/*.html",
    "./strani/**/*.html",
    "./js/**/*.js",
    "./scripts/**/*.py",
  ],
  safelist: [
    "container-site", "section", "h1-display", "h2-section", "lead", "card",
    "btn", "btn-primary", "btn-secondary", "btn-ghost", "badge", "chip",
    "topbar", "site-header", "category-box", "category-list", "hero-panel", "promo-tile", "section-title", "btn-brand",
    "nav-link", "footer-link", "skip-link", "breadcrumb", "grid-products", "prose-site",
  ],
  theme: {
    extend: {
      colors: {
        brand: "#007BC4",
        "brand-dark": "#006CAB",
        ink: "#0E0E0E",
        grey: "#F6F6F6",
        line: "#E5E5E5",
        muted: "#5B6470",
        // legacy aliases
        paper: "#F6F6F6",
        graphite: "#0E0E0E",
        accent: "#006CAB",
        "accent-hover": "#005A8F",
      },
      fontFamily: {
        sans: ["Arial", "Helvetica", "Liberation Sans", "sans-serif"],
      },
      maxWidth: {
        container: "72rem",
      },
    },
  },
  plugins: [],
};
