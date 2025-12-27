from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def cld_video(public_id: str | None, width: int = 1080) -> str:
    """
    Generates an optimized Cloudinary video URL.
    """
    if not public_id:
        return ""

    cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "demo")
    return (
        "https://res.cloudinary.com/"
        f"{cloud_name}/video/upload/"
        f"f_auto,q_auto:eco,vc_auto,w_{width},c_limit/{public_id}"
    )


@register.simple_tag
def cld_img(
    public_id: str | None, width: int = 800, height: int | None = None, gravity: str = "auto", format: str = "auto"
) -> str:
    """
    Generates an optimized Cloudinary image URL.
    """
    if not public_id:
        return ""

    cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", "demo")

    # Use specified format or default to auto
    fmt_str = f"f_{format}" if format and format != "auto" else "f_auto"

    transforms: list[str] = [fmt_str, "q_auto", f"w_{width}"]

    if height is not None:
        transforms.append(f"h_{height}")
        transforms.append("c_fill")
        transforms.append(f"g_{gravity}")

    transform_str = ",".join(transforms)
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/{transform_str}/{public_id}"
