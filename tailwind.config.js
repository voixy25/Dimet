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
    "nav-link", "footer-link", "skip-link", "breadcrumb", "grid-products", "prose-site",
  ],
  theme: {
    extend: {
      colors: {
        paper: "#F7F5F0",
        ink: "#1B1F23",
        line: "#DAD6CC",
        graphite: "#3A4149",
        accent: "#B45309",
        "accent-hover": "#92400E",
        muted: "#5B6470",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      maxWidth: {
        container: "72rem",
      },
    },
  },
  plugins: [],
};
