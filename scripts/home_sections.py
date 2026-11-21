"""HTML section builders for the home and shop pages."""
from html import escape
from pathlib import Path
from urllib.parse import quote

_ROOT = Path(__file__).resolve().parent.parent


def _img_dims(rel: str) -> tuple[int, int] | None:
    path = _ROOT / rel
    if not path.is_file():
        return None
    from PIL import Image
    with Image.open(path) as img:
        return img.size


HERO_SLIDES = [
    {
        "bg": "bg-[#000000]",
        "text": "text-white",
        "eyebrow_cls": "text-[#4DB8FF]",
        "lead": "text-gray-300",
        "eyebrow": "ZMOGLJIVOST",
        "title": "PNEVMATIKE",
        "copy": "Vrhunske pnevmatike za motorje, kolesa, go-karte in industrijske vozičke z zanesljivim oprijemom.",
        "href": "izdelki/index.html?cat=pnevmatike",
        "btn_cls": "btn-brand",
        "image": "images/pnevmatika_velika-2-1.webp",
        "width": 848,
        "height": 824,
        "alt": "Pnevmatika",
        "is_h1": True,
    },
    {
        "bg": "bg-[#F2F2F2]",
        "text": "text-[#242424]",
        "eyebrow_cls": "text-[#006AA9]",
        "lead": "text-[#4A4A4A]",
        "eyebrow": "KAKOVOST",
        "title": "GUMIJASTE CEVI",
        "copy": "Trpežne industrijske cevi za vodo, zrak, goriva in zahtevne delovne pogoje.",
        "href": "izdelki/index.html?cat=cevi",
        "btn_cls": "btn-brand",
        "image": "images/cev_velika.png",
        "width": 652,
        "height": 700,
        "alt": "Gumijasta cev",
        "is_h1": False,
    },
    {
        "bg": "bg-[#F2F2F2]",
        "text": "text-[#242424]",
        "eyebrow_cls": "text-[#006AA9]",
        "lead": "text-[#4A4A4A]",
        "eyebrow": "VZDRŽLJIVOST",
        "title": "VARJENE SAMOKOLNICE",
        "copy": "Robustne slovenske samokolnice z varjenim ogrodjem za gradbišče, delavnico in vrt.",
        "href": "izdelki/index.html?cat=samokolnice",
        "btn_cls": "btn-brand",
        "image": "images/samokolnica_velika.png",
        "width": 1100,
        "height": 629,
        "alt": "Varjena samokolnica Dimet",
        "is_h1": False,
    },
]


def _render_hero_slide(slide: dict, index: int) -> str:
    is_active = index == 0
    state_cls = "relative z-10 opacity-100" if is_active else "pointer-events-none absolute inset-0 z-0 opacity-0"
    inert_attr = "" if is_active else " inert"
    tab_attr = "" if is_active else ' tabindex="-1"'
    tag = "h1" if slide["is_h1"] else "h2"
    eager = 'loading="eager"' if is_active else 'loading="lazy"'
    return (
        f'<article class="flex min-h-[420px] flex-col justify-between gap-6 px-14 py-8 transition-opacity duration-500 '
        f'sm:p-12 md:flex-row md:items-center lg:min-h-[470px] {slide["bg"]} {slide["text"]} {state_cls}" '
        f'data-hero-slide="{index}" aria-hidden="{"false" if is_active else "true"}"{inert_attr}>'
        '<div class="relative z-10 max-w-md">'
        f'<p class="font-accent text-xs font-bold uppercase tracking-[0.18em] {slide["eyebrow_cls"]}">{escape(slide["eyebrow"])}</p>'
        f'<{tag} class="mt-3 font-heading text-3xl font-bold uppercase leading-[1.1] tracking-tight sm:text-4xl lg:text-[42px] {slide["text"]}">{escape(slide["title"])}</{tag}>'
        f'<p class="mt-4 text-sm leading-relaxed sm:text-base {slide["lead"]}">{escape(slide["copy"])}</p>'
        f'<p class="mt-7"><a href="{escape(slide["href"])}"{tab_attr} class="{slide["btn_cls"]} px-7 uppercase tracking-wide">OGLED PONUDBE</a></p>'
        '</div>'
        '<div class="relative z-10 flex shrink-0 items-center justify-center md:w-[46%]">'
        f'<img src="{escape(slide["image"])}" alt="{escape(slide["alt"])}" width="{slide["width"]}" height="{slide["height"]}" {eager} decoding="async" '
        'class="h-auto max-h-[260px] w-auto object-contain sm:max-h-[320px] lg:max-h-[370px]">'
        '</div>'
        '</article>'
    )


def hero_section() -> str:
    """Hero 3-slide carousel positioned beside the open 300px Kategorije menu on lg+."""
    slides_html = "".join(_render_hero_slide(s, i) for i, s in enumerate(HERO_SLIDES))
    dots_html = "".join(
        f'<button type="button" data-hero-dot="{i}" aria-label="Diapozitiv {i + 1}" '
        f'aria-pressed="{"true" if i == 0 else "false"}" '
        'class="inline-flex min-h-[24px] min-w-[24px] items-center justify-center rounded-full p-1 transition">'
        f'<span data-hero-dot-pill class="block h-2.5 rounded-full transition-all {"w-6 bg-[#007BC4]" if i == 0 else "w-2.5 bg-gray-500/80 hover:bg-[#007BC4]/70"}"></span>'
        '</button>'
        for i in range(len(HERO_SLIDES))
    )
    return f"""<section class="container-site pt-4 lg:pt-5" aria-label="Glavni drsnik">
  <div class="lg:grid lg:grid-cols-[300px_1fr] lg:gap-6">
    <div class="hidden lg:block" aria-hidden="true"></div>
    <div class="relative overflow-hidden border border-[#E8E8E8] bg-[#000000]" data-hero-carousel aria-roledescription="carousel" aria-label="Glavni drsnik">
      <div class="relative">{slides_html}</div>
      <button type="button" data-hero-prev aria-label="Prejšnji diapozitiv" class="absolute left-2.5 top-1/2 z-20 inline-flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 text-[#242424] shadow-md transition hover:bg-[#007BC4] hover:text-white sm:left-3">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
      </button>
      <button type="button" data-hero-next aria-label="Naslednji diapozitiv" class="absolute right-2.5 top-1/2 z-20 inline-flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 text-[#242424] shadow-md transition hover:bg-[#007BC4] hover:text-white sm:right-3">
        <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
      </button>
      <div class="absolute bottom-3 left-1/2 z-20 flex -translate-x-1/2 items-center gap-1 rounded-full bg-white/90 px-2.5 py-0.5 shadow-sm backdrop-blur-sm">
        {dots_html}
      </div>
    </div>
  </div>
</section>"""


def promo_banners() -> str:
    """2-column promo banners (290px height, 30px gap)."""
    banners = [
        {
            "image": "images/zracnica-trak.png",
            "width": 700,
            "height": 350,
            "alt": "Zračnice",
            "title": "ZRAČNICE",
            "copy": "Vzdržljive, elastične, popolno prileganje.",
            "href": "izdelki/index.html?cat=zracnice",
            "dark": False,
        },
        {
            "image": "images/scitnik-trak.png",
            "width": 700,
            "height": 350,
            "alt": "Ščitniki",
            "title": "ŠČITNIKI",
            "copy": "Zanesljiva zaščita platišč in zračnic v vseh pogojih.",
            "href": "izdelki/index.html?cat=scitniki",
            "dark": True,
        },
    ]
    cards = []
    for b in banners:
        if b["dark"]:
            overlay = '<div class="absolute inset-0 bg-gradient-to-r from-[#005B94]/85 via-[#005B94]/45 to-transparent" aria-hidden="true"></div>'
            title_cls = "text-white"
            copy_cls = "text-white/95"
            btn_cls = "btn bg-white text-[#242424] hover:bg-[#F2F2F2]"
        else:
            overlay = '<div class="absolute inset-0 bg-gradient-to-r from-[#F2F2F2]/95 via-[#F2F2F2]/80 to-transparent" aria-hidden="true"></div>'
            title_cls = "text-[#242424]"
            copy_cls = "text-[#4A4A4A]"
            btn_cls = "btn-brand"
        cards.append(
            f'<div class="group relative flex min-h-[260px] items-center overflow-hidden border border-[#E8E8E8] sm:h-[290px]">'
            f'<img src="{escape(b["image"])}" alt="{escape(b["alt"])}" width="{b["width"]}" height="{b["height"]}" loading="lazy" decoding="async" '
            'class="absolute inset-0 h-full w-full object-cover object-right transition duration-500 group-hover:scale-105">'
            f'{overlay}'
            '<div class="relative z-10 max-w-[85%] p-6 sm:max-w-[65%] sm:p-9">'
            f'<h2 class="mt-2 font-heading text-2xl font-bold uppercase sm:text-[28px] {title_cls}">{escape(b["title"])}</h2>'
            f'<p class="mt-2 text-sm leading-relaxed {copy_cls}">{escape(b["copy"])}</p>'
            f'<p class="mt-5"><a href="{escape(b["href"])}" class="{btn_cls} uppercase tracking-wide">OGLED PONUDBE</a></p>'
            '</div>'
            '</div>'
        )
    return f"""<section class="container-site mt-[30px]" aria-label="Priporočena ponudba">
  <div class="grid gap-[30px] md:grid-cols-2">{"".join(cards)}</div>
</section>"""


def seasonal_band(cards_html: str) -> str:
    """Full-bleed seasonal products band with bg-dimet.png."""
    return f"""<section class="mt-14 bg-[#F2F2F2] bg-cover bg-center py-14 sm:py-16" style="background-image: url('images/bg-dimet.png');" aria-labelledby="sezonsko-naslov">
  <div class="container-site">
    <h2 id="sezonsko-naslov" class="section-title uppercase">SEZONSKO AKTUALNI ARTIKLI</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{cards_html}</div>
    <p class="mt-10 text-center">
      <a href="izdelki/index.html" class="btn-brand px-9 py-3 text-sm font-semibold uppercase tracking-wider">VEČ ARTIKLOV</a>
    </p>
  </div>
</section>"""


def wheelbarrow_showcase() -> str:
    """Feature showcase banner: DIMET VARJENA SAMOKOLNICA 80L."""
    return """<section class="relative overflow-hidden bg-[#242424] bg-cover bg-center text-white" style="background-image: url('images/dimet-samokolnica.png');" aria-labelledby="showcase-samokolnica">
  <div class="absolute inset-0 bg-gradient-to-r from-[#141414]/85 via-[#141414]/70 to-[#141414]/45" aria-hidden="true"></div>
  <div class="container-site relative z-10 py-12 lg:py-14">
    <div class="grid items-center gap-8 lg:grid-cols-12">
      <div class="lg:col-span-6">
        <h2 id="showcase-samokolnica" class="mt-3 font-heading text-2xl font-bold uppercase leading-tight text-white sm:text-3xl lg:text-4xl">DIMET VARJENA SAMOKOLNICA 80L</h2>
        <p class="mt-3 max-w-lg text-sm leading-relaxed text-gray-200 sm:text-base">Trpežno varjeno ogrodje, pocinkana 80-litrska posoda in kakovostna izdelava za dolgoletno uporabo na gradbišču in okoli hiše.</p>
        <div class="mt-7 flex flex-wrap gap-3">
          <a href="izdelki/samokolnica-dmt-80-l-varjena.html" class="btn-brand px-7 uppercase tracking-wide">NAKUP ZDAJ</a>
          <a href="izdelki/index.html?cat=samokolnice" class="btn bg-white px-7 uppercase tracking-wide text-[#242424] hover:bg-[#F2F2F2]">OGLED PONUDBE</a>
        </div>
      </div>
      <div class="flex items-center justify-center lg:col-span-6">
        <img src="images/samokolnica-1.png" alt="Dimet varjena samokolnica 80L" width="703" height="268" loading="lazy" decoding="async" class="h-auto max-h-[268px] w-auto object-contain drop-shadow-2xl">
      </div>
    </div>
  </div>
</section>"""


def split_featured_section(sidebar_rows_html: str, tabs: list[dict]) -> str:
    """25% / 75% split section: main tabbed product grids first in DOM, sidebar visually left on lg+."""
    tab_buttons = []
    tab_panels = []
    for idx, tab in enumerate(tabs):
        is_first = idx == 0
        btn_cls = (
            "border-[#007BC4] text-[#007BC4]"
            if is_first
            else "border-transparent text-[#595959] hover:text-[#242424]"
        )
        tab_buttons.append(
            f'<button type="button" role="tab" id="tab-{escape(tab["id"])}" '
            f'aria-controls="panel-{escape(tab["id"])}" aria-selected="{"true" if is_first else "false"}" '
            f'tabindex="{"0" if is_first else "-1"}" data-tab-target="{escape(tab["id"])}" '
            f'class="border-b-2 pb-2 font-heading text-xs font-semibold uppercase tracking-wide transition sm:text-sm {btn_cls}">'
            f'{escape(tab["label"])}</button>'
        )
        hidden_cls = "" if is_first else "hidden"
        tab_panels.append(
            f'<div role="tabpanel" id="panel-{escape(tab["id"])}" aria-labelledby="tab-{escape(tab["id"])}" '
            f'data-tab-panel="{escape(tab["id"])}" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 {hidden_cls}">'
            f'{tab["cards_html"]}</div>'
        )

    return f"""<section class="container-site section" aria-labelledby="izpostavljeni-naslov">
  <div class="grid gap-8 lg:grid-cols-12">
    <div class="lg:col-span-9" data-tabs-container>
      <div class="mb-7 flex flex-col gap-4 border-b border-[#E8E8E8] sm:flex-row sm:items-end sm:justify-between">
        <h2 id="izpostavljeni-naslov" class="relative -mb-px border-b-2 border-[#007BC4] pb-3 font-heading text-xl font-semibold uppercase text-[#242424] sm:text-2xl">IZPOSTAVLJENI ARTIKLI</h2>
        <div class="flex flex-wrap gap-5" role="tablist" aria-label="Kategorije izpostavljenih izdelkov">
          {"".join(tab_buttons)}
        </div>
      </div>
      {"".join(tab_panels)}
    </div>

    <aside class="hidden lg:order-first lg:col-span-3 lg:flex lg:flex-col lg:gap-8" aria-label="Priporočene kategorije in izdelki">
      <div class="group relative flex min-h-[340px] flex-col justify-start overflow-hidden border border-[#E8E8E8] p-6 text-white">
        <img src="images/profil-trak.png" alt="Gumeni profili" width="400" height="500" loading="lazy" decoding="async" class="absolute inset-0 h-full w-full object-cover transition duration-500 group-hover:scale-105">
        <div class="absolute inset-0 bg-gradient-to-b from-[#005B94]/85 via-[#005B94]/45 to-transparent" aria-hidden="true"></div>
        <div class="relative z-10">
          <h3 class="mt-2 font-heading text-2xl font-bold uppercase leading-tight text-white">GUMENI PROFILI</h3>
          <p class="mt-5"><a href="izdelki/index.html?cat=profili" class="btn bg-white px-5 py-2 text-xs font-semibold uppercase tracking-wide text-[#242424] hover:bg-[#F2F2F2]">OGLED PONUDBE</a></p>
        </div>
      </div>

      <div class="border-[3px] border-[#007BC4] bg-white">
        <h3 class="bg-[#007BC4] px-4 py-3 font-heading text-sm font-semibold uppercase tracking-wide text-white">OGLEJTE SI TUDI</h3>
        <div class="divide-y divide-[#E8E8E8] p-3">{sidebar_rows_html}</div>
      </div>
    </aside>
  </div>
</section>"""


def news_section(posts: list[dict]) -> str:
    """Blog / News section: AKTUALNE NOVICE with 3 cards."""
    cards = []
    for post in posts[:3]:
        date_parts = str(post.get("date_formatted") or "").split()
        day = date_parts[0] if len(date_parts) > 0 else ""
        month = date_parts[1] if len(date_parts) > 1 else ""
        img_src = post.get("featured_image") or "images/o-nas.png"
        dims = _img_dims(img_src)
        dim_attrs = f' width="{dims[0]}" height="{dims[1]}"' if dims else ""
        href = post.get("link") or f"novice/{post['slug']}.html"
        cat_name = post.get("category") or "Novice"
        badge_html = (
            f'<div class="absolute left-3 top-3 z-10 flex flex-col items-center bg-white px-2.5 py-1.5 text-center shadow">'
            f'<span class="font-heading text-base font-bold leading-none text-[#242424]">{escape(day)}</span>'
            f'<span class="mt-0.5 text-[11px] font-bold uppercase tracking-wide text-[#595959]">{escape(month)}</span>'
            '</div>'
        ) if day else ""
        cards.append(
            '<article class="group flex flex-col overflow-hidden border border-[#E8E8E8] bg-white transition hover:shadow-md">'
            f'<div class="relative aspect-[16/10] overflow-hidden bg-[#F2F2F2]">'
            f'<a href="{escape(href)}" class="block h-full w-full">'
            f'<img src="{escape(img_src)}" alt="{escape(post["title"])}"{dim_attrs} loading="lazy" decoding="async" class="h-full w-full object-cover transition duration-500 group-hover:scale-105">'
            '</a>'
            f'{badge_html}'
            f'<span class="absolute bottom-0 left-4 z-10 bg-[#007BC4] px-3 py-1 font-heading text-[11px] font-semibold uppercase tracking-wide text-white">{escape(cat_name)}</span>'
            '</div>'
            '<div class="flex flex-1 flex-col p-6">'
            f'<h3 class="font-heading text-lg font-semibold leading-snug text-[#242424]"><a href="{escape(href)}" class="transition hover:text-[#006AA9]">{escape(post["title"])}</a></h3>'
            f'<p class="mt-3 line-clamp-3 text-sm leading-relaxed text-[#595959]">{escape(post.get("excerpt") or "")}</p>'
            f'<p class="mt-auto pt-4"><a href="{escape(href)}" class="inline-flex items-center gap-1.5 font-heading text-xs font-semibold uppercase tracking-wide text-[#007BC4] transition hover:text-[#006AA9]">Nadaljuj z branjem <span aria-hidden="true">&rarr;</span></a></p>'
            '</div>'
            '</article>'
        )

    return f"""<section class="container-site pb-12 sm:pb-16" aria-labelledby="novice-naslov">
  <h2 id="novice-naslov" class="section-title uppercase">AKTUALNE NOVICE</h2>
  <div class="grid gap-6 md:grid-cols-3">{"".join(cards)}</div>
</section>"""


def newsletter_section() -> str:
    """Newsletter section (MailPoet style 2-column form)."""
    return """<section class="border-t border-[#E8E8E8] bg-[#F2F2F2] py-12" aria-labelledby="newsletter-naslov">
  <div class="container-site">
    <div class="grid items-center gap-6 lg:grid-cols-12 lg:gap-10">
      <div class="lg:col-span-6">
        <h2 id="newsletter-naslov" class="font-heading text-xl font-bold leading-snug text-[#242424] sm:text-2xl">Prijavite se na naše e-novice in bodite med prvimi obveščeni glede popustov in novosti!</h2>
        <p class="mt-2 text-xs text-[#555555]">S prijavo se strinjate s pogoji in <a href="strani/politika-zasebnosti.html" class="font-semibold text-[#006AA9] underline hover:text-[#005587]">politiko zasebnosti</a>.</p>
      </div>
      <div class="lg:col-span-6">
        <form data-newsletter-form class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <label for="newsletter-email" class="sr-only">E-poštni naslov</label>
          <input id="newsletter-email" type="email" required placeholder="Vaš e-poštni naslov" class="h-[46px] w-full flex-1 rounded-full border border-[#E8E8E8] bg-white px-5 text-sm text-[#242424] placeholder:text-[#595959] focus:border-[#007BC4] focus:outline-none">
          <button type="submit" class="inline-flex h-[46px] shrink-0 items-center justify-center rounded-full bg-[#007BC4] px-8 font-heading text-sm font-semibold text-white transition hover:bg-[#006AA9]">Pošljite</button>
        </form>
        <p data-newsletter-status role="status" aria-live="polite" class="mt-2 text-sm font-medium text-[#006AA9]" hidden></p>
      </div>
    </div>
  </div>
</section>"""


def home_body(seasonal_cards: str, sidebar_rows: str, tabs: list[dict], posts: list[dict]) -> str:
    """Compose all 7 Woodmart homepage sections in exact order."""
    return "\n".join([
        hero_section(),
        promo_banners(),
        seasonal_band(seasonal_cards),
        wheelbarrow_showcase(),
        split_featured_section(sidebar_rows, tabs),
        news_section(posts),
        newsletter_section(),
    ])


def _shop_category_sidebar(categories: list[dict]) -> str:
    """Render full parent + subcategory filter sidebar for izdelki/index.html."""
    items: list[str] = [
        '<li><a href="index.html" data-cat-filter="" data-base-color="text-[#242424]" class="flex items-center justify-between px-5 py-2.5 text-[13px] font-semibold text-[#242424] transition hover:bg-[#F2F2F2] hover:text-[#006AA9]"><span>Vsi izdelki</span></a></li>'
    ]
    for cat in categories:
        subs = cat.get("subcategories") or []
        sub_html = ""
        if subs:
            sub_links = "".join(
                f'<li><a href="index.html?cat={quote(sub["slug"])}" data-cat-filter="{escape(sub["slug"])}" data-base-color="text-[#555555]" '
                'class="flex items-center justify-between py-1.5 pl-8 pr-4 text-xs text-[#555555] transition hover:text-[#006AA9]">'
                f'<span>{escape(sub["name"])}</span><span>({sub.get("count", 0)})</span></a></li>'
                for sub in subs
            )
            sub_html = f'<ul class="border-t border-[#E8E8E8] bg-[#FAFAFA] py-1.5">{sub_links}</ul>'
        items.append(
            '<li class="border-t border-[#E8E8E8]">'
            f'<a href="index.html?cat={quote(cat["slug"])}" data-cat-filter="{escape(cat["slug"])}" data-base-color="text-[#242424]" '
            'class="flex items-center justify-between px-5 py-2.5 text-[13px] text-[#242424] transition hover:bg-[#F2F2F2] hover:text-[#006AA9]">'
            f'<span>{escape(cat["name"])}</span><span class="text-xs text-[#595959]">({cat.get("count", 0)})</span></a>'
            f'{sub_html}</li>'
        )
    return (
        '<aside aria-label="Filter kategorij" class="hidden lg:block">'
        '<p class="category-box">Kategorije</p>'
        f'<ul class="border border-t-0 border-[#E8E8E8] bg-white">{"".join(items)}</ul>'
        '</aside>'
    )


def _shop_category_chips(categories: list[dict]) -> str:
    """Render responsive category filter chips (including subcategories) above product grid."""
    chips = [
        '<a href="index.html" data-cat-filter="" data-base-color="text-title-dark" class="chip text-xs">Vsi izdelki</a>'
    ]
    for cat in categories:
        chips.append(
            f'<a href="index.html?cat={quote(cat["slug"])}" data-cat-filter="{escape(cat["slug"])}" data-base-color="text-title-dark" class="chip text-xs">{escape(cat["name"])}</a>'
        )
        for sub in cat.get("subcategories") or []:
            chips.append(
                f'<a href="index.html?cat={quote(sub["slug"])}" data-cat-filter="{escape(sub["slug"])}" data-base-color="text-title-dark" class="chip text-xs bg-[#FAFAFA]">{escape(cat["name"])}: {escape(sub["name"])}</a>'
            )
    return f'<div class="mt-5 flex flex-wrap gap-2 lg:hidden" aria-label="Hitri filtri kategorij">{"".join(chips)}</div>'


def shop_body(categories: list[dict], cards: str) -> str:
    return f"""<div class="container-site section">
<div class="grid gap-8 lg:grid-cols-[280px_1fr]">
  {_shop_category_sidebar(categories)}
  <div>
  <div class="flex flex-wrap items-baseline justify-between gap-2 border-b border-[#E8E8E8] pb-3">
    <h1 class="h1-display text-[#242424]" data-shop-heading>Izdelki</h1>
    <p class="text-sm text-[#595959]" data-product-count aria-live="polite"></p>
  </div>
  <h2 class="sr-only">Seznam izdelkov</h2>
  {_shop_category_chips(categories)}
  <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
    <label class="sr-only" for="product-search">Iskanje izdelkov</label>
    <input id="product-search" type="search" placeholder="Poiščite izdelek" class="w-full rounded-full border border-[#E8E8E8] px-4 py-2 text-sm sm:max-w-sm" data-product-search>
    <label class="sr-only" for="product-sort">Razvrsti</label>
    <select id="product-sort" class="rounded-full border border-[#E8E8E8] bg-white px-4 py-2 text-sm" data-product-sort>
      <option value="name">Ime A-Z</option>
      <option value="price-asc">Cena: nizka proti visoki</option>
      <option value="price-desc">Cena: visoka proti nizki</option>
    </select>
    <button type="button" data-filter-reset class="hidden rounded-full border border-[#E8E8E8] px-4 py-2 text-xs font-semibold text-[#007BC4] hover:border-[#007BC4]">Ponastavi filter</button>
  </div>
  <div class="grid-products mt-8" data-product-grid>{cards}</div>
  <p id="no-results" class="mt-8 text-[#595959]" hidden>Ni izdelkov, ki bi ustrezali izbranemu filtru.</p>
  </div>
</div>
</div>"""
