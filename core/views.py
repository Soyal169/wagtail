from django.http import HttpResponse
from django.template.loader import render_to_string


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    content = render_to_string("core/robots.txt", {"sitemap_url": sitemap_url})
    return HttpResponse(content, content_type="text/plain")
