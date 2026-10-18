import re

from django import template

from core.utils import sanitize_html, sanitize_inline, shape_class

register = template.Library()


@register.filter
def safe_html(value):
    """Rich HTML — preserves block elements."""
    return sanitize_html(value)


@register.filter
def safe_inline(value):
    """Inline-only HTML — strips block elements."""
    return sanitize_inline(value)


@register.filter
def shape(value):
    return shape_class(value)


@register.filter
def has_content(value):
    return bool(value and str(value).strip())


@register.filter
def getattr_filter(obj, name):
    try:
        return getattr(obj, name, "")
    except Exception:
        return ""


@register.filter
def video_embed(value):
    """Return a dict describing how to render a video URL.

    Returns {"type": "iframe", "url": embed_url} for YouTube / Vimeo.
    Returns {"type": "video",  "url": file_url}  for direct MP4/WebM links.
    Returns None for anything unrecognised (so the caller can fall through).
    """
    if not value:
        return None
    value = str(value).strip()

    # YouTube — watch, short, embed, shorts
    yt_patterns = [
        r"(?:youtube\.com/watch\?[^\s]*v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in yt_patterns:
        match = re.search(pattern, value)
        if match:
            return {
                "type": "iframe",
                "url": f"https://www.youtube.com/embed/{match.group(1)}",
            }

    # Vimeo
    vm_match = re.search(r"vimeo\.com/(\d+)", value)
    if vm_match:
        return {
            "type": "iframe",
            "url": f"https://player.vimeo.com/video/{vm_match.group(1)}",
        }

    # Direct video file
    stripped = value.split("?")[0].split("#")[0].lower()
    if stripped.endswith((".mp4", ".webm", ".ogg", ".ogv", ".mov")):
        return {"type": "video", "url": value}

    return None