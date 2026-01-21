from __future__ import annotations

import os
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# Any of these showing up in rendered HTML means your templates did NOT execute correctly.
FORBIDDEN_RENDER_TOKENS = [
    "{% image",
    "{% include",
    "{% if",
    "{% load",
    "{{",
    "}}",
    "%}",
]

# We mainly care about the CMS templates that previously broke.
CRITICAL_TEMPLATES_TO_RENDER = [
    "cms_integration/partials/cards/speaker_card.html",
    "cms_integration/partials/cards/sponsor_card.html",
    "cms_integration/partials/speakers_grid.html",
    "cms_integration/partials/sponsors_grid.html",
    "cms_integration/blocks/speaker_grid_block.html",
    "cms_integration/blocks/partner_grid_block.html",
]


def _repo_root() -> Path:
    # If this file is in repo root, parents[0] is repo root.
    # If it’s inside a folder, this still works reasonably because we walk up until we find "templates/".
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "templates").exists():
            return candidate
    return here.parent


def _setup_django(repo_root: Path) -> None:
    """
    Boot Django so we can render templates using the real template engine + your installed tags.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # Ensure repo root is importable
    sys.path.insert(0, str(repo_root))

    import django  # noqa: WPS433

    django.setup()


def _render_template(template_name: str, context: dict[str, Any]) -> str:
    from django.template.loader import render_to_string  # noqa: WPS433

    return render_to_string(template_name, context)


def _build_dummy_contexts() -> dict[str, dict[str, Any]]:
    """
    Build contexts that exercise both Cloudinary branch and (if possible) Wagtail-image branch.
    We always include a Cloudinary fallback context so rendering never depends on DB/image availability.
    """
    speaker_cloud = SimpleNamespace(
        name="Test Speaker",
        company="Test Company",
        role="Test Role",
        linkedin_url="",
        is_keynote=False,
        photo_upload=None,
        photo_public_id="speakers/test-speaker",
    )
    sponsor_cloud = SimpleNamespace(
        name="Test Sponsor",
        tier="community",
        website="https://example.com",
        logo_upload=None,
        logo_public_id="sponsors/test-sponsor",
    )

    contexts: dict[str, dict[str, Any]] = {
        "speaker_card_cloud": {"speaker": speaker_cloud},
        "sponsor_card_cloud": {"sponsor": sponsor_cloud},
        "speakers_grid_cloud": {"speakers": [speaker_cloud, speaker_cloud]},
        # Fix: context key must match the loop in the template (sponsors, not partners)
        "sponsors_grid_cloud": {"sponsors": [sponsor_cloud, sponsor_cloud]},
        # block templates use `self`
        "speaker_grid_block_cloud": {
            "self": SimpleNamespace(title="Meet the Legends", description="", featured_speakers=[speaker_cloud])
        },
        "partner_grid_block_cloud": {"self": SimpleNamespace(title="Commercial Partners", partners=[sponsor_cloud])},
    }

    # Optional: try to pull a real DB-backed object to exercise the `{% image ... %}` path.
    # If DB isn’t migrated / no images exist, we simply skip.
    try:
        from apps.cms_integration.snippets import Partner, Speaker  # noqa: WPS433

        real_speaker = Speaker.objects.exclude(photo_upload=None).first()
        if real_speaker:
            contexts["speaker_card_db"] = {"speaker": real_speaker}
            contexts["speakers_grid_db"] = {"speakers": [real_speaker]}

        real_partner = Partner.objects.exclude(logo_upload=None).first()
        if real_partner:
            contexts["sponsor_card_db"] = {"sponsor": real_partner}
            # Fix: context key must match the loop (sponsors), passing the Partner model instance
            contexts["sponsors_grid_db"] = {"sponsors": [real_partner]}
    except Exception:
        # Don’t fail the hook if DB isn’t available in CI yet.
        pass

    return contexts


def _render_guard() -> list[str]:
    """
    Render critical templates and ensure no Django/Wagtail template tokens leak into output.
    """
    failures: list[str] = []
    contexts = _build_dummy_contexts()

    render_matrix = [
        ("cms_integration/partials/cards/speaker_card.html", ["speaker_card_cloud", "speaker_card_db"]),
        ("cms_integration/partials/cards/sponsor_card.html", ["sponsor_card_cloud", "sponsor_card_db"]),
        ("cms_integration/partials/speakers_grid.html", ["speakers_grid_cloud", "speakers_grid_db"]),
        ("cms_integration/partials/sponsors_grid.html", ["sponsors_grid_cloud", "sponsors_grid_db"]),
        ("cms_integration/blocks/speaker_grid_block.html", ["speaker_grid_block_cloud"]),
        ("cms_integration/blocks/partner_grid_block.html", ["partner_grid_block_cloud"]),
    ]

    for template_name, ctx_keys in render_matrix:
        for key in ctx_keys:
            if key not in contexts:
                continue
            out = _render_template(template_name, contexts[key])

            for token in FORBIDDEN_RENDER_TOKENS:
                if token in out:
                    failures.append(f"[render] {template_name} ({key}): leaked token '{token}' into output")
                    break  # don’t spam multiple tokens for same render

            # Extra sanity: card templates should produce an <img> in cloud mode
            if "card_cloud" in key and ("speaker_card" in key or "sponsor_card" in key):
                if "<img" not in out:
                    failures.append(f"[render] {template_name} ({key}): expected an <img> tag but none found")

    return failures


def main() -> int:
    repo_root = _repo_root()
    failures: list[str] = []

    # Removed static scan entirely. Relying solely on render guard.

    # Render check: only if Django can boot
    try:
        _setup_django(repo_root)
        failures.extend(_render_guard())
    except Exception as e:
        # If Django setup fails, we fail the hook because we can't verify templates.
        failures.append(f"[render] Django template render guard could not run: {e!r}")

    if failures:
        print("\n".join(failures))
        print(
            "\nFix: stop formatters from breaking Django tags, ensure `{% load wagtailimages_tags %}` exists, "
            "and ensure critical templates do not leak `{% ... %}` / `{{ ... }}` into final HTML."
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
