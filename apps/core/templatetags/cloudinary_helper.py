from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def cld_video(public_id: str | None, width: int = 1920) -> str:
    """
    Generates an optimized Cloudinary video URL.

    Usage:
        {% cld_video 'odin/hero-bg' width=1920 %}
    """
    if not public_id:
        return ""

    cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "demo")
    return (
        "https://res.cloudinary.com/"
        f"{cloud_name}/video/upload/"
        f"f_auto,q_auto:good,vc_auto,w_{width},c_limit/{public_id}"
    )


@register.simple_tag
def cld_img(
    public_id: str | None,
    width: int = 800,
    height: int | None = None,
    gravity: str = "auto",
) -> str:
    """
    Generates an optimized Cloudinary image URL.

    Usage:
        {% cld_img 'odin/speaker-1' width=400 height=400 gravity='face' %}
    """
    if not public_id:
        return ""

    cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "demo")

    transforms: list[str] = [f"f_auto,q_auto,w_{width}"]
    if height is not None:
        transforms.append(f"h_{height}")
        transforms.append("c_fill")
        transforms.append(f"g_{gravity}")

    transform_str = ",".join(transforms)
    return (
        "https://res.cloudinary.com/"
        f"{cloud_name}/image/upload/{transform_str}/{public_id}"
    )
