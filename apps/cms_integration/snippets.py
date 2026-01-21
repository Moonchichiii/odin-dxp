from __future__ import annotations

from typing import Any

from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.snippets.models import register_snippet

from .utils.cloudinary_upload import upload_wagtail_image_to_cloudinary

# ---------------------------------------------------------------------
# SPEAKERS
# ---------------------------------------------------------------------


@register_snippet
class Speaker(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Auto-generated from name. Used in URLs.",
    )
    role = models.CharField(max_length=255, help_text="e.g. 'VP of Engineering'")
    company = models.CharField(max_length=255, help_text="e.g. 'OpenAI'")

    photo_upload = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Upload/select a headshot from Wagtail Images (recommended).",
    )

    photo_public_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="Cloudinary Public ID fallback (e.g. 'speakers/elon-musk').",
    )

    linkedin_url = models.URLField(blank=True)
    is_keynote = models.BooleanField(default=False)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("role"),
        FieldPanel("company"),
        FieldPanel("photo_upload"),
        FieldPanel("photo_public_id"),
        FieldPanel("linkedin_url"),
        FieldPanel("is_keynote"),
    ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.photo_upload and not self.photo_public_id:
            self.photo_public_id = upload_wagtail_image_to_cloudinary(
                self.photo_upload,
                folder="speakers",
            )
        super().save(*args, **kwargs)

    def clean(self) -> None:
        self.name = self.name.strip()
        self.company = self.company.strip()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.company}")[:255]
        super().clean()

    class Meta:
        verbose_name = "Speaker"
        verbose_name_plural = "Speakers"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                Lower("company"),
                name="uniq_speaker_name_company_ci",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.company})"


# ---------------------------------------------------------------------
# SPONSORS (RENAMED FROM Partner — DATA PRESERVED)
# ---------------------------------------------------------------------


@register_snippet
class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Auto-generated from name.",
    )

    logo_upload = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Upload/select a logo from Wagtail Images (recommended).",
    )

    logo_public_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="Cloudinary Public ID for the logo.",
    )

    website = models.URLField(blank=True)

    # Sponsors are tiered (commercial relationship)
    TIER_CHOICES = [
        ("platinum", "Platinum"),
        ("gold", "Gold"),
        ("silver", "Silver"),
        ("bronze", "Bronze"),
    ]
    tier = models.CharField(max_length=50, choices=TIER_CHOICES, default="bronze")

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("tier"),
        FieldPanel("logo_upload"),
        FieldPanel("logo_public_id"),
        FieldPanel("website"),
    ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.logo_upload and not self.logo_public_id:
            self.logo_public_id = upload_wagtail_image_to_cloudinary(
                self.logo_upload,
                folder="sponsors",
            )
        super().save(*args, **kwargs)

    def clean(self) -> None:
        self.name = self.name.strip()
        if not self.slug:
            self.slug = slugify(self.name)[:255]
        super().clean()

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ["tier", "name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uniq_sponsor_name_ci",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_tier_display()})"


# ---------------------------------------------------------------------
# PARTNERS (NEW — NON-COMMERCIAL RELATIONSHIPS)
# ---------------------------------------------------------------------


@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Auto-generated from name.",
    )

    logo_upload = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Upload/select a logo from Wagtail Images (recommended).",
    )

    logo_public_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="Cloudinary Public ID for the logo.",
    )

    website = models.URLField(blank=True)

    # Partners have types, not tiers
    TYPE_CHOICES = [
        ("community", "Community Partner"),
        ("media", "Media Partner"),
        ("technology", "Technology Partner"),
        ("institutional", "Institutional Partner"),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="community")

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("type"),
        FieldPanel("logo_upload"),
        FieldPanel("logo_public_id"),
        FieldPanel("website"),
    ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.logo_upload and not self.logo_public_id:
            self.logo_public_id = upload_wagtail_image_to_cloudinary(
                self.logo_upload,
                folder="partners",
            )
        super().save(*args, **kwargs)

    def clean(self) -> None:
        self.name = self.name.strip()
        if not self.slug:
            self.slug = slugify(self.name)[:255]
        super().clean()

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"
        ordering = ["type", "name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="uniq_partner_name_ci",
            )
        ]

    def __str__(self) -> str:
        return self.name
