from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .snippets import Partner, Speaker


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


def hx_ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<span class='text-emerald-400 font-medium'>HTMX + Tailwind are alive ⚡</span>")


def hx_sponsors(request: HttpRequest) -> HttpResponse:
    partners = Partner.objects.only("name", "logo_public_id", "website", "tier").order_by("name")
    return render(request, "cms_integration/partials/sponsors_grid.html", {"partners": partners})


def hx_speakers(request: HttpRequest) -> HttpResponse:
    speakers = Speaker.objects.only(
        "name", "slug", "role", "company", "photo_public_id", "linkedin_url", "is_keynote"
    ).order_by("-is_keynote", "name")
    return render(request, "cms_integration/partials/speakers_grid.html", {"speakers": speakers})
