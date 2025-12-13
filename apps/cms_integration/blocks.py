from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        help_text="Main headline (optional).",
    )
    subtitle = blocks.CharBlock(
        required=False,
        help_text="Highlighted text (optional).",
    )
    description = blocks.TextBlock(required=False)

    # Option A (recommended for speed): Cloudinary IDs
    video_public_id = blocks.CharBlock(
        required=False,
        label="Video Public ID (Cloudinary)",
        help_text="e.g. 'odin/hero-bg'. If set, takes priority over uploaded video.",
    )
    poster_public_id = blocks.CharBlock(
        required=False,
        label="Poster/Image Public ID (Cloudinary)",
        help_text="e.g. 'odin/hero-bg-poster'. Used as fallback + while video loads.",
    )

    # Option B: Upload in Wagtail (optional)
    video_upload = DocumentChooserBlock(
        required=False,
        label="Upload Video (optional)",
        help_text="Upload MP4/WebM. Used only if Video Public ID is empty.",
    )
    poster_upload = ImageChooserBlock(
        required=False,
        label="Upload Poster Image (optional)",
        help_text="Fallback image if no video, or while video loads.",
    )

    cta_text = blocks.CharBlock(required=False, default="Get Tickets")
    cta_link = blocks.CharBlock(required=False, help_text="URL or relative path")

    class Meta:
        template = "cms_integration/blocks/hero_block.html"
        icon = "media"
        label = "Hero Section"


class ContentBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock()

    class Meta:
        template = "cms_integration/blocks/content_block.html"
        icon = "doc-full"
        label = "Text Section"


class SpeakerGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Meet the Legends")
    description = blocks.TextBlock(required=False)

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

    partners = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Partner"),
        label="Select Partners to display",
    )

    class Meta:
        template = "cms_integration/blocks/partner_grid_block.html"
        icon = "gem"
        label = "Partner Logos"
