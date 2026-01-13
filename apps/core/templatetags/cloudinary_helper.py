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
