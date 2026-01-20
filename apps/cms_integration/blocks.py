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

    title = blocks.CharBlock(
        required=True,
        label="Main Headline (H1)",
        help_text="The big, punchy text in the center.",
        default="The Future of AI",
    )

    # Keep existing field, but reframe it for the client
    subtitle = blocks.CharBlock(
        required=False,
        label="Lead (Legacy / Optional)",
        help_text="Fallback lead text shown above the H1 if 'Lead paragraph' is empty.",
    )

    # IMPORTANT: if you're now using description as the main paragraph below H1,
    # update label + help text, but keep the field name.
    description = blocks.TextBlock(
        required=False,
        label="Main paragraph (Below H1)",
        help_text="The first paragraph under the headline (gradient style).",
    )

    lead = blocks.CharBlock(
        required=False,
        label="Lead paragraph (Above H1)",
        help_text="Short kicker shown in the top/brain area above the headline (preferred).",
    )

    paragraphs = blocks.ListBlock(
        blocks.CharBlock(required=True, max_length=220),
        required=False,
        label="Extra paragraphs (Below main paragraph)",
        help_text="Optional extra lines under the main paragraph (smaller white text).",
    )

    # Media (unchanged)
    video_public_id = blocks.CharBlock(required=False, label="Cloudinary Video ID", help_text="...")
    poster_public_id = blocks.CharBlock(required=False, label="Cloudinary Poster ID", help_text="...")

    video_upload = DocumentChooserBlock(required=False, label="Upload Video (Fallback)", help_text="...")
    poster_upload = ImageChooserBlock(required=False, label="Upload Poster (Fallback)", help_text="...")

    extra_images = blocks.ListBlock(
        ImageChooserBlock(),
        required=False,
        label="Brain/Logo Image",
        help_text="If set, this replaces the lead text at the very top.",
    )

    cta_buttons = blocks.ListBlock(HeroCtaBlock(), required=False, label="Call to Action Buttons")

    class Meta:
        template = "cms_integration/blocks/hero_block.html"
        icon = "media"
        label = "Hero Section"


class CountdownBlock(blocks.StructBlock):
    """
    High-urgency countdown timer for ticket sales.
    """

    enabled = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="Turn this ON/OFF without removing the block.",
    )

    title = blocks.CharBlock(default="Ticket Flash Sale Ends In")
    target_date = blocks.DateTimeBlock(help_text="The date/time the countdown ends.")
    end_message = blocks.CharBlock(
        default="Sale Ended",
        help_text="Text to show when time is up.",
    )

    cta_label = blocks.CharBlock(required=False, label="Button Label")
    cta_url = blocks.URLBlock(required=False, label="Button URL")

    class Meta:
        template = "cms_integration/blocks/countdown_block.html"
        icon = "time"
        label = "Countdown Timer"


class QuoteItemBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    author = blocks.CharBlock(required=False)
    role = blocks.CharBlock(required=False)
    organization = blocks.CharBlock(
        required=False,
        help_text="e.g. Microsoft",
    )
    logo = ImageChooserBlock(required=False)

    class Meta:
        icon = "openquote"
        label = "Quote"


class TestimonialGridBlock(blocks.StructBlock):
    """
    Grid of quotes/testimonials.
    """

    title = blocks.CharBlock(required=False, default="What People Are Saying")
    quotes = blocks.ListBlock(QuoteItemBlock(), label="Testimonials")

    class Meta:
        template = "cms_integration/blocks/testimonial_grid_block.html"
        icon = "openquote"
        label = "Testimonials"


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
