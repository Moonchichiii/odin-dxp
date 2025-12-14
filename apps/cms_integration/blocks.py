from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroCtaBlock(blocks.StructBlock):
    """
    Reusable CTA block specifically for the Hero section.
    """
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

    class Meta:
        icon = "link"
        label = "Hero CTA"


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

    extra_images = blocks.ListBlock(
        ImageChooserBlock(required=False),
        required=False,
        label="Extra hero images (optional)",
        help_text="Logos / badges displayed over the hero background.",
    )

    extra_images_position = blocks.ChoiceBlock(
        choices=[
            ("top", "Top"),
            ("center", "Center"),
            ("bottom", "Bottom"),
        ],
        default="top",
        required=False,
        label="Extra images position",
    )

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

    # Updated: List of buttons instead of single link
    cta_buttons = blocks.ListBlock(
        HeroCtaBlock(),
        required=False,
        label="Hero CTA buttons",
        help_text="Add one or more buttons under the hero text.",
    )

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

class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, label="Question")
    answer = blocks.RichTextBlock(required=True, label="Answer")

    class Meta:
        icon = "help"
        label = "FAQ Item"


class FAQSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Frequently Asked Questions")
    faqs = blocks.ListBlock(FAQItemBlock(), label="Questions")

    class Meta:
        template = "cms_integration/blocks/faq_section_block.html"
        icon = "help"
        label = "AEO / FAQ Section"
