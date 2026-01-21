from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

# ---------------------------------------------------------------------
# HERO BLOCKS
# ---------------------------------------------------------------------


class HeroCtaBlock(blocks.StructBlock):
    """
    A specific button style for the Hero section (Big & Bold).
    """

    label = blocks.CharBlock(
        required=True,
        max_length=50,
        help_text="Text to appear on the button (e.g., 'Get Tickets').",
    )
    page = blocks.PageChooserBlock(required=False, help_text="Link to an internal page.")
    url = blocks.URLBlock(
        required=False,
        label="External URL",
        help_text="Link to an external site (e.g., https://google.com).",
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
        default="The Future of AI",
    )

    subtitle = blocks.CharBlock(
        required=False,
        label="Lead (Legacy / Optional)",
        help_text="Fallback lead text shown above the H1 if 'Lead paragraph' is empty.",
    )

    description = blocks.TextBlock(
        required=False,
        label="Main paragraph (Below H1)",
        help_text="The first paragraph under the headline (gradient style).",
    )

    lead = blocks.CharBlock(
        required=False,
        label="Lead paragraph (Above H1)",
        help_text="Short kicker shown above the headline (preferred).",
    )

    paragraphs = blocks.ListBlock(
        blocks.CharBlock(required=True, max_length=220),
        required=False,
        label="Extra paragraphs (Below main paragraph)",
    )

    video_public_id = blocks.CharBlock(required=False, label="Cloudinary Video ID")
    poster_public_id = blocks.CharBlock(required=False, label="Cloudinary Poster ID")

    video_upload = DocumentChooserBlock(required=False, label="Upload Video (Fallback)")
    poster_upload = ImageChooserBlock(required=False, label="Upload Poster (Fallback)")

    extra_images = blocks.ListBlock(
        ImageChooserBlock(),
        required=False,
        label="Brain / Logo Image",
        help_text="If set, this replaces the lead text at the very top.",
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


# ---------------------------------------------------------------------
# TIME / URGENCY
# ---------------------------------------------------------------------


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
    target_date = blocks.DateTimeBlock()
    end_message = blocks.CharBlock(default="Sale Ended")

    cta_label = blocks.CharBlock(required=False)
    cta_url = blocks.URLBlock(required=False)

    class Meta:
        template = "cms_integration/blocks/countdown_block.html"
        icon = "time"
        label = "Countdown Timer"


# ---------------------------------------------------------------------
# CONTENT & SOCIAL PROOF
# ---------------------------------------------------------------------


class QuoteItemBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    author = blocks.CharBlock(required=False)
    role = blocks.CharBlock(required=False)
    organization = blocks.CharBlock(required=False)
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

    heading = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ul", "ol"],
    )

    class Meta:
        template = "cms_integration/blocks/content_block.html"
        icon = "doc-full"
        label = "Content Section"


# ---------------------------------------------------------------------
# NEXUS (DYNAMIC FEATURE GRID)
# ---------------------------------------------------------------------


class NexusFeatureItemBlock(blocks.StructBlock):
    """
    A single row in the Z-layout.
    """

    tagline = blocks.CharBlock(
        required=False,
        help_text="Small eyebrow text (e.g., 'Track 6')",
    )
    headline = blocks.CharBlock(
        required=True,
        help_text="Main title (e.g., 'AI MEDIA')",
    )
    description = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ul", "ol"],
        help_text="The descriptive content.",
    )

    # Image Handling
    image_upload = ImageChooserBlock(required=False, help_text="Wagtail Image (fallback)")
    image_public_id = blocks.CharBlock(
        required=False,
        help_text="Cloudinary Public ID (e.g., 'v1234/my-image')",
    )

    # CTA
    cta_label = blocks.CharBlock(required=False, label="Button Label")
    cta_url = blocks.URLBlock(required=False, label="Button URL")

    class Meta:
        icon = "doc-full-inverse"
        label = "Feature Row"


class NexusGridBlock(blocks.StructBlock):
    """
    The container for the Z-pattern layout.
    """

    title = blocks.CharBlock(required=False, help_text="Optional Section Heading")
    features = blocks.ListBlock(NexusFeatureItemBlock(), label="Feature Rows")

    class Meta:
        template = "cms_integration/blocks/nexus_feature_grid.html"
        icon = "list-ul"
        label = "Nexus Dynamic Feature Grid"


# ---------------------------------------------------------------------
# SPEAKERS
# ---------------------------------------------------------------------


class SpeakerGridBlock(blocks.StructBlock):
    """
    Displays a grid of selected speakers.
    """

    title = blocks.CharBlock(default="Meet the Legends")
    description = blocks.TextBlock(required=False)

    featured_speakers = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Speaker"),
        label="Select Speakers",
    )

    class Meta:
        template = "cms_integration/blocks/speaker_grid_block.html"
        icon = "group"
        label = "Speaker Grid"


# ---------------------------------------------------------------------
# SPONSORS (COMMERCIAL / TIERED)
# ---------------------------------------------------------------------


class SponsorGridBlock(blocks.StructBlock):
    """
    Static grid for Sponsors (commercial, tiered, ordered by value).
    """

    title = blocks.CharBlock(default="Our Sponsors")

    sponsors = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Sponsor"),
        label="Select Sponsors",
        help_text="Commercial sponsors. Displayed by tier.",
    )

    class Meta:
        template = "cms_integration/blocks/sponsors_grid.html"
        icon = "group"
        label = "Sponsor Grid"


# ---------------------------------------------------------------------
# PARTNERS (NON-COMMERCIAL / COMMUNITY)
# ---------------------------------------------------------------------


class PartnerCarouselBlock(blocks.StructBlock):
    """
    GSAP-powered 3D carousel for Partners.
    """

    title = blocks.CharBlock(default="Community Partners")

    partners = blocks.ListBlock(
        SnippetChooserBlock("cms_integration.Partner"),
        label="Select Partners",
        help_text="Community, media, technology, or institutional partners.",
    )

    class Meta:
        template = "cms_integration/blocks/partners_carousel.html"
        icon = "gem"
        label = "Partner Carousel (3D)"


# ---------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------


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
