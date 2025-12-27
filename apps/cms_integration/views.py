from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Partner, Speaker


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


def hx_ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<span class='text-emerald-400 font-medium'>HTMX + Tailwind are alive ⚡</span>")


def hx_sponsors(request: HttpRequest) -> HttpResponse:
    """Fetch all Sponsors/Partners from the Snippet model."""
    # Order by tier importance, then name
    # You might want to add a specific ordering field later, but this works for now.
    partners = Partner.objects.all().order_by("name")

    return render(
        request,
        "cms_integration/partials/sponsors_grid.html",
        {"partners": partners},
    )


def hx_speakers(request: HttpRequest) -> HttpResponse:
    """Fetch all Speakers from the Snippet model."""
    # Filter for keynote first, then alphabetical
    speakers = Speaker.objects.all().order_by("-is_keynote", "name")

    return render(
        request,
        "cms_integration/partials/speakers_grid.html",
        {"speakers": speakers},
    )
