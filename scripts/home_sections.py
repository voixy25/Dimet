"""HTML section builders for the home and shop pages."""
from html import escape
from urllib.parse import quote

from layout import ADDRESS, EMAIL, PHONE, category_sidebar

HERO_TITLE = "Industrijski materiali za vsak izziv"
HERO_LEAD = ("Tehnične gume, cevi, pene, tesnila in trakovi za industrijo, obrt in delavnice. "
             "Zanesljiva kakovost, hitra dostava in nasvet strokovnjaka.")


def _tel(phone: str) -> str:
    return phone.replace(" ", "")


def hero_panel(hero_img: str) -> str:
    return f"""<div class="hero-panel flex flex-col items-center gap-6 p-8 text-white md:flex-row md:justify-between">
    <div class="max-w-md">
      <h1 class="h1-display text-white">{HERO_TITLE}</h1>
      <p class="lead mt-4 text-white">{HERO_LEAD}</p>
      <div class="mt-8 flex flex-wrap gap-3"><a class="btn btn-brand" href="izdelki/">Oglejte si izdelke</a><a class="btn border border-white text-white hover:bg-white hover:text-ink" href="kontakt.html">Kontaktirajte nas</a></div>
    </div>
    <div class="w-48 shrink-0 md:w-64">{hero_img}</div>
  </div>"""


def promo_tiles() -> str:
    def tile(title: str, copy: str, term: str, tone: str, btn: str) -> str:
        return f"""<div class="promo-tile {tone} p-8">
    <h2 class="text-2xl font-bold uppercase">{title}</h2>
    <p class="mt-3">{copy}</p>
    <p class="mt-6"><a class="btn {btn}" href="izdelki/?q={quote(term)}">Ogled ponudbe</a></p>
  </div>"""
    return f"""<section class="mt-8" aria-label="Priporočena ponudba"><div class="grid gap-6 md:grid-cols-2">
  {tile("Zračnice", "Vzdržljive, elastične, popolno prileganje.", "zracnic", "bg-grey text-ink", "btn-brand")}
  {tile("Tesnila", "Tesnila za industrijo, obrt in delavnice.", "tesnil", "bg-brand text-white", "bg-white text-ink hover:bg-grey")}
</div></section>"""


def home_body(categories: dict[str, str], hero_img: str, cards: str) -> str:
    return f"""<div class="container-site section">
<div class="grid gap-8 lg:grid-cols-[280px_1fr]">
  {category_sidebar(0, categories)}
  {hero_panel(hero_img)}
</div>
{promo_tiles()}
</div>
<section class="section" aria-labelledby="izpostavljeno"><div class="container-site">
  <h2 class="section-title" id="izpostavljeno">Izpostavljeni izdelki</h2>
  <div class="grid-products mt-8">{cards}</div>
  <p class="mt-6 text-center"><a class="btn btn-brand" href="izdelki/">Vsi izdelki</a></p>
</div></section>
<section class="section bg-grey" aria-labelledby="o-podjetju"><div class="container-site">
  <h2 class="section-title" id="o-podjetju">O podjetju Dimet</h2>
  <p class="lead mt-6 max-w-2xl text-ink">Dimet d.o.o. že vrsto let oskrbuje industrijo in obrtnike z izbranimi tehničnimi materiali.</p>
  <p class="mt-4"><a class="btn btn-brand" href="o-nas.html">Več o nas</a></p>
</div></section>
<section class="section" aria-labelledby="kontakt"><div class="container-site card p-6">
  <h2 class="h2-section" id="kontakt">Kontakt</h2>
  <p class="mt-3 text-muted">{escape(ADDRESS)}</p>
  <p class="mt-1"><a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="tel:{_tel(PHONE)}">{escape(PHONE)}</a></p>
</div></section>"""


def shop_body(categories: dict[str, str], cards: str) -> str:
    return f"""<div class="container-site section">
<div class="grid gap-8 lg:grid-cols-[280px_1fr]">
  {category_sidebar(1, categories)}
  <div>
  <h1 class="h1-display text-ink">Izdelki</h1>
  <h2 class="sr-only">Seznam izdelkov</h2>
  <div class="mt-6 flex flex-col gap-3 sm:flex-row">
    <label class="sr-only" for="product-search">Iskanje izdelkov</label>
    <input id="product-search" type="search" placeholder="Poiščite izdelek" class="w-full rounded border border-line px-3 py-2 sm:max-w-sm" data-product-search>
    <label class="sr-only" for="product-sort">Razvrsti</label>
    <select id="product-sort" class="rounded border border-line px-3 py-2" data-product-sort>
      <option value="name">Ime A-Z</option>
      <option value="price-asc">Cena: nizka proti visoki</option>
      <option value="price-desc">Cena: visoka proti nizki</option>
    </select>
  </div>
  <div class="grid-products mt-8" data-product-grid>{cards}</div>
  <p id="no-results" class="mt-8" hidden>Ni izdelkov, ki bi ustrezali iskanju.</p>
  </div>
</div>
</div>"""
