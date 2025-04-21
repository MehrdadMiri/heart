from django import template
import re

register = template.Library()

@register.filter(name="aparat_embed")
def aparat_embed(url: str) -> str:
    """
    Converts a normal Aparat share URL to an iframe‑ready embed URL.

    Share URL examples
      https://www.aparat.com/v/iNgzs
      https://aparat.com/v/iNgzs

    Embed URL pattern (official docs):
      https://www.aparat.com/video/video/embed/videohash/<hash>/vt/frame
    """
    m = re.search(r"aparat\.com/(?:v|video)/([^/?&#]+)", url)
    if m:
        code = m.group(1)
        return f"https://www.aparat.com/video/video/embed/videohash/{code}/vt/frame"
    return url            # fall back unchanged if pattern not matched
