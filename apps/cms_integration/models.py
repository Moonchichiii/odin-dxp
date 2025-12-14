from __future__ import annotations

from typing import Any, Mapping, cast

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .blocks import ContentBlock, HeroBlock, PartnerGridBlock, SpeakerGridBlock

# --- 1. Snippets (Reusable Data) ---


@register_snippet
class Speaker(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=255,
        help_text="e.g. VP & Chief AI Scientist",
    )
    company = models.CharField(
        max_length=255,
        help_text="e.g. Meta",
    )

    # Cloudinary Public ID (Lightweight string, handled by our helper)
    photo_public_id = models.CharField(
        max_length=255,
        help_text="Cloudinary Public ID (e.g. 'wsai/yann-lecun'). Use folder structure!",
    )

    linkedin_url = models.URLField(blank=True)
    is_keynote = models.BooleanField(default=False)

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("company"),
        FieldPanel("photo_public_id"),
        FieldPanel("linkedin_url"),
        FieldPanel("is_keynote"),
    ]

    class Meta:
        verbose_name = "Speaker (Person)"
        verbose_name_plural = "Speakers (People)"

    def __str__(self) -> str:
        return f"{self.name} - {self.company}"


@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo_public_id = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    tier = models.CharField(
        max_length=50,
        choices=[
            ("headline", "Headline"),
            ("gold", "Gold"),
            ("community", "Community"),
        ],
        default="community",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("logo_public_id"),
        FieldPanel("website"),
        FieldPanel("tier"),
    ]

    class Meta:
        verbose_name = "Sponsor / Partner"
        verbose_name_plural = "Sponsors & Partners"

    def __str__(self) -> str:
        return str(self.name)


# --- 2. The Page Model ---


class HomePage(Page):
    template = "cms_integration/home_page.html"

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("content_section", ContentBlock()),
            ("speaker_grid", SpeakerGridBlock()),
            ("partner_grid", PartnerGridBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Home Page"


# --- 3. Navigation Settings ---


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False, label="External URL")

    def get_url(self, value: Mapping[str, Any]) -> str:
        page = value.get("page")
        if page:
            return cast(str, page.url)
        return cast(str, value.get("url", ""))

    class Meta:
        icon = "link"


@register_setting(icon="link", order=100)
class NavigationSettings(BaseSiteSetting):
    primary_navigation = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
    )

    # Footer Content
    footer_description: models.TextField = models.TextField(
        default="Event Intelligence Platform built for speed, clarity, and scale.",
        max_length=250,
    )

    # Simple columnar structure for footer links
    footer_col_1_title: models.CharField = models.CharField(default="Explore", max_length=50)
    footer_col_1_links = StreamField([("link", LinkBlock())], use_json_field=True, blank=True)

    footer_col_2_title: models.CharField = models.CharField(default="Company", max_length=50)
    footer_col_2_links = StreamField([("link", LinkBlock())], use_json_field=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("primary_navigation"),
            ],
            heading="Header Navigation",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_description"),
                FieldPanel("footer_col_1_title"),
                FieldPanel("footer_col_1_links"),
                FieldPanel("footer_col_2_title"),
                FieldPanel("footer_col_2_links"),
            ],
            heading="Footer Content",
        ),
    ]
class Meta:
        verbose_name = "Header & Footer Links"
