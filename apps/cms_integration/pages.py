from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.query import PageQuerySet

from .blocks import (
    ContentBlock,
    CountdownBlock,
    FAQSectionBlock,
    HeroBlock,
    NexusGridBlock,
    PartnerCarouselBlock,
    SpeakerGridBlock,
    SponsorGridBlock,
    TestimonialGridBlock,
)
from .mixins import SEOAttributes
from .snippets import Partner, Speaker, Sponsor

# ---------------------------------------------------------------------
# SPEAKERS
# ---------------------------------------------------------------------


class SpeakersIndexPage(RoutablePageMixin, Page):
    """
    /speakers/ and /speakers/{slug}/
    """

    template = "cms_integration/speakers_index.html"
    subpage_types: list[str] = []

    def get_context(self, request: HttpRequest, *args: Any, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context(request, *args, **kwargs)
        ctx["speakers"] = Speaker.objects.order_by("-is_keynote", "name")
        return ctx

    @route(r"^(?P<slug>[-\w]+)/$")
    def speaker_detail(self, request: HttpRequest, slug: str) -> HttpResponse:
        speaker = get_object_or_404(Speaker, slug=slug)
        return render(
            request,
            "cms_integration/speaker_detail.html",
            {"page": self, "speaker": speaker},
        )


# ---------------------------------------------------------------------
# SPONSORS (COMMERCIAL / TIERED)
# ---------------------------------------------------------------------


class SponsorsIndexPage(RoutablePageMixin, Page):
    """
    /sponsors/ and /sponsors/{slug}/
    """

    template = "cms_integration/sponsors_index.html"
    subpage_types: list[str] = []

    def get_context(self, request: HttpRequest, *args: Any, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context(request, *args, **kwargs)
        ctx["sponsors"] = Sponsor.objects.order_by("tier", "name")
        return ctx

    @route(r"^(?P<slug>[-\w]+)/$")
    def sponsor_detail(self, request: HttpRequest, slug: str) -> HttpResponse:
        sponsor = get_object_or_404(Sponsor, slug=slug)
        return render(
            request,
            "cms_integration/sponsor_detail.html",
            {"page": self, "sponsor": sponsor},
        )


# ---------------------------------------------------------------------
# PARTNERS (NON-COMMERCIAL / COMMUNITY)
# ---------------------------------------------------------------------


class PartnersIndexPage(RoutablePageMixin, Page):
    """
    /partners/ and /partners/{slug}/
    """

    template = "cms_integration/partners_index.html"
    subpage_types: list[str] = []

    def get_context(self, request: HttpRequest, *args: Any, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context(request, *args, **kwargs)
        ctx["partners"] = Partner.objects.order_by("type", "name")
        return ctx

    @route(r"^(?P<slug>[-\w]+)/$")
    def partner_detail(self, request: HttpRequest, slug: str) -> HttpResponse:
        partner = get_object_or_404(Partner, slug=slug)
        return render(
            request,
            "cms_integration/partner_detail.html",
            {"page": self, "partner": partner},
        )


# ---------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------


class HomePage(SEOAttributes, Page):
    template = "cms_integration/home_page.html"

    if TYPE_CHECKING:
        objects: PageQuerySet["HomePage"]

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("countdown", CountdownBlock()),
            ("content_section", ContentBlock()),
            ("testimonial_grid", TestimonialGridBlock()),
            ("nexus_grid", NexusGridBlock()),
            ("speaker_grid", SpeakerGridBlock()),
            ("sponsor_section", SponsorGridBlock()),  # Commercial / Tiered
            ("partner_carousel", PartnerCarouselBlock()),  # GSAP 3D Carousel
            ("faq_section", FAQSectionBlock()),
        ],
        use_json_field=True,
        collapsed=True,
    )

    # Event Schema (SEO / AI / Google)
    event_start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="For Google Event Schema",
    )
    event_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="For Google Event Schema",
    )
    event_location = models.CharField(
        max_length=255,
        blank=True,
        default="Amsterdam",
        help_text="City / Venue for Schema",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("event_start_date"),
                FieldPanel("event_end_date"),
                FieldPanel("event_location"),
            ],
            heading="Schema & Metadata",
            classname="collapsed",
        ),
    ]

    promote_panels = Page.promote_panels + SEOAttributes.seo_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(promote_panels, heading="SEO & Social"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )

    class Meta:
        verbose_name = "Home Page"
