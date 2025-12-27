from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, cast

from django.forms import Media
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from apps.cms_integration.models import HomePage

logger = logging.getLogger(__name__)


def safe_reverse(viewname: str, *args: Any, **kwargs: Any) -> str:
    """
    Reverse helper that never crashes the admin UI.

    We log at DEBUG level so you can enable it when needed.
    """
    try:
        return reverse(viewname, args=args, kwargs=kwargs)
    except NoReverseMatch as e:
        logger.debug("NoReverseMatch for %s args=%s kwargs=%s (%s)", viewname, args, kwargs, e)
        return ""


def snippet_list_url(app_label: str, model_name: str) -> str:
    """
    Wagtail snippet URLs vary by version / configuration.

    Try:
      1) Namespaced URL: wagtailsnippets_{app}_{model}:list  (newer Wagtail)
      2) Older pattern: wagtailsnippets:list (app, model)
    """
    # Newer Wagtail pattern
    url = safe_reverse(f"wagtailsnippets_{app_label}_{model_name}:list")
    if url:
        return url

    # Older Wagtail pattern
    url = safe_reverse("wagtailsnippets:list", app_label, model_name)
    if url:
        return url

    # Last resort: snippets index (so buttons still appear, just less specific)
    return safe_reverse("wagtailsnippets:index") or ""


@hooks.register("insert_global_admin_css")
def global_admin_css() -> SafeString:
    return format_html('<link rel="stylesheet" href="{}">', static("css/odin-admin.css"))


@hooks.register("register_admin_menu_item")
def register_speakers_menu_item() -> MenuItem:
    return MenuItem(
        "Speakers",
        snippet_list_url("cms_integration", "speaker"),
        icon_name="user",
        order=205,
        classname="odin-menu-speakers",
    )


@hooks.register("register_admin_menu_item")
def register_sponsors_menu_item() -> MenuItem:
    return MenuItem(
        "Sponsors",
        snippet_list_url("cms_integration", "partner"),
        icon_name="group",
        order=210,
        classname="odin-menu-sponsors",
    )


@hooks.register("construct_main_menu")
def clean_sidebar_menu(_request: Any, menu_items: list[Any]) -> None:
    hidden = {"help", "reports", "snippets"}
    menu_items[:] = [item for item in menu_items if getattr(item, "name", "") not in hidden]


@dataclass
class ClientQuickActionsPanel:
    order: int = 0

    @property
    def media(self) -> Media:
        return Media()

    def render_html(self, parent_context: dict[str, Any]) -> SafeString:
        request: HttpRequest = parent_context["request"]

        # Settings
        settings_index = safe_reverse("wagtailsettings:index")
        header_settings_url = (
            safe_reverse("wagtailsettings:edit", "cms_integration", "headersettings") or settings_index
        )
        footer_settings_url = (
            safe_reverse("wagtailsettings:edit", "cms_integration", "footersettings") or settings_index
        )

        # Snippets (robust)
        speakers_url = snippet_list_url("cms_integration", "speaker")
        partners_url = snippet_list_url("cms_integration", "partner")

        # Pages
        pages_url = safe_reverse("wagtailadmin_explore_root")

        # Home page edit
        home_edit_url = ""
        try:
            homepage = cast(Any, HomePage.objects).live().first()
            if homepage:
                home_edit_url = safe_reverse("wagtailadmin_pages:edit", homepage.id)
        except Exception:
            home_edit_url = ""

        context = {
            "home_edit_url": home_edit_url,
            "pages_url": pages_url,
            "header_settings_url": header_settings_url,
            "footer_settings_url": footer_settings_url,
            "speakers_url": speakers_url,
            "partners_url": partners_url,
        }

        html = render_to_string("admin/odin_dashboard_panel.html", context=context, request=request)
        return SafeString(html)


@hooks.register("construct_homepage_panels")
def add_custom_dashboard_panels(_request: HttpRequest, panels: list[Any]) -> None:
    panels[:] = [p for p in panels if getattr(p, "name", "") != "site_summary"]
    panels.insert(0, ClientQuickActionsPanel())
