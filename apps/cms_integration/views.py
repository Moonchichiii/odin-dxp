from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


def hx_ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "<span class='text-emerald-400 font-medium'>HTMX + Tailwind are alive ⚡</span>"
    )
