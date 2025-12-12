from django.http import HttpRequest, HttpResponse


def hx_ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "<span class='text-emerald-400 font-medium'>HTMX + Tailwind are alive ⚡</span>"
    )
