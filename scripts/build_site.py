"""Build the static Dimet site from data/content.json into the project root."""
import json
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from layout import ADDRESS, EMAIL, PHONE, SITE_URL, footer, head, header  # noqa: E402
from home_sections import home_body, shop_body  # noqa: E402
from sanitize import clean_html  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
INFO_SLUGS = ("pogosta-vprasanja", "stroski-dostave", "nacin-placila", "vracilo-blaga",
              "pogoji-poslovanja", "politika-zasebnosti", "piskotki")
CATEGORIES = {
    "Gume": "guma",
    "Cevi": "cev",
    "Tesnila": "tesnil",
    "Pene": "pena",
    "Plošče": "plosc",
    "Palice": "palica",
    "Zračnice": "zracnic",
}
FEATURED_COUNT = 6
HERO_SLUG = "cev-za-vodo-fi-10x17-10-bar-rdeca"
Product = dict
Route = "callable"


def esc(text: object) -> str:
    return escape(str(text if text is not None else ""), quote=True)


def format_price(price: str | None) -> str:
    if not price:
        return ""
    return f"{float(price):.2f}".replace(".", ",") + " €"


def format_date(iso: str) -> str:
    year, month, day = iso.split("-")
    return f"{int(day):02d}. {int(month):02d}. {year}"


def image_size(rel: str) -> tuple[int, int]:
    from PIL import Image
    with Image.open(ROOT / rel) as img:
        return img.size


def make_router(products: set[str], posts: set[str], depth: int):
    prefix = "../" * depth

    def route(path: str) -> str:
        slug = path.strip("/").split("?")[0]
        if slug.startswith("izdelek/"):
            slug = slug[len("izdelek/"):]
        if slug in products:
            target = f"izdelki/{slug}.html"
        elif slug in posts:
            target = f"novice/{slug}.html"
        elif slug in INFO_SLUGS:
            target = f"strani/{slug}.html"
        elif slug in ("o-nas", "kontakt"):
            target = f"{slug}.html"
        elif slug == "novice":
            target = "novice/index.html"
        elif slug in ("trgovina", "izdelki"):
            target = "izdelki/index.html"
        else:
            target = "index.html"
        return prefix + target

    return route


class Site:
    def __init__(self, data: dict) -> None:
        self.products: list[Product] = data["products"]
        self.pages = {p["slug"]: p for p in data["pages"]}
        self.posts: list[dict] = data["posts"]
        self.known = {p.name for p in IMAGES.iterdir()} if IMAGES.is_dir() else set()
        self.product_slugs = {p["slug"] for p in self.products}
        self.post_slugs = {p["slug"] for p in self.posts}
        self.written: list[str] = []

    def clean(self, html: str, depth: int) -> str:
        route = make_router(self.product_slugs, self.post_slugs, depth)
        return clean_html(html, self.known, route, image_root="../" * depth)

    def write(self, rel: str, html: str) -> None:
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        self.written.append(rel)

    def page(self, rel: str, title: str, desc: str, depth: int, body: str, og: str | None = None) -> None:
        html = (head(title, desc, depth, rel, og) + header(depth)
                + f'  <main id="main">\n{body}\n  </main>\n' + footer(depth))
        self.write(rel, html)


def img_tag(rel: str | None, alt: str, depth: int, cls: str = "", eager: bool = False) -> str:
    if not rel or not (ROOT / rel).is_file():
        return ""
    width, height = image_size(rel)
    return (f'<img src="{"../" * depth}{esc(rel)}" alt="{esc(alt)}" width="{width}" height="{height}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async" class="{cls}">')


def mailto(title: str) -> str:
    return f"mailto:{EMAIL}?subject={quote(title)}"


def stock_badge(in_stock: bool) -> str:
    label = "Na zalogi" if in_stock else "Ni na zalogi"
    return f'<span class="badge">{label}</span>'


def product_card(p: Product, depth: int) -> str:
    root = "../" * depth
    price = format_price(p["price"])
    price_attr = esc(p["price"]) if p["price"] else ""
    price_html = f'<p class="text-lg font-bold">{price}</p>' if price else '<p class="text-sm">Cena na povpraševanje</p>'
    return f"""<article class="card flex flex-col overflow-hidden" data-product-card data-title="{esc(p['title'])}" data-price="{price_attr}">
  <a href="{root}izdelki/{esc(p['slug'])}.html" class="block aspect-square overflow-hidden bg-white">{img_tag(p['image'], p['title'], depth, 'h-full w-full object-contain')}</a>
  <div class="flex flex-1 flex-col gap-2 p-4">
    <h3 class="text-base font-semibold"><a href="{root}izdelki/{esc(p['slug'])}.html">{esc(p['title'])}</a></h3>
    {price_html}
    <p class="text-xs text-muted">Šifra: {esc(p['sku'])}</p>
    <p>{stock_badge(p['in_stock'])}</p>
    <div class="mt-auto flex flex-wrap gap-2 pt-2">
      <a class="btn btn-ghost" href="{root}izdelki/{esc(p['slug'])}.html">Podrobnosti</a>
      <a class="btn btn-secondary" href="{esc(mailto(p['title']))}">Povpraševanje</a>
    </div>
  </div>
</article>"""


def build_home(site: Site) -> None:
    featured = [p for p in site.products if p["in_stock"]][:FEATURED_COUNT]
    hero = next((p for p in site.products if p["slug"] == HERO_SLUG and p["image"]), None)
    if hero is None:
        raise ValueError(f"Hero product '{HERO_SLUG}' missing or has no image")
    hero_img = img_tag(hero["image"], hero["title"], 0, "h-auto w-full object-contain", eager=True)
    cards = "".join(product_card(p, 0) for p in featured)
    body = home_body(CATEGORIES, hero_img, cards)
    site.page("index.html", "Dimet", "Industrijski materiali za vsak izziv: gume, cevi, pene, tesnila in trakovi.", 0, body)


def build_shop(site: Site) -> None:
    cards = "".join(product_card(p, 1) for p in site.products)
    site.page("izdelki/index.html", "Izdelki", "Vsi izdelki Dimet: gume, cevi, pene, tesnila in trakovi.", 1,
              shop_body(CATEGORIES, cards))


def build_product(site: Site, p: Product) -> None:
    desc_src = p["html"] or (f"<p>{esc(p['short'])}</p>" if p["short"] else "")
    desc = site.clean(desc_src, 1)
    price = format_price(p["price"]) or "Cena na povpraševanje"
    body = f"""<div class="container-site section">
  <nav class="breadcrumb" aria-label="Drobtinice"><a href="../index.html">Domov</a> / <a href="index.html">Izdelki</a> / <span>{esc(p['title'])}</span></nav>
  <article class="mt-6 grid gap-8 md:grid-cols-2">
    <div class="card overflow-hidden bg-white">{img_tag(p['image'], p['title'], 1, 'w-full h-auto')}</div>
    <div>
      <h1 class="h1-display">{esc(p['title'])}</h1>
      <p class="mt-4 text-2xl font-bold">{price}</p>
      <p class="mt-2 text-sm">Šifra: {esc(p['sku'])}</p>
      <p class="mt-2">{stock_badge(p['in_stock'])}</p>
      <p class="mt-6"><a class="btn btn-primary" href="{esc(mailto(p['title']))}">Povpraševanje</a></p>
      <p class="mt-4"><a href="index.html">&larr; Nazaj na izdelke</a></p>
    </div>
  </article>
  <section class="prose-site mt-10" aria-label="Opis izdelka">{desc}</section>
</div>"""
    short = (p["short"] or p["title"])[:160]
    og = f"{SITE_URL}/{p['image']}" if p["image"] else None
    site.page(f"izdelki/{p['slug']}.html", p["title"], short, 1, body, og)


def article(title: str, inner: str, extra: str = "") -> str:
    return f"""<div class="container-site section"><article class="prose-site">
  <h1 class="h1-display">{esc(title)}</h1>{extra}
  {inner}
</article></div>"""


def build_news(site: Site) -> None:
    items = "".join(
        f'<article class="card p-6"><p class="text-sm"><time datetime="{esc(n["date"])}">{format_date(n["date"])}</time></p>'
        f'<h2 class="mt-1 text-xl font-semibold"><a href="{esc(n["slug"])}.html">{esc(n["title"])}</a></h2>'
        f'<p class="mt-2">{esc(n["excerpt"])}</p></article>' for n in site.posts)
    body = f'<div class="container-site section"><h1 class="h1-display">Novice</h1><div class="mt-8 grid gap-6 md:grid-cols-2">{items}</div></div>'
    site.page("novice/index.html", "Novice", "Novice in nasveti podjetja Dimet.", 1, body)
    for n in site.posts:
        date = f'<p class="mt-2 text-sm"><time datetime="{esc(n["date"])}">{format_date(n["date"])}</time></p>'
        inner = article(n["title"], site.clean(n["html"], 1), date)
        inner += '<p class="container-site"><a href="index.html">&larr; Vse novice</a></p>'
        site.page(f"novice/{n['slug']}.html", n["title"], (n["excerpt"] or n["title"])[:160], 1, inner)


def build_pages(site: Site) -> None:
    def get(slug: str) -> dict:
        if slug not in site.pages:
            raise KeyError(f"Page '{slug}' missing from content.json")
        return site.pages[slug]

    about = get("o-nas")
    site.page("o-nas.html", about["title"], "O podjetju Dimet d.o.o.", 0, article(about["title"], site.clean(about["html"], 0)))
    contact = get("kontakt")
    block = f"""<div class="card mt-8 p-6 not-prose"><h2 class="h2-section">Dimet d.o.o.</h2>
  <p class="mt-3">{esc(ADDRESS)}</p>
  <p>Telefon: <a href="tel:{PHONE.replace(' ', '')}">{esc(PHONE)}</a></p>
  <p>E-pošta: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>"""
    site.page("kontakt.html", contact["title"], "Kontaktni podatki podjetja Dimet d.o.o.", 0,
              article(contact["title"], site.clean(contact["html"], 0) + block))
    for slug in INFO_SLUGS:
        page = get(slug)
        site.page(f"strani/{slug}.html", page["title"], page["title"], 1, article(page["title"], site.clean(page["html"], 1)))
    not_found = """<div class="container-site section text-center"><h1 class="h1-display">Strani ni mogoče najti</h1>
  <p class="lead mt-4">Žal te strani ne najdemo. Morda je bila premaknjena ali odstranjena.</p>
  <p class="mt-8"><a class="btn btn-primary" href="/index.html">Nazaj na domačo stran</a></p></div>"""
    site.page("404.html", "Stran ni najdena", "Stran ni najdena.", 0, not_found)
    # Hosts serve 404.html for deep URLs; a root base keeps css, js and nav links working.
    not_found_path = ROOT / "404.html"
    not_found_path.write_text(
        not_found_path.read_text(encoding="utf-8").replace("<head>", '<head>\n  <base href="/">', 1),
        encoding="utf-8",
    )


def build_seo(site: Site) -> None:
    urls = [r for r in site.written if r != "404.html"]
    entries = "".join(f"  <url><loc>{SITE_URL}/{'' if r == 'index.html' else r}</loc></url>\n" for r in sorted(urls))
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")


def main() -> None:
    content = ROOT / "data" / "content.json"
    if not content.is_file():
        raise FileNotFoundError(f"Missing {content}")
    site = Site(json.loads(content.read_text(encoding="utf-8")))
    build_home(site)
    build_shop(site)
    for product in site.products:
        build_product(site, product)
    build_news(site)
    build_pages(site)
    build_seo(site)


if __name__ == "__main__":
    main()
