"""Shared page shell: head, header, footer. Returns HTML strings only."""
from html import escape

SITE_NAME = "Dimet"
SITE_URL = "https://dimet.si"
DESCRIPTION = "Industrijski materiali za vsak izziv: tehnične gume, cevi, pene, tesnila, trakovi in folije. Dimet d.o.o., Kranj."
EMAIL = "info@dimet.si"
PHONE = "+386 41 317 673"
ADDRESS = "Jezerska cesta 65, 4000 Kranj"

NAV = [
    ("izdelki/", "Izdelki"),
    ("novice/", "Novice"),
    ("o-nas.html", "O nas"),
    ("kontakt.html", "Kontakt"),
]


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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/site.css">
  <script src="{root}js/site.js" defer></script>
</head>
<body class="min-h-screen bg-paper text-ink antialiased">
  <a href="#main" class="skip-link">Preskoči na vsebino</a>
"""


def header(depth: int) -> str:
    root = _depth_prefix(depth)
    links = "".join(
        f'<a href="{root}{href}" class="nav-link">{label}</a>' for href, label in NAV
    )
    mobile = "".join(
        f'<a href="{root}{href}" class="block py-3 text-lg font-medium">{label}</a>' for href, label in NAV
    )
    return f"""  <header class="sticky top-0 z-40 border-b border-line bg-paper/95 backdrop-blur">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
      <a href="{root}index.html" class="flex items-center gap-2 font-extrabold tracking-tight text-ink" aria-label="Dimet, domača stran">
        <img src="{root}images/favicon.png" alt="" width="32" height="32" class="h-8 w-8 rounded">
        <span class="text-xl">Dimet</span>
      </a>
      <nav class="hidden items-center gap-6 md:flex" aria-label="Glavna navigacija">{links}</nav>
      <div class="flex items-center gap-2">
        <a href="{root}izdelki/" class="btn btn-primary hidden sm:inline-flex">Izdelki</a>
        <button type="button" class="btn btn-ghost md:hidden" data-nav-toggle aria-expanded="false" aria-controls="mobile-nav">
          <span class="sr-only">Meni</span>
          <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
      </div>
    </div>
    <nav id="mobile-nav" class="hidden border-t border-line px-4 pb-4 md:hidden" aria-label="Mobilna navigacija">{mobile}</nav>
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
    return f"""  <footer class="mt-24 border-t border-line bg-ink text-paper">
    <div class="mx-auto grid max-w-6xl gap-10 px-4 py-14 sm:px-6 md:grid-cols-3">
      <div>
        <p class="text-xl font-extrabold">Dimet d.o.o.</p>
        <p class="mt-3 max-w-xs text-sm text-paper/75">Industrijski materiali za vsak izziv. Tehnična guma, cevi, pene, tesnila in trakovi.</p>
      </div>
      <div class="text-sm">
        <h2 class="font-semibold uppercase tracking-wider text-paper/60">Kontakt</h2>
        <ul class="mt-3 space-y-2">
          <li>{ADDRESS}</li>
          <li><a class="footer-link" href="tel:{PHONE.replace(' ', '')}">{PHONE}</a></li>
          <li><a class="footer-link" href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
      <div class="text-sm">
        <h2 class="font-semibold uppercase tracking-wider text-paper/60">Informacije</h2>
        <nav aria-label="Informacije" class="mt-3"><ul class="space-y-2">{info_links}</ul></nav>
      </div>
    </div>
    <div class="border-t border-paper/10">
      <p class="mx-auto max-w-6xl px-4 py-5 text-xs text-paper/60 sm:px-6">&copy; {year} Dimet d.o.o. Vse pravice pridržane.</p>
    </div>
  </footer>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Organization","name":"Dimet d.o.o.","url":"{SITE_URL}","email":"{EMAIL}","telephone":"{PHONE}","address":{{"@type":"PostalAddress","streetAddress":"Jezerska cesta 65","postalCode":"4000","addressLocality":"Kranj","addressCountry":"SI"}}}}
  </script>
</body>
</html>
"""
