from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = template.Library()


@register.filter
def startswith(text, prefix):
    return bool(text) and str(text).startswith(str(prefix))


@register.filter
def split(value, delimiter=","):
    """Splits a comma-separated CharField value into a trimmed list, e.g.
    for rendering tech-stack chips or a JSON-LD knowsAbout array."""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]


@register.simple_tag
def nav_is_active(request_path, link_page, title):
    """Whether a header nav link should render as the active page.
    Home matches only on an exact path; every other section matches
    itself and its descendants (e.g. a project case study still
    highlights "Projects")."""
    if not link_page:
        return False
    if title == "Home":
        return request_path == link_page.url
    return request_path.startswith(link_page.url)


@register.simple_tag
def highlight_gradient(full_text, highlight):
    """Wraps the first occurrence of `highlight` within `full_text` in the
    site's gradient-text span, escaping everything else."""
    if not highlight or highlight not in full_text:
        return escape(full_text)
    before, _, after = full_text.partition(highlight)
    gradient_span = (
        '<span class="text-transparent bg-clip-text bg-gradient-to-r '
        'from-emerald-600 to-teal-600 dark:from-emerald-400 dark:to-teal-400">'
        f"{escape(highlight)}</span>"
    )
    return mark_safe(f"{escape(before)}{gradient_span}{escape(after)}")


@register.simple_tag
def toc_headings(body):
    """Collects (anchor_id, text) tuples for every heading block in a
    StreamField body, for an auto-generated table of contents."""
    headings = []
    for block in body:
        if block.block_type == "heading":
            headings.append((slugify(block.value), str(block.value)))
    return headings
