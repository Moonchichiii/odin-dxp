from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        help_text="Main headline (e.g. 'Real-time event journeys')",
    )
    subtitle = blocks.CharBlock(
        required=False,
        help_text="Highlighted text (e.g. 'orchestrated by data')",
    )
    description = blocks.TextBlock(required=False)

    # Cloudinary integration
    video_public_id = blocks.CharBlock(
        required=False,
        label="Video Public ID",
        help_text="e.g. 'odin/hero-bg'. Leave empty for image only.",
    )
    poster_public_id = blocks.CharBlock(
        required=True,
        label="Poster/Image Public ID",
        help_text=(
            "e.g. 'odin/hero-bg-poster'. Used for mobile "
            "and while video loads."
        ),
    )

    cta_text = blocks.CharBlock(required=False, default="Get Tickets")
    cta_link = blocks.CharBlock(
        required=False,
        help_text="URL or relative path",
    )

    class Meta:
        template = "cms_integration/blocks/hero_block.html"
        icon = "media"
        label = "Hero Section"


class ContentBlock(blocks.StructBlock):
    """
    For general text sections like the 'Back to the future' intro.
    """

    heading = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock()

    class Meta:
        template = "cms_integration/blocks/content_block.html"
        icon = "doc-full"
        label = "Text Section"


class SpeakerGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Meet the Legends")
    description = blocks.TextBlock(required=False)

    # Allow manual selection of speakers for the home page
    featured_speakers = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Speaker"),
        label="Select Speakers to highlight",
    )

    class Meta:
        template = "cms_integration/blocks/speaker_grid_block.html"
        icon = "group"
        label = "Speaker Grid"


class PartnerGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Commercial Partners")

    # Manual selection is safer for high-visibility pages like the home page
    partners = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Partner"),
        label="Select Partners to display",
    )

    class Meta:
        template = "cms_integration/blocks/partner_grid_block.html"
        icon = "gem"
        label = "Partner Logos"
