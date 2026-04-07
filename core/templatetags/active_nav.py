from django import template
from django.utils import translation

register = template.Library()


@register.simple_tag(takes_context=True)
def active_nav(context, *urls):
    request = context.get("request")
    if not request:
        return ""

    current_url = request.path

    for url in urls:
        if url == "home" and (current_url == "/" or current_url == ""):
            return "text-blue-600 font-semibold"
        elif url != "home" and current_url.startswith(f"/{url}/"):
            return "text-blue-600 font-semibold"

    return "text-gray-700 hover:text-blue-600 font-medium transition-colors"
