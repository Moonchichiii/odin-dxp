from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class HeroCtaBlock(blocks.StructBlock):
    """
    A specific button style for the Hero section (Big & Bold).
    """

    label = blocks.CharBlock(
        required=True, max_length=50, help_text="Text to appear on the button (e.g., 'Get Tickets')."
    )
    page = blocks.PageChooserBlock(required=False, help_text="Link to an internal page.")
    url = blocks.URLBlock(
        required=False, label="External URL", help_text="Link to an external site (e.g., https://google.com)."
    )
    style = blocks.ChoiceBlock(
        choices=[
            ("primary", "Primary (Green Glow)"),
            ("secondary", "Secondary (Glass/Border)"),
            ("ghost", "Ghost (Text Link)"),
        ],
        default="primary",
        required=False,
    )

    class Meta:
        icon = "link"
        label = "Hero Button"


class HeroBlock(blocks.StructBlock):
    """
    Full-screen hero section with video background and centered text.
    """

    title = blocks.CharBlock(required=True, help_text="Main headline (H1). Keep it punchy.", default="The Future of AI")
    subtitle = blocks.CharBlock(
        required=False,
        help_text="Gradient text below the headline (optional).",
    )
    description = blocks.TextBlock(
        required=False, help_text="Small uppercase text above the headline (e.g., 'OCTOBER 2026 • AMSTERDAM')."
    )

    # Media
    video_public_id = blocks.CharBlock(
        required=False,
        label="Cloudinary Video ID",
        help_text="The 'Public ID' from Cloudinary (e.g., 'odin/hero-bg'). Optimized for streaming.",
    )
    poster_public_id = blocks.CharBlock(
        required=False,
        label="Cloudinary Poster ID",
        help_text="Image ID to show while video loads (e.g., 'odin/hero-poster').",
    )

    # Fallback Uploads
    video_upload = DocumentChooserBlock(
        required=False,
        label="Upload Video (Fallback)",
        help_text="Upload MP4 if not using Cloudinary ID.",
    )
    poster_upload = ImageChooserBlock(
        required=False,
        label="Upload Poster (Fallback)",
        help_text="Upload an image if not using Cloudinary ID.",
    )

    # Extra visual elements
    extra_images = blocks.ListBlock(
        ImageChooserBlock(),
        required=False,
        label="Floating Logos",
        help_text="Add sponsor logos or badges to float above the title.",
    )

    cta_buttons = blocks.ListBlock(
        HeroCtaBlock(),
        required=False,
        label="Call to Action Buttons",
    )

    class Meta:
        template = "cms_integration/blocks/hero_block.html"
        icon = "media"
        label = "Hero Section"


class ContentBlock(blocks.StructBlock):
    """
    Standard text section with a glass card background.
    """

    heading = blocks.CharBlock(required=False, help_text="Section title.")
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ul", "ol"],
        help_text="Main content. Formatting is limited to keep the design clean.",
    )

    class Meta:
        template = "cms_integration/blocks/content_block.html"
        icon = "doc-full"
        label = "Content Section"


class SpeakerGridBlock(blocks.StructBlock):
    """
    Displays a grid of selected speakers.
    """

    title = blocks.CharBlock(default="Meet the Legends")
    description = blocks.TextBlock(required=False, help_text="Introductory text below the title.")

    featured_speakers = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Speaker"),
        label="Select Speakers",
        help_text="Search and select speakers to display in this grid.",
    )

    class Meta:
        template = "cms_integration/blocks/speaker_grid_block.html"
        icon = "group"
        label = "Speaker Grid"


class PartnerGridBlock(blocks.StructBlock):
    """
    Displays a grid of partners/sponsors.
    """

    title = blocks.CharBlock(default="Commercial Partners")

    partners = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Partner"),
        label="Select Partners",
        help_text="Search and select sponsors to display.",
    )

    class Meta:
        template = "cms_integration/blocks/partner_grid_block.html"
        icon = "gem"
        label = "Partner Logos"


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True)
    answer = blocks.RichTextBlock(features=["bold", "italic", "link"])

    class Meta:
        icon = "help"
        label = "Q&A"


class FAQSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="Frequently Asked Questions")
    faqs = blocks.ListBlock(FAQItemBlock(), label="Questions")

    class Meta:
        template = "cms_integration/blocks/faq_section_block.html"
        icon = "help"
        label = "FAQ Section"
