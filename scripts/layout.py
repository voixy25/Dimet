"""Shared page shell: head, header, footer. Returns HTML strings only."""
from html import escape
from urllib.parse import quote

SITE_NAME = "Dimet"
SITE_URL = "https://dimet.si"
DESCRIPTION = (
    "Industrijski materiali za vsak izziv: tehnične gume, cevi, pene, tesnila, "
    "trakovi in folije. Dimet d.o.o., Kranj."
)
EMAIL = "info@dimet.si"
PHONE = "+386 41 317 673"
ADDRESS = "Jezerska cesta 65, 4000 Kranj"
HOURS = "DELOVNI ČAS | PON-PET: 8:00 - 16:00 | SOB: 8:00-12:00 | NED: ZAPRTO"

NAV = [
    ("index.html", "Domov"),
    ("o-nas.html", "O nas"),
    ("kontakt.html", "Kontakt"),
    ("izdelki/index.html", "Izdelki"),
    ("novice/index.html", "Novice"),
]

TOPBAR_LINKS = [
    ("novice/index.html", "Novice"),
    ("strani/pogosta-vprasanja.html", "Pogosta vprašanja"),
    ("strani/politika-zasebnosti.html", "Politika zasebnosti"),
]

SOCIAL_LINKS = [
    (
        "Facebook",
        "https://www.facebook.com/",
        '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    ),
    (
        "Instagram",
        "https://www.instagram.com/",
        '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/>'
        '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
        '<line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
    ),
    (
        "LinkedIn",
        "https://www.linkedin.com/",
        '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/>'
        '<rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>',
    ),
]

CATEGORY_MENU: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("Samokolnice", "samokolnice", [
        ("Samokolnica DMT 80 L", "samokolnica"),
        ("Samokolnica 6404", "6404"),
        ("Gumi ročaji", "rocaj"),
    ]),
    ("Pnevmatike", "pnevmatike", [
        ("Moto pnevmatike", "mc50"),
        ("Kolesne gume", "186"),
        ("Vozičkovne gume", "390"),
    ]),
    ("Zračnice", "zracnice", [
        ("Zračnice TR-75A", "tr-75a"),
        ("Moto zračnice", "tr-4"),
        ("Vozičkovne zračnice", "10x2"),
    ]),
    ("Ščitniki", "scitniki", [
        ("Ščitniki moto", "scitnik moto"),
        ("Industrijski ščitniki", "11.00"),
    ]),
    ("Cevi", "cevi", [
        ("Cevi za vodo", "cev za vodo"),
        ("Cevi za bencin", "cev za bencin"),
        ("Cevi za zrak", "cev za zrak"),
    ]),
    ("Profili", "profili", [
        ("Profil U keder", "keder"),
        ("Penasti profili", "penasti"),
        ("Profili guma+kovina", "prtljaznik"),
    ]),
    ("Tesnila", "tesnila", [
        ("Tesnila za tlačilko", "tlacilko"),
        ("Tesnila Damper", "damper"),
        ("Tesnilni trakovi", "tesnilni trak"),
    ]),
    ("Jermeni", "jermeni", [
        ("Okrogli jermeni", "jermen okrogli"),
        ("Klinasti jermeni", "li c"),
        ("Zobati jermeni", "sawasbelt"),
    ]),
    ("Pena", "pena", [
        ("Zvočna izolacija", "zvocno izolacijo"),
        ("Penasti izdelki", "profil penasti"),
        ("Lepila v razpršilu", "lepilo"),
    ]),
    ("Tehnična plastika", "tehnicna-plastika", [
        ("Poliamid PA 6G", "poliamid"),
        ("Polietilen PE/HD", "polietilen"),
        ("Poliuretan plošče", "poliuretan"),
    ]),
    ("Drobni gumeni-tehnični izdelki", "drobni-gumeni-tehnicni-izdelki", [
        ("Gumi čepi", "cep"),
        ("Natiki", "natik"),
        ("Vezice", "vezice"),
        ("Gumaflex", "gumaflex"),
    ]),
]

FOOTER_INFO_LINKS = [
    ("strani/pogoji-poslovanja.html", "Pogoji poslovanja"),
    ("strani/nacin-placila.html", "Način plačila"),
    ("strani/stroski-dostave.html", "Stroški dostave"),
    ("strani/vracilo-blaga.html", "Vračilo blaga"),
    ("strani/piskotki.html", "Piškotki"),
]

FOOTER_ABOUT_LINKS = [
    ("index.html", "Domača stran", False),
    ("novice/index.html", "Novice", False),
    ("o-nas.html", "O nas", False),
    ("kontakt.html", "Kontakt", False),
    ("https://www.facebook.com/", "Facebook", True),
]


def _depth_prefix(depth: int) -> str:
    return "../" * depth


def head(title: str, description: str, depth: int, path: str, og_image: str | None = None) -> str:
    """Render document <head> and opening <body> tag."""
    root = _depth_prefix(depth)
    full_title = escape(title if title == SITE_NAME else f"{title} | {SITE_NAME}")
    canonical = escape(f"{SITE_URL}/{path}")
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Poppins:wght@500;600;700&display=swap">
  <link rel="icon" href="{root}images/favicon.png" type="image/png">
  <link rel="stylesheet" href="{root}css/site.css">
  <script src="{root}js/site.js" defer></script>
</head>
<body class="min-h-screen bg-white font-sans text-body-text antialiased">
  <a href="#main" class="skip-link">Preskoči na vsebino</a>
"""


def _category_flyout_items(root: str, is_home: bool) -> str:
    """Build the 11 parent category items with hover flyouts."""
    chevron = (
        '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m9 18 6-6-6-6"/></svg>'
    )
    rows: list[str] = []
    for label, cat_slug, subitems in CATEGORY_MENU:
        sub_links = "".join(
            f'<li><a href="{root}izdelki/index.html?q={quote(sq)}" '
            'class="block py-1.5 text-sm text-body-text transition hover:text-[#006AA9]">'
            f'{escape(sl)}</a></li>'
            for sl, sq in subitems
        )
        cat_href = f"{root}izdelki/index.html?cat={quote(cat_slug)}"
        rows.append(
            '<li>'
            f'<a href="{cat_href}">'
            f'<span>{escape(label)}</span>{chevron}</a>'
            '<div class="category-flyout">'
            f'<p class="mb-2 border-b border-[#E8E8E8] pb-3 font-heading text-xs font-semibold uppercase tracking-wide text-[#242424]">{escape(label)}</p>'
            f'<ul class="space-y-1">{sub_links}</ul>'
            f'<p class="mt-3 border-t border-[#E8E8E8] pt-2">'
            f'<a href="{cat_href}" class="text-xs font-semibold uppercase text-[#007BC4] hover:text-[#006AA9]">Prikaži vse &rarr;</a>'
            '</p>'
            '</div>'
            '</li>'
        )
    visibility = "block" if is_home else "hidden shadow-lg"
    return (
        f'<nav aria-label="Kategorije" class="absolute left-0 top-full z-30 w-[300px] {visibility}">'
        f'<ul class="category-list">{"".join(rows)}</ul>'
        '</nav>'
    )


def category_sidebar(depth: int, categories: dict[str, str]) -> str:
    """Legacy category sidebar helper preserved for downstream page builders."""
    root = _depth_prefix(depth)
    items = "".join(
        f'<li><a href="{root}izdelki/index.html?q={quote(term)}">{escape(label)}</a></li>'
        for label, term in categories.items()
    )
    return (
        '<nav aria-label="Kategorije" class="hidden lg:block">'
        '<p class="category-box">Kategorije</p>'
        f'<ul class="category-list">{items}</ul></nav>'
    )


def _current_attr(href: str, current: str) -> str:
    """Return aria-current="page" for the nav entry that contains the current page."""
    if href.endswith("/index.html"):
        active = current.startswith(href[:-len("index.html")])
    elif href.endswith("/"):
        active = current.startswith(href)
    else:
        active = current == href
    return ' aria-current="page"' if active and current else ""


def _render_topbar(root: str) -> str:
    socials = "".join(
        f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer" aria-label="{escape(name)}" class="p-1.5 text-white/90 hover:text-white">'
        f'<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svg_path}</svg>'
        '</a>'
        for name, url, svg_path in SOCIAL_LINKS
    )
    top_links = '<span class="text-white/40" aria-hidden="true">|</span>'.join(
        f'<a href="{root}{href}" class="px-2.5 text-white hover:underline">{escape(label)}</a>'
        for href, label in TOPBAR_LINKS
    )
    return f"""    <div class="topbar hidden h-[42px] bg-[#007BC4] text-xs text-white lg:block">
      <div class="container-site flex h-full items-center justify-between gap-4">
        <p class="font-sans tracking-wide">{escape(HOURS)}</p>
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1 border-r border-white/25 pr-3">{socials}</div>
          <div class="flex items-center">{top_links}</div>
        </div>
      </div>
    </div>"""


def _render_header_actions(root: str) -> str:
    tel_href = f"tel:{PHONE.replace(' ', '')}"
    return f"""      <div class="flex items-center gap-3 lg:gap-4">
        <a href="{tel_href}" class="hidden items-center gap-2 text-sm font-bold text-[#242424] transition hover:text-[#006AA9] xl:inline-flex">
          <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span>{PHONE}</span>
        </a>
        <a href="{root}kontakt.html" aria-label="Kontakt" title="Kontakt" class="hidden items-center gap-1.5 text-[13px] font-bold uppercase text-[#242424] transition hover:text-[#006AA9] sm:inline-flex">
          <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
          <span class="hidden md:inline">Kontakt</span>
        </a>
        <a href="{root}izdelki/index.html" aria-label="Katalog izdelkov" title="Izdelki" class="relative inline-flex items-center gap-1.5 p-1.5 text-[13px] font-bold uppercase text-[#242424] transition hover:text-[#006AA9]">
          <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          <span class="hidden md:inline">Izdelki</span>
        </a>
        <button type="button" class="inline-flex h-10 w-10 items-center justify-center rounded-full text-[#242424] hover:bg-[#F2F2F2] lg:hidden" data-nav-toggle aria-expanded="false" aria-controls="mobile-nav">
          <span class="sr-only">Meni</span>
          <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
      </div>"""


def header(depth: int, current: str = "", is_home: bool | None = None) -> str:
    """Render Woodmart Header Electronics structure (topbar, main header, category + nav bar)."""
    root = _depth_prefix(depth)
    if is_home is None:
        is_home = current == "index.html"

    links = "".join(
        f'<a href="{root}{href}" class="nav-link px-4 font-sans text-[13px] font-bold uppercase tracking-wide"{_current_attr(href, current)}>{label}</a>'
        for href, label in NAV
    )
    mobile_nav = "".join(
        f'<a href="{root}{href}" class="block border-b border-[#E8E8E8] py-3 font-sans text-[13px] font-bold uppercase text-[#242424] hover:text-[#006AA9]"{_current_attr(href, current)}>{label}</a>'
        for href, label in NAV
    )
    mobile_cats = "".join(
        f'<a href="{root}izdelki/index.html?cat={quote(cat_slug)}" class="block py-1.5 text-sm text-body-text hover:text-[#006AA9]">{escape(label)}</a>'
        for label, cat_slug, _ in CATEGORY_MENU
    )

    return f"""  <header class="site-header relative z-40 bg-white">
{_render_topbar(root)}
    <div class="border-b border-[#E8E8E8] bg-white">
      <div class="container-site flex h-[76px] items-center justify-between gap-4 lg:h-[105px] lg:gap-8">
        <a href="{root}index.html" class="inline-flex shrink-0 items-center" aria-label="Dimet, domača stran">
          <img src="{root}images/dimet-logo.jpg" alt="Dimet" width="250" height="41" class="h-auto w-[179px] lg:w-[250px]">
        </a>
        <form action="{root}izdelki/index.html" method="get" role="search" class="relative hidden min-w-0 flex-1 md:flex md:max-w-xl">
          <label for="site-search" class="sr-only">Iskanje izdelkov</label>
          <input id="site-search" type="search" name="q" placeholder="Iskanje izdelkov..." class="pill-search">
          <button type="submit" aria-label="Išči" class="absolute right-1.5 top-1/2 inline-flex h-[36px] w-[36px] -translate-y-1/2 items-center justify-center rounded-full bg-[#007BC4] text-white transition hover:bg-[#006AA9]">
            <svg aria-hidden="true" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
          </button>
        </form>
{_render_header_actions(root)}
      </div>
    </div>
    <div class="hidden border-b border-[#E8E8E8] bg-white lg:block">
      <div class="container-site flex h-[52px] items-center gap-6">
        <div class="relative w-[300px] shrink-0" data-cat-menu data-default-open="{"true" if is_home else "false"}">
          <button type="button" class="category-box" aria-expanded="{"true" if is_home else "false"}">
            <span class="flex items-center gap-3">
              <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
              <span>Kategorije</span>
            </span>
            <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
          </button>
          {_category_flyout_items(root, is_home)}
        </div>
        <nav class="flex items-center" aria-label="Glavna navigacija">{links}</nav>
      </div>
    </div>
    <nav id="mobile-nav" class="hidden max-h-[calc(100vh-76px)] overflow-y-auto border-b border-[#E8E8E8] bg-white px-4 pb-5 pt-3 lg:hidden" aria-label="Mobilna navigacija">
      <form action="{root}izdelki/index.html" method="get" role="search" class="relative mb-3">
        <label for="mobile-search" class="sr-only">Iskanje izdelkov</label>
        <input id="mobile-search" type="search" name="q" placeholder="Iskanje izdelkov..." class="pill-search pr-12">
        <button type="submit" aria-label="Išči" class="absolute right-1.5 top-1/2 inline-flex h-[36px] w-[36px] -translate-y-1/2 items-center justify-center rounded-full bg-[#007BC4] text-white">
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
        </button>
      </form>
      <div>{mobile_nav}</div>
      <div class="mt-4">
        <p class="mb-2 font-heading text-xs font-semibold uppercase tracking-wider text-[#242424]">Kategorije</p>
        <div class="grid grid-cols-1 gap-0.5">{mobile_cats}</div>
      </div>
    </nav>
  </header>
"""


def footer(depth: int) -> str:
    """Render Woodmart footer-layout: 7 dark footer."""
    root = _depth_prefix(depth)
    info_html = "".join(
        f'<li><a class="footer-link" href="{root}{href}">{label}</a></li>'
        for href, label in FOOTER_INFO_LINKS
    )
    about_html = "".join(
        (
            f'<li><a class="footer-link" href="{href}" target="_blank" rel="noopener noreferrer">{label}</a></li>'
            if external
            else f'<li><a class="footer-link" href="{root}{href}">{label}</a></li>'
        )
        for href, label, external in FOOTER_ABOUT_LINKS
    )
    tel_href = f"tel:{PHONE.replace(' ', '')}"
    return f"""  <footer class="mt-16 bg-[#0A0A0A] py-12 text-gray-300">
    <div class="container-site">
      <div class="grid grid-cols-1 gap-8 md:grid-cols-12">
        <div class="md:col-span-6">
          <a href="{root}index.html" class="inline-block rounded bg-white p-2">
            <img src="{root}images/dimet-logo.jpg" alt="Dimet d.o.o." width="250" height="41" class="h-auto w-[200px]" loading="lazy">
          </a>
          <p class="mt-4 text-sm font-medium text-gray-200">Cene so v EUR in vključujejo DDV.</p>
          <ul class="mt-4 space-y-2 text-sm text-gray-300">
            <li>{ADDRESS}</li>
            <li><a class="footer-link" href="{tel_href}">{PHONE}</a></li>
            <li><a class="footer-link" href="mailto:{EMAIL}">{EMAIL}</a></li>
          </ul>
        </div>
        <div class="md:col-span-3">
          <h2 class="font-heading text-sm font-semibold uppercase tracking-wider text-white">SPLOŠNE INFORMACIJE</h2>
          <nav aria-label="Splošne informacije" class="mt-4">
            <ul class="space-y-1.5">{info_html}</ul>
          </nav>
        </div>
        <div class="md:col-span-3">
          <h2 class="font-heading text-sm font-semibold uppercase tracking-wider text-white">O NAS</h2>
          <nav aria-label="O nas" class="mt-4">
            <ul class="space-y-1.5">{about_html}</ul>
          </nav>
        </div>
      </div>
      <div class="mt-8 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-6 text-xs text-gray-400 sm:flex-row">
        <p>&copy; 2025 Dimet d.o.o. Vse pravice pridržane. Izdelava: Domen Skomina</p>
        <img src="{root}images/payments.png" alt="Načini plačila" width="255" height="22" class="h-[22px] w-auto" loading="lazy">
      </div>
    </div>
  </footer>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Organization","name":"Dimet d.o.o.","url":"{SITE_URL}","email":"{EMAIL}","telephone":"{PHONE}","address":{{"@type":"PostalAddress","streetAddress":"Jezerska cesta 65","postalCode":"4000","addressLocality":"Kranj","addressCountry":"SI"}}}}
  </script>
</body>
</html>
"""
