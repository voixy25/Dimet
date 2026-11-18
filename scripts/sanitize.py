"""Allowlist sanitizer: turns WordPress/Elementor HTML into plain static markup.

Standard library only. Anything not explicitly allowed is dropped, and the
contents of dangerous elements (script, style, forms, ...) are discarded.
"""
import os
import re
from html import escape
from html.parser import HTMLParser
from typing import Callable
from urllib.parse import urlsplit

ALLOWED_TAGS = {
    "p", "br", "hr", "strong", "b", "em", "i", "u", "span", "div",
    "ul", "ol", "li", "h2", "h3", "h4", "h5", "h6", "blockquote",
    "a", "img", "table", "thead", "tbody", "tr", "th", "td",
}
VOID_TAGS = {"br", "hr", "img", "input", "embed"}
ALLOWED_ATTRS = {
    "a": {"href", "title"},
    "img": {"src", "alt", "width", "height"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
}
DROP_WITH_CONTENT = {
    "script", "style", "form", "input", "select", "textarea", "button",
    "iframe", "object", "embed", "noscript", "svg", "template",
}
SAFE_SCHEMES = {"http", "https", "mailto", "tel"}
LEGACY_HOST = re.compile(r"^(?:www\.)?dimet\.si$", re.I)
HEADING = re.compile(r"<(/?)h([1-6])\b", re.I)
EMPTY_TAG = re.compile(r"<(div|span|p)>\s*</\1>", re.I)


def _safe_url(value: str) -> bool:
    cleaned = re.sub(r"[\x00-\x20]+", "", value).lower()
    if ":" not in cleaned.split("/", 1)[0]:
        return True
    return cleaned.split(":", 1)[0] in SAFE_SCHEMES


class _Allowlist(HTMLParser):
    def __init__(self, known_images: set, route: Callable[[str], str], image_root: str) -> None:
        super().__init__(convert_charrefs=True)
        self.known = known_images
        self.route = route
        self.image_root = image_root
        self.out: list[str] = []
        self.open_tags: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in DROP_WITH_CONTENT:
            if tag not in VOID_TAGS:
                self.skip_depth += 1
            return
        if self.skip_depth or tag not in ALLOWED_TAGS:
            return
        if tag == "img":
            rendered = self._image(dict(attrs))
            if rendered:
                self.out.append(rendered)
            return
        self.out.append(f"<{tag}{self._attributes(tag, attrs)}>")
        if tag not in VOID_TAGS:
            self.open_tags.append(tag)

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in DROP_WITH_CONTENT and tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in DROP_WITH_CONTENT:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth or tag not in self.open_tags:
            return
        while self.open_tags:
            closing = self.open_tags.pop()
            self.out.append(f"</{closing}>")
            if closing == tag:
                break

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.out.append(escape(data, quote=False))

    def close(self) -> None:
        super().close()
        while self.open_tags:
            self.out.append(f"</{self.open_tags.pop()}>")

    def _attributes(self, tag: str, attrs: list) -> str:
        allowed = ALLOWED_ATTRS.get(tag, set())
        parts = []
        for name, value in attrs:
            if name not in allowed or value is None:
                continue
            if name == "href":
                value = self._href(value)
                if value is None:
                    continue
            parts.append(f' {name}="{escape(value, quote=True)}"')
        return "".join(parts)

    def _href(self, value: str) -> str | None:
        parts = urlsplit(value.strip())
        if parts.scheme in ("http", "https") and LEGACY_HOST.match(parts.netloc or ""):
            fragment = f"#{parts.fragment}" if parts.fragment else ""
            return self.route(parts.path) + fragment
        if not _safe_url(value.strip()):
            return None
        return value.strip()

    def _image(self, attrs: dict) -> str:
        src = attrs.get("src") or ""
        name = os.path.basename(urlsplit(src).path)
        if name not in self.known:
            return ""
        alt = escape(attrs.get("alt") or "", quote=True)
        return (
            f'<img src="{self.image_root}images/{escape(name, quote=True)}" '
            f'alt="{alt}" loading="lazy" decoding="async">'
        )


def _no_skipped_headings(html: str) -> str:
    """Clamp headings to h2..h6 and never jump more than one level down the outline."""
    state = {"previous": 1, "open": 2}

    def repl(match: re.Match) -> str:
        closing, level = match.group(1), int(match.group(2))
        if closing:
            return f"</h{state['open']}"
        new_level = min(max(level, 2), state["previous"] + 1)
        state["previous"] = new_level
        state["open"] = new_level
        return f"<h{new_level}"

    return HEADING.sub(repl, html)


def clean_html(html: str, known_images: set, route: Callable[[str], str], image_root: str = "") -> str:
    """Return plain HTML containing only allowlisted tags and attributes.

    route maps a WordPress path to a site-relative href; image_root is the prefix
    to the site root ("" at top level, "../" one level down).
    """
    parser = _Allowlist(known_images, route, image_root)
    parser.feed(html or "")
    parser.close()
    cleaned = "".join(parser.out)
    cleaned = _no_skipped_headings(cleaned)
    cleaned = EMPTY_TAG.sub("", cleaned)
    return re.sub(r"\n\s*\n+", "\n", cleaned).strip()
