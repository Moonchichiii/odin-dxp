from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, cast

from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.query import PageQuerySet
from wagtail.snippets.models import register_snippet

from .blocks import ContentBlock, FAQSectionBlock, HeroBlock, PartnerGridBlock, SpeakerGridBlock

# --- 0. SEO & AEO Mixin (Abstract) ---


class SEOAttributes(models.Model):
    """
    Inherit from this to give any Page powerful SEO & Social capabilities.
    """

    # 1. Social Sharing
    og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=("Social Share Image (Facebook/LinkedIn/Twitter). " "Recommended size: 1200x630."),
    )

    # 2. AEO / Structured Data Context
    structured_data_type = models.CharField(
        max_length=50,
        choices=[
            ("Website", "Website (General)"),
            ("Event", "Event (Conference/Summit)"),
            ("Organization", "Organization (Company)"),
            ("Article", "Article/Blog Post"),
        ],
        default="Website",
        help_text="Tells Google/AI what this page represents.",
    )

    # Panels to be used in the Promote tab
    seo_panels = [
        MultiFieldPanel(
            [
                FieldPanel("og_image"),
                FieldPanel("structured_data_type"),
            ],
            heading="Social Media & AI Context",
        ),
    ]

    class Meta:
        abstract = True


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
        help_text="Cloudinary Public ID (e.g. 'name,role,company'). Use folder structure!",
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


# --- 2. The Page Model (Updated with SEO/AEO) ---


class HomePage(SEOAttributes, Page):
    template = "cms_integration/home_page.html"

    if TYPE_CHECKING:
        objects: PageQuerySet["HomePage"]

    # A. Content Structure
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

    # B. AEO Specific Data (For JSON-LD)
    event_start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Used for Google Event Schema",
    )
    event_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Used for Google Event Schema",
    )
    event_location = models.CharField(
        max_length=255,
        blank=True,
        default="Amsterdam",
        help_text="City/Venue for Schema",
    )

    # Content tab
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("event_start_date"),
                FieldPanel("event_end_date"),
                FieldPanel("event_location"),
            ],
            heading="Event Key Details (For AI/Google)",
            classname="collapsible",
        ),
        FieldPanel("body"),
    ]

    # SEO tab (Promote + our mixin panels)
    promote_panels = Page.promote_panels + SEOAttributes.seo_panels

    # Editor tabs
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(promote_panels, heading="SEO & Social"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )

    class Meta:
        verbose_name = "Home Page"


# --- 3. Global Site Settings ---


# 3a. Shared Blocks
class LinkBlock(blocks.StructBlock):
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
    label = blocks.CharBlock(required=True)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False, label="External URL")

    # Submenu items (optional)
    children = blocks.ListBlock(
        LinkBlock(),
        required=False,
        label="Submenu links",
        help_text="Optional dropdown items under this nav item.",
    )

    def get_url(self, value: Mapping[str, Any]) -> str:
        page = value.get("page")
        if page:
            return cast(str, page.url)
        return cast(str, value.get("url", ""))

    class Meta:
        icon = "folder-open-inverse"
        label = "Nav item"


class CtaLinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True, max_length=50)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.URLBlock(required=False, label="External URL")
    style = blocks.ChoiceBlock(
        choices=[
            ("primary", "Primary"),
            ("secondary", "Secondary"),
            ("ghost", "Ghost"),
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
        label = "CTA button"


# 3b. Header Settings
@register_setting(icon="site", order=100)
class HeaderSettings(BaseSiteSetting):
    logo_image: models.ForeignKey = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    logo_alt_text: models.CharField = models.CharField(
        max_length=120,
        blank=True,
        help_text="Accessibility alt text for the logo (optional).",
    )

    # Updated to use NavItemBlock for dropdown support
    primary_navigation = StreamField(
        [("item", NavItemBlock())],
        use_json_field=True,
        blank=True,
        help_text="Top navigation (supports optional dropdown children).",
    )

    # Added CTA buttons
    cta_buttons = StreamField(
        [("cta", CtaLinkBlock())],
        use_json_field=True,
        blank=True,
        help_text="Header CTA buttons shown on desktop + mobile.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo_image"),
                FieldPanel("logo_alt_text"),
                FieldPanel("primary_navigation"),
                FieldPanel("cta_buttons"),
            ],
            heading="Header",
        )
    ]

    class Meta:
        verbose_name = "Header"


# 3c. Footer Settings
@register_setting(icon="doc-full-inverse", order=110)
class FooterSettings(BaseSiteSetting):
    footer_description: models.TextField = models.TextField(
        default="Event Intelligence Platform built for speed, clarity, and scale.",
        max_length=250,
    )

    footer_col_1_title: models.CharField = models.CharField(default="Explore", max_length=50)
    footer_col_1_links = StreamField([("link", LinkBlock())], use_json_field=True, blank=True)

    footer_col_2_title: models.CharField = models.CharField(default="Company", max_length=50)
    footer_col_2_links = StreamField([("link", LinkBlock())], use_json_field=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("footer_description"),
                FieldPanel("footer_col_1_title"),
                FieldPanel("footer_col_1_links"),
                FieldPanel("footer_col_2_title"),
                FieldPanel("footer_col_2_links"),
            ],
            heading="Footer",
        )
    ]
    class Meta:
        verbose_name = "Footer"
