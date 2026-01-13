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

from .blocks import ContentBlock, FAQSectionBlock, HeroBlock, PartnerGridBlock, SpeakerGridBlock
from .mixins import SEOAttributes
from .snippets import Partner, Speaker


class SpeakersIndexPage(RoutablePageMixin, Page):
    """
    Logic for /speakers/ and /speakers/{slug}/
    """
    template = "cms_integration/speakers_index.html"
    subpage_types: list[str] = []  # No child pages allowed

    def get_context(self, request: HttpRequest, *args: Any, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context(request, *args, **kwargs)
        ctx["speakers"] = Speaker.objects.order_by("-is_keynote", "name")
        return ctx

    @route(r"^(?P<slug>[-\w]+)/$")
    def speaker_detail(self, request: HttpRequest, slug: str) -> HttpResponse:
        speaker = get_object_or_404(Speaker, slug=slug)
        return render(request, "cms_integration/speaker_detail.html", {"page": self, "speaker": speaker})


class SponsorsIndexPage(RoutablePageMixin, Page):
    """
    Logic for /sponsors/ and /sponsors/{slug}/
    """
    template = "cms_integration/sponsors_index.html"
    subpage_types: list[str] = []

    def get_context(self, request: HttpRequest, *args: Any, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context(request, *args, **kwargs)
        ctx["sponsors"] = Partner.objects.order_by("tier", "name")
        return ctx

    @route(r"^(?P<slug>[-\w]+)/$")
    def sponsor_detail(self, request: HttpRequest, slug: str) -> HttpResponse:
        sponsor = get_object_or_404(Partner, slug=slug)
        return render(request, "cms_integration/sponsor_detail.html", {"page": self, "sponsor": sponsor})


class HomePage(SEOAttributes, Page):
    template = "cms_integration/home_page.html"

    if TYPE_CHECKING:
        objects: PageQuerySet["HomePage"]

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("content_section", ContentBlock()),
            ("speaker_grid", SpeakerGridBlock()),
            ("partner_grid", PartnerGridBlock()),
            ("faq_section", FAQSectionBlock()),
        ],
        use_json_field=True,
        collapsed=True,
    )

    # Schema Data (For Google/AI)
    event_start_date = models.DateTimeField(null=True, blank=True, help_text="For Google Event Schema")
    event_end_date = models.DateTimeField(null=True, blank=True, help_text="For Google Event Schema")
    event_location = models.CharField(
        max_length=255, blank=True, default="Amsterdam", help_text="City/Venue for Schema"
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
