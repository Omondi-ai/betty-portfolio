import bleach
from django.utils.safestring import mark_safe

# ---------- Full rich text (block + inline) — used for story body, impact, timeline ----------
ALLOWED_TAGS = [
    "p", "br", "strong", "b", "em", "i", "u", "s", "strike",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li",
    "blockquote", "a", "img", "span", "div",
    "table", "thead", "tbody", "tr", "th", "td",
    "hr", "pre", "code",
    "figure", "figcaption",
]

ALLOWED_ATTRIBUTES = {
    "*": ["class", "style"],
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "width", "height"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

# ---------- Inline-only (no block elements) — used for hero statement and intro ----------
INLINE_TAGS = [
    "em", "i", "strong", "b", "u", "s", "br",
    "a", "span",
]

INLINE_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "span": ["class"],
}


def clean_html(html):
    """Sanitise rich HTML for storage. Returns a plain string."""
    if not html:
        return ""
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def sanitize_html(html):
    """Sanitise rich HTML for rendering. Returns a SafeString."""
    return mark_safe(clean_html(html))


def clean_inline(html):
    """Strip ALL block-level tags, keeping text and inline formatting.

    <h2>Hello</h2>          -> Hello
    <p>Hi <strong>there</strong></p>  -> Hi <strong>there</strong>
    <em>italic</em>         -> <em>italic</em>
    """
    if not html:
        return ""
    return bleach.clean(
        html,
        tags=INLINE_TAGS,
        attributes=INLINE_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def sanitize_inline(html):
    """Inline-only sanitised HTML for rendering. Returns a SafeString."""
    return mark_safe(clean_inline(html))


def shape_class(shape):
    return f"shape-{shape}" if shape else "shape-circle"