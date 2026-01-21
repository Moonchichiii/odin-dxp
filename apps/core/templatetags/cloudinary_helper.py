from __future__ import annotations

from django import template
from django.conf import settings

register = template.Library()


def _cloud_name() -> str:
    """
    Single source of truth for Cloudinary cloud name.
    """
    storage = getattr(settings, "CLOUDINARY_STORAGE", {})
    return storage.get("CLOUD_NAME") or "demo"


@register.simple_tag
def cld_video(public_id: str | None, width: int = 1080) -> str:
    """
    Generates an optimized Cloudinary video URL.
    """
    if not public_id:
        return ""

    cloud_name = _cloud_name()
    return (
        f"https://res.cloudinary.com/{cloud_name}/video/upload/"
        f"f_auto,q_auto:eco,vc_auto,w_{width},c_limit/{public_id}"
    )


@register.simple_tag
def cld_img(
    public_id: str | None,
    width: int = 800,
    height: int | None = None,
    gravity: str = "auto",
    fmt: str = "auto",
    quality: str = "auto",
) -> str:
    """
    Generates an optimized Cloudinary image URL.
    """
    if not public_id:
        return ""

    cloud_name = _cloud_name()

    fmt_str = f"f_{fmt}" if fmt and fmt != "auto" else "f_auto"
    quality_str = f"q_{quality}" if quality and quality != "auto" else "q_auto"
    transforms: list[str] = [fmt_str, quality_str, "dpr_auto", f"w_{width}"]

    if height is not None:
        transforms.extend(
            [
                f"h_{height}",
                "c_fill",
                f"g_{gravity}",
            ]
        )

    transform_str = ",".join(transforms)
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/{transform_str}/{public_id}"


@register.simple_tag
def cld_srcset(public_id: str | None, aspect_ratio: str = "4:3") -> str:
    """
    Generates a responsive srcset string.
    Output: "url 600w, url 800w, url 1200w"
    Uses: f_auto,q_auto,c_fill,g_auto + enforced aspect ratio.
    """
    if not public_id:
        return ""

    cloud_name = _cloud_name()
    base_url = f"https://res.cloudinary.com/{cloud_name}/image/upload"

    base_params = f"f_auto,q_auto,c_fill,g_auto,ar_{aspect_ratio}"

    small = f"{base_url}/{base_params},w_600/{public_id} 600w"
    medium = f"{base_url}/{base_params},w_800/{public_id} 800w"
    large = f"{base_url}/{base_params},w_1200/{public_id} 1200w"

    return f"{small}, {medium}, {large}"
