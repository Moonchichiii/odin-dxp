from __future__ import annotations

from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


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

    photo_public_id = models.CharField(
        max_length=255,
        help_text="Cloudinary Public ID for their headshot (e.g. 'speakers/elon-musk'). Focus on the face.",
    )

    linkedin_url = models.URLField(blank=True, help_text="Optional LinkedIn profile link.")
    is_keynote = models.BooleanField(default=False, help_text="Check this to prioritize this speaker in lists.")

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("role"),
        FieldPanel("company"),
        FieldPanel("photo_public_id"),
        FieldPanel("linkedin_url"),
        FieldPanel("is_keynote"),
    ]

    class Meta:
        verbose_name = "Speaker"
        verbose_name_plural = "Speakers"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(Lower("name"), Lower("company"), name="uniq_speaker_name_company_ci")]

    def __str__(self) -> str:
        return f"{self.name} ({self.company})"

    def clean(self) -> None:
        self.name = self.name.strip()
        self.company = self.company.strip()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.company}")[:255]
        super().clean()


@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Auto-generated from name.",
    )
    logo_public_id = models.CharField(
        max_length=255, help_text="Cloudinary Public ID for the logo. White/Transparent PNG works best."
    )
    website = models.URLField(blank=True)
    tier = models.CharField(
        max_length=50,
        choices=[("headline", "Headline"), ("gold", "Gold"), ("community", "Community")],
        default="community",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("logo_public_id"),
        FieldPanel("website"),
        FieldPanel("tier"),
    ]

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(Lower("name"), name="uniq_partner_name_ci")]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        self.name = self.name.strip()
        if not self.slug:
            self.slug = slugify(self.name)[:255]
        super().clean()
