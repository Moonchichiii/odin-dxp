from __future__ import annotations

from typing import Any, Mapping, cast

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string


class LinkBlock(blocks.StructBlock):
    """Simple link for footers/menus"""

    label = blocks.CharBlock(required=True)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False, label="External URL")

    def get_url(self, value: Mapping[str, Any]) -> str:
        page = value.get("page")
        if page:
            return cast(str, page.url)
        return cast(str, value.get("url", ""))

    class Meta:
        icon = "link"
        label = "Link"


class NavItemBlock(blocks.StructBlock):
    """Top level nav item with optional dropdown"""

    label = blocks.CharBlock(required=True)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False, label="External URL")
    children = blocks.ListBlock(
        LinkBlock(),
        required=False,
        label="Dropdown Items",
        help_text="Add links here to create a dropdown menu.",
    )

    def get_url(self, value: Mapping[str, Any]) -> str:
        page = value.get("page")
        if page:
            return cast(str, page.url)
        return cast(str, value.get("url", ""))

    class Meta:
        icon = "folder-open-inverse"
        label = "Menu Item"


class CtaLinkBlock(blocks.StructBlock):
    """Special button for the header (e.g. Get Tickets)"""

    label = blocks.CharBlock(required=True, max_length=50)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False, label="External URL")
    style = blocks.ChoiceBlock(
        choices=[
            ("primary", "Primary (Green)"),
            ("secondary", "Secondary (Border)"),
            ("ghost", "Ghost (Text)"),
        ],
        default="primary",
        required=False,
    )

    def get_url(self, value: Mapping[str, Any]) -> str:
        page = value.get("page")
        if page:
            return cast(str, page.url)
        return cast(str, value.get("url", ""))

    class Meta:
        icon = "link"
        label = "Header Button"


@register_setting(icon="site", order=100)
class HeaderSettings(BaseSiteSetting):
    logo_image: models.ForeignKey = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Upload the site logo (SVG or Transparent PNG preferred).",
    )
    logo_alt_text: models.CharField = models.CharField(
        max_length=120,
        blank=True,
        help_text="Text description of the logo for screen readers (e.g. 'DXP Odin').",
    )

    primary_navigation: StreamField = StreamField([("item", NavItemBlock())], use_json_field=True, blank=True)
    cta_buttons: StreamField = StreamField([("cta", CtaLinkBlock())], use_json_field=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo_image"),
                FieldPanel("logo_alt_text"),
            ],
            heading="Branding",
        ),
        MultiFieldPanel(
            [
                FieldPanel("primary_navigation"),
                FieldPanel("cta_buttons"),
            ],
            heading="Navigation",
        ),
    ]

    class Meta:
        verbose_name = "Header Configuration"


@register_setting(icon="doc-full-inverse", order=110)
class FooterSettings(BaseSiteSetting):
    footer_description: models.TextField = models.TextField(
        default="Event Intelligence Platform built for speed, clarity, and scale.",
        max_length=250,
        help_text="Small blurb appearing below the logo in the footer.",
    )

    footer_col_1_title: models.CharField = models.CharField(default="Explore", max_length=50)
    footer_col_1_links: StreamField = StreamField([("link", LinkBlock())], use_json_field=True, blank=True)

    footer_col_2_title: models.CharField = models.CharField(default="Company", max_length=50)
    footer_col_2_links: StreamField = StreamField([("link", LinkBlock())], use_json_field=True, blank=True)

    # === NEW: Social Media & Toggle Configuration ===
    show_floating_social_bar: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Enable Floating Social Bar",
        help_text=(
            "If checked, a glass sidebar with social icons will appear on the right side of the screen "
            "(Desktop only)."
        ),
    )

    social_linkedin: models.URLField = models.URLField(blank=True, help_text="LinkedIn URL")
    social_x: models.URLField = models.URLField(blank=True, help_text="X (Twitter) URL")
    social_instagram: models.URLField = models.URLField(blank=True, help_text="Instagram URL")
    social_youtube: models.URLField = models.URLField(blank=True, help_text="YouTube URL")
    social_facebook: models.URLField = models.URLField(blank=True, help_text="Facebook URL")

    panels = [
        FieldPanel("footer_description"),
        MultiFieldPanel(
            [
                FieldPanel("footer_col_1_title"),
                FieldPanel("footer_col_1_links"),
            ],
            heading="Column 1",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_col_2_title"),
                FieldPanel("footer_col_2_links"),
            ],
            heading="Column 2",
        ),
        # === NEW PANEL GROUP ===
        MultiFieldPanel(
            [
                FieldPanel("show_floating_social_bar"),
                FieldPanel("social_linkedin"),
                FieldPanel("social_x"),
                FieldPanel("social_instagram"),
                FieldPanel("social_youtube"),
                FieldPanel("social_facebook"),
            ],
            heading="Social Media & Floating Bar",
        ),
    ]

    class Meta:
        verbose_name = "Footer Configuration"


@register_setting(icon="time", order=120)
class FlashSaleSettings(BaseSiteSetting):
    is_active: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="Activate Flash Sale",
        help_text="Check this to show the countdown timer on the site.",
    )

    title: models.CharField = models.CharField(
        max_length=100,
        default="2-For-1 Ticket Flash Sale Ends In",
        help_text="The headline above the timer.",
    )

    end_date: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When does the sale end?",
    )

    end_message: models.CharField = models.CharField(
        max_length=100,
        default="Flash Sale has ended!",
        help_text="What to show when the timer hits zero.",
    )

    cta_label: models.CharField = models.CharField(
        max_length=50,
        default="Get Tickets",
        blank=True,
        help_text="Button label text.",
    )

    cta_url: models.URLField = models.URLField(
        blank=True,
        verbose_name="Button URL",
        help_text="Where the button should link to.",
    )

    panels = [
        FieldPanel("is_active"),
        FieldPanel("title"),
        FieldPanel("end_date"),
        FieldPanel("end_message"),
        MultiFieldPanel(
            [
                FieldPanel("cta_label"),
                FieldPanel("cta_url"),
            ],
            heading="Call to Action",
        ),
    ]

    class Meta:
        verbose_name = "Flash Sale Configuration"
