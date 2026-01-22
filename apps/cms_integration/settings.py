from __future__ import annotations

from typing import Any, Mapping, cast

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page


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
        default="Global AI & future-tech events platform. Connecting minds, shaping the future.",
        max_length=250,
        help_text="A short, high-impact value proposition appearing below the logo.",
    )

    footer_col_1_title: models.CharField = models.CharField(
        default="Explore",
        max_length=50,
    )
    footer_col_1_links: StreamField = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
    )

    footer_col_2_title: models.CharField = models.CharField(
        default="Company",
        max_length=50,
    )
    footer_col_2_links: StreamField = StreamField(
        [("link", LinkBlock())],
        use_json_field=True,
        blank=True,
    )

    company_name: models.CharField = models.CharField(
        default="Nexus AI Events Global Ltd",
        max_length=255,
    )
    company_address: models.TextField = models.TextField(
        default=("Level 5, The Innovation Hub\n" "123 Future Tech Boulevard\n" "London, EC1V 9XX\n" "United Kingdom"),
    )
    company_numbers: models.TextField = models.TextField(
        default="Company No: 12345678\nVAT No: GB 987 6543 21",
    )

    copyright_text: models.CharField = models.CharField(
        default="All rights reserved",
        max_length=255,
        help_text="Text shown after the automatic year.",
    )

    show_footer_social_icons: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Show Social Icons Inside Footer",
    )

    # === Contact block ===
    show_enquiries_block: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Show Contact Block",
        help_text="Toggle the contact section in the footer.",
    )

    enquiries_title: models.CharField = models.CharField(
        default="Enquiries",
        max_length=50,
        help_text="Heading shown above the contact details.",
    )

    enquiries_email: models.EmailField = models.EmailField(
        blank=True,
        help_text="Contact email shown in the footer.",
    )

    enquiries_phone: models.CharField = models.CharField(
        blank=True,
        max_length=30,
        help_text="Optional phone number (e.g. +44 20 1234 5678).",
    )

    panels = [
        FieldPanel("footer_description"),
        MultiFieldPanel(
            [FieldPanel("show_footer_social_icons")],
            heading="Footer: Social Icons",
        ),
        MultiFieldPanel(
            [FieldPanel("footer_col_1_title"), FieldPanel("footer_col_1_links")],
            heading="Footer Column 1",
        ),
        MultiFieldPanel(
            [FieldPanel("footer_col_2_title"), FieldPanel("footer_col_2_links")],
            heading="Footer Column 2",
        ),
        MultiFieldPanel(
            [
                FieldPanel("company_name"),
                FieldPanel("company_address"),
                FieldPanel("company_numbers"),
                FieldPanel("copyright_text"),
            ],
            heading="Legal & Address",
        ),
        MultiFieldPanel(
            [
                FieldPanel("show_enquiries_block"),
                FieldPanel("enquiries_title"),
                FieldPanel("enquiries_email"),
                FieldPanel("enquiries_phone"),
            ],
            heading="Footer Contact",
        ),
    ]

    class Meta:
        verbose_name = "Footer Configuration"


@register_setting(icon="link", order=120)
class SocialLinksSettings(BaseSiteSetting):
    """
    Canonical social URLs used across the site (footer + sidebar).
    """

    linkedin: models.URLField = models.URLField(blank=True, verbose_name="LinkedIn URL")
    x: models.URLField = models.URLField(blank=True, verbose_name="X (Twitter) URL")
    instagram: models.URLField = models.URLField(blank=True, verbose_name="Instagram URL")
    youtube: models.URLField = models.URLField(blank=True, verbose_name="YouTube URL")
    facebook: models.URLField = models.URLField(blank=True, verbose_name="Facebook URL")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("linkedin"),
                FieldPanel("x"),
                FieldPanel("instagram"),
                FieldPanel("youtube"),
                FieldPanel("facebook"),
            ],
            heading="Social Links",
        )
    ]

    class Meta:
        verbose_name = "Social Links (URLs)"


@register_setting(icon="cog", order=130)
class SocialSidebarSettings(BaseSiteSetting):
    """
    Controls ONLY the floating social sidebar (templates/partials/social_floating.html).
    """

    enabled: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Enable Floating Social Sidebar",
        help_text="Shows the floating sidebar on the right. Template: templates/partials/social_floating.html",
    )

    panels = [
        FieldPanel("enabled"),
    ]

    class Meta:
        verbose_name = "Social Sidebar (Toggle)"


@register_setting(icon="time", order=130)
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


@register_setting(icon="locked", order=150)
class CookieSettings(BaseSiteSetting):
    is_active: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="Enable Cookie Banner",
        help_text="Show the consent banner to new visitors.",
    )
    title: models.CharField = models.CharField(default="We value your privacy", max_length=100)
    message: models.TextField = models.TextField(
        default=(
            "We use cookies to enhance your browsing experience, serve personalized ads or content, "
            "and analyze our traffic."
        )
    )
    accept_button_text: models.CharField = models.CharField(default="Accept All", max_length=50)
    decline_button_text: models.CharField = models.CharField(default="Decline", max_length=50)

    # Links to legal pages
    privacy_page: models.ForeignKey = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    privacy_policy_url: models.URLField = models.URLField(blank=True, help_text="External link if page not selected")

    panels = [
        FieldPanel("is_active"),
        FieldPanel("title"),
        FieldPanel("message"),
        MultiFieldPanel(
            [
                FieldPanel("accept_button_text"),
                FieldPanel("decline_button_text"),
            ],
            heading="Buttons",
        ),
        MultiFieldPanel(
            [
                FieldPanel("privacy_page"),
                FieldPanel("privacy_policy_url"),
            ],
            heading="Legal Link",
        ),
    ]

    class Meta:
        verbose_name = "Cookie Consent Settings"
