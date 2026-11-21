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
SEASONAL_SLUGS = (
    "13x1000-x-concar",
    "cev-za-bencin-3-5x9-5-10bar-1-8",
    "cev-za-vodo-fi-10x17-10-bar-rdeca",
)
SIDEBAR_SLUGS = (
    "samokolnica-6404",
    "profil-u-keder",
    "tesnilo-damper-20-klinasto",
    "pena-za-zvocno-izolacijo-3-cm-2000x1000",
)
TAB_LIMIT = 6
Product = dict


def esc(text: object) -> str:
    return escape(str(text if text is not None else ""), quote=True)


def format_price(price: str | float | int | None) -> str:
    if price is None or price == "":
        return ""
    try:
        return f"{float(price):.2f}".replace(".", ",") + " €"
    except (ValueError, TypeError):
        return ""


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
        self.categories: list[dict] = data.get("categories", [])
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

    def page(
        self,
        rel: str,
        title: str,
        desc: str,
        depth: int,
        body: str,
        og: str | None = None,
        is_home: bool = False,
    ) -> None:
        html = (
            head(title, desc, depth, rel, og)
            + header(depth, rel, is_home=is_home)
            + f'  <main id="main">\n{body}\n  </main>\n'
            + footer(depth)
        )
        self.write(rel, html)


def img_tag(rel: str | None, alt: str, depth: int, cls: str = "", eager: bool = False, extra_attrs: str = "") -> str:
    if not rel or not (ROOT / rel).is_file():
        return ""
    width, height = image_size(rel)
    extra = f" {extra_attrs}" if extra_attrs else ""
    return (f'<img src="{"../" * depth}{esc(rel)}" alt="{esc(alt)}" width="{width}" height="{height}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async" class="{cls}"{extra}>')


def mailto(title: str) -> str:
    return f"mailto:{EMAIL}?subject={quote(title)}"


def stock_badge(in_stock: bool) -> str:
    label = "Na zalogi" if in_stock else "Ni na zalogi"
    return f'<span class="badge">{label}</span>'


def _discount_pct(p: Product) -> int | None:
    reg = p.get("regular_price")
    sale = p.get("sale_price")
    if sale in (None, "") or reg in (None, ""):
        return None
    try:
        reg_f, sale_f = float(reg), float(sale)
    except (ValueError, TypeError):
        return None
    if reg_f <= sale_f or reg_f <= 0:
        return None
    return round((reg_f - sale_f) / reg_f * 100)


def _price_html(p: Product) -> str:
    unit = p.get("unit") or ""
    unit_html = f' <span class="text-xs text-[#595959]">{esc(unit)}</span>' if unit else ""
    pct = _discount_pct(p)
    if pct is not None:
        reg_str = format_price(p["regular_price"])
        sale_str = format_price(p["sale_price"])
        return (
            f'<p class="mt-1 flex flex-wrap items-baseline gap-1">'
            f'<span class="line-through text-[#595959] mr-2 text-sm">{reg_str}</span> '
            f'<span class="font-bold text-brand text-base">{sale_str}</span>'
            f'{unit_html}</p>'
        )
    price = format_price(p.get("price"))
    if price:
        return (
            f'<p class="mt-1 flex flex-wrap items-baseline gap-1">'
            f'<span class="font-bold text-heading-dark text-base">{price}</span>'
            f'{unit_html}</p>'
        )
    return '<p class="mt-1 text-sm text-[#595959]">Cena na povpraševanje</p>'


def product_card(p: Product, depth: int) -> str:
    root = "../" * depth
    raw_price = p.get("price")
    price_attr = esc(raw_price) if raw_price not in (None, "") else ""
    cats = p.get("categories") or []
    cat_slugs = ",".join(c["slug"] for c in cats if c.get("slug"))
    cat_names = ",".join(c["name"] for c in cats if c.get("name"))
    primary_cat = cats[0] if cats else None
    cat_link = (
        f'<p class="text-xs text-[#595959]"><a href="{root}izdelki/index.html?cat={esc(primary_cat["slug"])}" '
        f'class="transition hover:text-brand">{esc(primary_cat["name"])}</a></p>'
        if primary_cat else ""
    )

    badges: list[str] = []
    pct = _discount_pct(p)
    if pct is not None:
        badges.append(
            f'<span class="inline-flex items-center rounded-full bg-[#007BC4] px-2.5 py-0.5 font-heading text-xs font-semibold text-white">-{pct}%</span>'
        )
    if p.get("is_new"):
        badges.append(
            '<span class="inline-flex items-center rounded-full bg-[#FBBC34] px-2.5 py-0.5 font-heading text-xs font-semibold text-[#242424]">Novo</span>'
        )
    badges_html = (
        f'<div class="absolute left-3 top-3 z-10 flex flex-wrap gap-1.5">{"".join(badges)}</div>'
        if badges else ""
    )
    img_markup = img_tag(p.get("image"), p["title"], depth, "h-full w-full object-contain transition duration-300 group-hover:scale-105")
    if not img_markup:
        img_markup = f'<span class="flex h-full w-full items-center justify-center text-xs text-[#595959]">{esc(p["title"])}</span>'

    return f"""<article class="card group flex flex-col overflow-hidden p-0" data-product-card data-title="{esc(p['title'])}" data-price="{price_attr}" data-categories="{esc(cat_slugs)}" data-category-names="{esc(cat_names)}">
  <div class="relative aspect-square overflow-hidden border-b border-[#E8E8E8] bg-white p-4">
    {badges_html}
    <a href="{root}izdelki/{esc(p['slug'])}.html" class="block h-full w-full">{img_markup}</a>
  </div>
  <div class="flex flex-1 flex-col gap-1.5 p-4">
    <h3 class="font-heading text-sm font-medium leading-snug text-heading-dark sm:text-base"><a href="{root}izdelki/{esc(p['slug'])}.html" class="transition hover:text-brand">{esc(p['title'])}</a></h3>
    {cat_link}
    {_price_html(p)}
    <div class="mt-auto flex flex-wrap gap-2 pt-3">
      <a class="btn btn-ghost min-h-[38px] px-4 text-xs" href="{root}izdelki/{esc(p['slug'])}.html">Podrobnosti</a>
      <a class="btn-brand min-h-[38px] px-4 text-xs" href="{esc(mailto(p['title']))}">Povpraševanje</a>
    </div>
  </div>
</article>"""


def compact_product_row(p: Product) -> str:
    """Compact horizontal product row for the home sidebar 'Oglejte si tudi' widget."""
    href = f"izdelki/{esc(p['slug'])}.html"
    unit = p.get("unit") or ""
    unit_html = f' <span class="text-[11px] text-[#595959]">{esc(unit)}</span>' if unit else ""
    pct = _discount_pct(p)
    if pct is not None:
        price_str = (
            f'<span class="line-through text-[#595959] mr-1 text-xs">{format_price(p["regular_price"])}</span>'
            f'<span class="font-bold text-brand text-sm">{format_price(p["sale_price"])}</span>{unit_html}'
        )
    else:
        formatted = format_price(p.get("price"))
        price_str = (
            f'<span class="font-bold text-heading-dark text-sm">{formatted}</span>{unit_html}'
            if formatted
            else '<span class="text-xs text-[#595959]">Cena na povpraševanje</span>'
        )
    thumb = img_tag(p.get("image"), p["title"], 0, "h-full w-full object-contain") or f'<span class="sr-only">{esc(p["title"])}</span>'
    return (
        '<article class="flex items-center gap-3 py-2.5">'
        f'<a href="{href}" class="h-16 w-16 shrink-0 overflow-hidden border border-[#E8E8E8] bg-white p-1">{thumb}</a>'
        '<div class="min-w-0 flex-1">'
        f'<h4 class="line-clamp-2 font-heading text-xs font-medium leading-snug text-[#242424]"><a href="{href}" class="transition hover:text-[#006AA9]">{esc(p["title"])}</a></h4>'
        f'<p class="mt-1">{price_str}</p>'
        '</div>'
        '</article>'
    )


def _pick_products(by_slug: dict[str, Product], slugs: tuple[str, ...], fallback: list[Product], limit: int) -> list[Product]:
    picked = [by_slug[s] for s in slugs if s in by_slug]
    seen = {p["slug"] for p in picked}
    for p in fallback:
        if len(picked) >= limit:
            break
        if p["slug"] not in seen:
            picked.append(p)
            seen.add(p["slug"])
    return picked[:limit]


def build_home(site: Site) -> None:
    by_slug = {p["slug"]: p for p in site.products}
    in_stock = [p for p in site.products if p.get("in_stock")]

    seasonal = _pick_products(by_slug, SEASONAL_SLUGS, in_stock, 3)
    seasonal_cards = "".join(product_card(p, 0) for p in seasonal)

    sidebar_products = _pick_products(by_slug, SIDEBAR_SLUGS, in_stock, 4)
    sidebar_rows = "".join(compact_product_row(p) for p in sidebar_products)

    best_sellers = sorted(
        in_stock,
        key=lambda p: (int(p.get("total_sales") or 0), 1 if _discount_pct(p) is not None else 0),
        reverse=True,
    )[:TAB_LIMIT]

    new_first = [p for p in site.products if p.get("is_new")]
    new_tab = _pick_products(by_slug, tuple(p["slug"] for p in new_first), in_stock, TAB_LIMIT)

    sale_items = sorted(
        [p for p in site.products if _discount_pct(p) is not None],
        key=lambda p: _discount_pct(p) or 0,
        reverse=True,
    )[:TAB_LIMIT]

    tabs = [
        {
            "id": "najbolje-prodajano",
            "label": "NAJBOLJE PRODAJANO",
            "cards_html": "".join(product_card(p, 0) for p in best_sellers),
        },
        {
            "id": "novo",
            "label": "NOVO",
            "cards_html": "".join(product_card(p, 0) for p in new_tab),
        },
        {
            "id": "akcija",
            "label": "AKCIJA",
            "cards_html": "".join(product_card(p, 0) for p in sale_items),
        },
    ]

    body = home_body(seasonal_cards, sidebar_rows, tabs, site.posts)
    site.page(
        "index.html",
        "Dimet",
        "Industrijski materiali za vsak izziv: gume, cevi, pene, tesnila in trakovi.",
        0,
        body,
        is_home=True,
    )


def build_shop(site: Site) -> None:
    cards = "".join(product_card(p, 1) for p in site.products)
    site.page(
        "izdelki/index.html",
        "Izdelki",
        "Vsi izdelki Dimet: gume, cevi, pene, tesnila in trakovi.",
        1,
        shop_body(site.categories, cards),
    )


def build_product(site: Site, p: Product) -> None:
    desc_src = p["html"] or (f"<p>{esc(p['short'])}</p>" if p["short"] else "")
    desc = site.clean(desc_src, 1)
    unit = p.get("unit") or ""
    unit_html = f' <span class="text-sm font-normal text-[#595959]">/ {esc(unit)}</span>' if unit else ""
    pct = _discount_pct(p)
    if pct is not None:
        price_block = (
            f'<p class="mt-4 flex flex-wrap items-baseline gap-2">'
            f'<span class="text-lg text-[#595959] line-through">{format_price(p["regular_price"])}</span>'
            f'<span class="text-2xl font-bold text-brand">{format_price(p["sale_price"])}</span>'
            f'{unit_html}</p>'
        )
    else:
        price = format_price(p.get("price")) or "Cena na povpraševanje"
        price_block = f'<p class="mt-4 text-2xl font-bold">{price}{unit_html if p.get("price") else ""}</p>'

    all_images: list[str] = []
    for candidate in [p.get("image"), *(p.get("gallery") or [])]:
        if candidate and (ROOT / candidate).is_file() and candidate not in all_images:
            all_images.append(candidate)

    main_img_html = img_tag(p.get("image"), p["title"], 1, "w-full h-auto", eager=True, extra_attrs="data-product-main-img")
    gallery_html = ""
    if len(all_images) > 1:
        thumbs = []
        for idx, img_rel in enumerate(all_images, start=1):
            w, h = image_size(img_rel)
            active = idx == 1
            border_cls = "border-[#007BC4]" if active else "border-[#E8E8E8] hover:border-[#007BC4]"
            thumbs.append(
                f'<button type="button" data-gallery-thumb data-img-src="../{esc(img_rel)}" '
                f'data-img-width="{w}" data-img-height="{h}" '
                f'aria-label="Slika {idx} od {len(all_images)}" aria-pressed="{"true" if active else "false"}" '
                f'class="h-20 w-20 overflow-hidden rounded-lg border-2 bg-white p-1 transition {border_cls}">'
                f'{img_tag(img_rel, f"{p["title"]} - slika {idx}", 1, "h-full w-full object-contain")}'
                '</button>'
            )
        gallery_html = f'<div class="mt-3 flex flex-wrap gap-3" role="group" aria-label="Galerija slik izdelka">{"".join(thumbs)}</div>'

    attrs = p.get("attributes") or p.get("_product_attributes") or []
    attr_rows = "".join(
        f'<tr><th scope="row" class="w-1/2 border-b border-[#E8E8E8] bg-[#F2F2F2] px-3 py-2 text-left text-sm font-semibold text-[#242424]">{esc(a["name"])}</th>'
        f'<td class="border-b border-[#E8E8E8] px-3 py-2 text-sm text-[#4A4A4A]">{esc(a["value"])}</td></tr>'
        for a in attrs if a.get("name") and a.get("value") not in (None, "")
    )
    attrs_html = (
        f'<section class="mt-8" aria-label="Tehnične lastnosti">'
        f'<h2 class="h2-section text-lg">Tehnične lastnosti</h2>'
        f'<table class="mt-3 w-full border-collapse border border-[#E8E8E8] text-left text-sm"><tbody>{attr_rows}</tbody></table>'
        '</section>'
        if attr_rows else ""
    )

    body = f"""<div class="container-site section">
  <nav class="breadcrumb" aria-label="Drobtinice"><a href="../index.html">Domov</a> / <a href="index.html">Izdelki</a> / <span>{esc(p['title'])}</span></nav>
  <article class="mt-6 grid gap-8 md:grid-cols-2">
    <div>
      <div class="card overflow-hidden bg-white">{main_img_html}</div>
      {gallery_html}
    </div>
    <div>
      <h1 class="h1-display">{esc(p['title'])}</h1>
      {price_block}
      <p class="mt-2 text-sm">Šifra: {esc(p['sku'])}</p>
      <p class="mt-2">{stock_badge(p['in_stock'])}</p>
      <p class="mt-6"><a class="btn-brand" href="{esc(mailto(p['title']))}">Povpraševanje</a></p>
      <p class="mt-4"><a href="index.html">&larr; Nazaj na izdelke</a></p>
    </div>
  </article>
  {attrs_html}
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
    contact_form = f"""<form action="mailto:{EMAIL}" method="post" enctype="text/plain" data-contact-form class="mt-6 space-y-4 max-w-xl">
  <div>
    <label for="contact-name" class="block text-sm font-semibold text-[#242424]">Ime in priimek *</label>
    <input id="contact-name" name="name" type="text" required autocomplete="name" class="mt-1 w-full rounded-lg border border-[#E8E8E8] px-4 py-2.5 text-sm text-[#242424] focus:border-[#007BC4] focus:outline-none">
  </div>
  <div class="grid gap-4 sm:grid-cols-2">
    <div>
      <label for="contact-email" class="block text-sm font-semibold text-[#242424]">E-pošta *</label>
      <input id="contact-email" name="email" type="email" required autocomplete="email" class="mt-1 w-full rounded-lg border border-[#E8E8E8] px-4 py-2.5 text-sm text-[#242424] focus:border-[#007BC4] focus:outline-none">
    </div>
    <div>
      <label for="contact-phone" class="block text-sm font-semibold text-[#242424]">Telefon</label>
      <input id="contact-phone" name="phone" type="tel" autocomplete="tel" class="mt-1 w-full rounded-lg border border-[#E8E8E8] px-4 py-2.5 text-sm text-[#242424] focus:border-[#007BC4] focus:outline-none">
    </div>
  </div>
  <div>
    <label for="contact-message" class="block text-sm font-semibold text-[#242424]">Sporočilo *</label>
    <textarea id="contact-message" name="message" rows="5" required class="mt-1 w-full rounded-lg border border-[#E8E8E8] px-4 py-2.5 text-sm text-[#242424] focus:border-[#007BC4] focus:outline-none"></textarea>
  </div>
  <div>
    <button type="submit" class="btn-brand">Pošlji sporočilo</button>
  </div>
  <p data-contact-status role="status" aria-live="polite" class="text-sm font-medium text-[#006AA9]" hidden></p>
</form>"""
    block = f"""<div class="card mt-8 p-6"><h2 class="h2-section">Dimet d.o.o.</h2>
  <p class="mt-3">{esc(ADDRESS)}</p>
  <p>Telefon: <a href="tel:{PHONE.replace(' ', '')}">{esc(PHONE)}</a></p>
  <p>E-pošta: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <div class="mt-5 overflow-hidden rounded-xl border border-[#E8E8E8]">
    <iframe title="Zemljevid lokacije Dimet d.o.o., Jezerska cesta 65, 4000 Kranj" src="https://maps.google.com/maps?q=Jezerska%20cesta%2065%2C%204000%20Kranj&amp;t=&amp;z=15&amp;ie=UTF8&amp;iwloc=&amp;output=embed" width="100%" height="320" loading="lazy" referrerpolicy="no-referrer-when-downgrade" class="block w-full border-0"></iframe>
  </div></div>"""
    site.page("kontakt.html", contact["title"], "Kontaktni podatki podjetja Dimet d.o.o.", 0,
              article(contact["title"], site.clean(contact["html"], 0) + contact_form + block))
    for slug in INFO_SLUGS:
        page = get(slug)
        site.page(f"strani/{slug}.html", page["title"], page["title"], 1, article(page["title"], site.clean(page["html"], 1)))
    not_found = """<div class="container-site section text-center"><h1 class="h1-display">Strani ni mogoče najti</h1>
  <p class="lead mt-4">Žal te strani ne najdemo. Morda je bila premaknjena ali odstranjena.</p>
  <p class="mt-8"><a class="btn-brand" href="/index.html">Nazaj na domačo stran</a></p></div>"""
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
