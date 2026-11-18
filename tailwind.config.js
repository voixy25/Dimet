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
    "btn", "btn-primary", "btn-secondary", "btn-ghost", "btn-brand", "badge", "chip",
    "topbar", "site-header", "pill-search",
    "category-box", "category-list", "category-flyout", "hero-panel", "promo-tile",
    "section-title", "nav-link", "footer-link", "skip-link",
    "breadcrumb", "grid-products", "prose-site",
  ],
  theme: {
    container: {
      center: true,
      padding: "1rem",
      screens: {
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1222px",
        "2xl": "1222px",
      },
    },
    extend: {
      colors: {
        brand: "#007BC4",
        "brand-dark": "#006AA9",
        "brand-accent": "#FBBC34",
        "cta-blue": "#0081FF",
        "title-dark": "#242424",
        "heading-dark": "#333333",
        "body-text": "#767676",
        "slide-light": "#F2F2F2",
        "footer-dark": "#0A0A0A",
        "border-light": "#E8E8E8",
        // legacy aliases
        ink: "#242424",
        grey: "#F2F2F2",
        line: "#E8E8E8",
        muted: "#767676",
        paper: "#F2F2F2",
        graphite: "#0A0A0A",
        accent: "#007BC4",
        "accent-hover": "#006AA9",
      },
      fontFamily: {
        sans: ["Lato", "Arial", "Helvetica", "sans-serif"],
        heading: ["Poppins", "Arial", "Helvetica", "sans-serif"],
        accent: ["Montserrat", "sans-serif"],
      },
      maxWidth: {
        container: "1222px",
      },
    },
  },
  plugins: [],
};
