from __future__ import annotations

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string


class SEOAttributes(models.Model):
    og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Recommended size: 1200x630.",
    )

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

    seo_panels = [
        MultiFieldPanel(
            [FieldPanel("og_image"), FieldPanel("structured_data_type")],
            heading="Social Media & AI Context",
        )
    ]

    class Meta:
        abstract = True
