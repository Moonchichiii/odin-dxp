from __future__ import annotations

from typing import Any, Mapping, Optional, Protocol, cast

import cloudinary.uploader


class HasFileField(Protocol):
    file: Any


def upload_wagtail_image_to_cloudinary(
    image: HasFileField,
    *,
    folder: str,
    public_id: Optional[str] = None,
) -> str:
    f = image.file
    f.open("rb")

    try:
        options: dict[str, Any] = {
            "folder": folder,
            "resource_type": "image",
            "overwrite": True,
            "unique_filename": False,
        }
        if public_id:
            options["public_id"] = public_id

        result = cast(Mapping[str, Any], cloudinary.uploader.upload(f, **options))
        return str(result["public_id"])
    finally:
        try:
            f.close()
        except Exception:
            pass
