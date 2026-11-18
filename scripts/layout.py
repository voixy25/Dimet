"""Shared page shell: head, header, footer. Returns HTML strings only."""
from html import escape
from urllib.parse import quote

SITE_NAME = "Dimet"
SITE_URL = "https://dimet.si"
DESCRIPTION = "Industrijski materiali za vsak izziv: tehnične gume, cevi, pene, tesnila, trakovi in folije. Dimet d.o.o., Kranj."
EMAIL = "info@dimet.si"
PHONE = "+386 41 317 673"
ADDRESS = "Jezerska cesta 65, 4000 Kranj"

NAV = [
    ("index.html", "Domov"),
    ("o-nas.html", "O nas"),
    ("kontakt.html", "Kontakt"),
    ("novice/", "Novice"),
    ("izdelki/", "Izdelki"),
]

TOPBAR_LINKS = [
    ("novice/", "Novice"),
    ("strani/pogosta-vprasanja.html", "Pogosta vprašanja"),
    ("strani/politika-zasebnosti.html", "Politika zasebnosti"),
]
HOURS = "Delovni čas: pon-pet 8:00 - 16:00 | sob 8:00-12:00 | ned: zaprto"


def _depth_prefix(depth: int) -> str:
    return "../" * depth


def head(title: str, description: str, depth: int, path: str, og_image: str | None = None) -> str:
    root = _depth_prefix(depth)
    full_title = escape(title if title == SITE_NAME else f"{title} | {SITE_NAME}")
    canonical = f"{SITE_URL}/{path}"
    image = og_image or f"{SITE_URL}/images/favicon.png"
    return f"""<!doctype html>
<html lang="sl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{escape(image)}">
  <link rel="icon" href="{root}images/favicon.png" type="image/png">
  <link rel="stylesheet" href="{root}css/site.css">
  <script src="{root}js/site.js" defer></script>
</head>
<body class="min-h-screen bg-white text-ink antialiased">
  <a href="#main" class="skip-link">Preskoči na vsebino</a>
"""


def category_sidebar(depth: int, categories: dict[str, str]) -> str:
    root = _depth_prefix(depth)
    items = "".join(
        f'<li><a href="{root}izdelki/?q={quote(term)}">{escape(label)}</a></li>'
        for label, term in categories.items()
    )
    return (
        '<nav aria-label="Kategorije" class="hidden lg:block">'
        '<p class="category-box">Kategorije</p>'
        f'<ul class="category-list">{items}</ul></nav>'
    )


def header(depth: int) -> str:
    root = _depth_prefix(depth)
    top = "".join(
        f'<a href="{root}{href}" class="px-2">{label}</a>' for href, label in TOPBAR_LINKS
    )
    links = "".join(
        f'<a href="{root}{href}" class="nav-link px-3 font-bold uppercase hover:text-brand-dark">{label}</a>'
        for href, label in NAV
    )
    mobile = "".join(
        f'<a href="{root}{href}" class="block min-h-11 py-3 text-base font-bold uppercase">{label}</a>' for href, label in NAV
    )
    return f"""  <header class="site-header sticky top-0 z-40">
    <div class="topbar">
      <div class="container-site flex flex-wrap items-center justify-between gap-x-4">
        <p class="py-2">{HOURS}</p>
        <div class="hidden md:flex">{top}</div>
      </div>
    </div>
    <div class="container-site flex items-center justify-between gap-4 py-3">
      <a href="{root}index.html" class="inline-flex shrink-0" aria-label="Dimet, domača stran">
        <img src="{root}images/dimet-logo.jpg" alt="Dimet" width="168" height="56" class="h-14 w-auto">
      </a>
      <form action="{root}izdelki/" method="get" role="search" class="hidden min-w-0 flex-1 sm:flex sm:max-w-xl">
        <label for="site-search" class="sr-only">Iskanje izdelkov</label>
        <input id="site-search" type="search" name="q" placeholder="Iskanje izdelkov" class="min-h-11 w-full min-w-0 border border-line px-3 text-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand">
        <button type="submit" class="btn-brand"><span class="sr-only">Išči</span>
          <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
        </button>
      </form>
      <div class="flex items-center gap-2">
        <a href="{root}kontakt.html" class="nav-link hidden font-bold uppercase sm:inline-flex">Kontakt</a>
        <button type="button" class="btn btn-ghost lg:hidden" data-nav-toggle aria-expanded="false" aria-controls="mobile-nav">
          <span class="sr-only">Meni</span>
          <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
      </div>
    </div>
    <div class="hidden border-t border-line lg:block">
      <nav class="container-site flex items-center" aria-label="Glavna navigacija">{links}</nav>
    </div>
    <nav id="mobile-nav" class="hidden border-t border-line px-4 pb-4 lg:hidden" aria-label="Mobilna navigacija">{mobile}</nav>
  </header>
"""


def footer(depth: int) -> str:
    root = _depth_prefix(depth)
    info = [
        ("strani/pogosta-vprasanja.html", "Pogosta vprašanja"),
        ("strani/stroski-dostave.html", "Stroški dostave"),
        ("strani/nacin-placila.html", "Način plačila"),
        ("strani/vracilo-blaga.html", "Vračilo blaga"),
        ("strani/pogoji-poslovanja.html", "Pogoji poslovanja"),
        ("strani/politika-zasebnosti.html", "Politika zasebnosti"),
        ("strani/piskotki.html", "Piškotki"),
    ]
    info_links = "".join(f'<li><a class="footer-link" href="{root}{href}">{label}</a></li>' for href, label in info)
    year = "2026"
    return f"""  <footer class="mt-24 bg-ink text-white">
    <div class="mx-auto grid max-w-6xl gap-10 px-4 py-14 sm:px-6 md:grid-cols-3">
      <div>
        <p class="text-xl font-extrabold">Dimet d.o.o.</p>
        <p class="mt-3 max-w-xs text-sm text-white/80">Industrijski materiali za vsak izziv. Tehnična guma, cevi, pene, tesnila in trakovi.</p>
      </div>
      <div class="text-sm">
        <h2 class="font-semibold uppercase tracking-wider text-white/70">Kontakt</h2>
        <ul class="mt-3 space-y-2">
          <li>{ADDRESS}</li>
          <li><a class="footer-link" href="tel:{PHONE.replace(' ', '')}">{PHONE}</a></li>
          <li><a class="footer-link" href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
      <div class="text-sm">
        <h2 class="font-semibold uppercase tracking-wider text-white/70">Informacije</h2>
        <nav aria-label="Informacije" class="mt-3"><ul class="space-y-2">{info_links}</ul></nav>
      </div>
    </div>
    <div class="border-t border-white/10">
      <p class="mx-auto max-w-6xl px-4 py-5 text-xs text-white/70 sm:px-6">&copy; {year} Dimet d.o.o. Vse pravice pridržane.</p>
    </div>
  </footer>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Organization","name":"Dimet d.o.o.","url":"{SITE_URL}","email":"{EMAIL}","telephone":"{PHONE}","address":{{"@type":"PostalAddress","streetAddress":"Jezerska cesta 65","postalCode":"4000","addressLocality":"Kranj","addressCountry":"SI"}}}}
  </script>
</body>
</html>
"""
