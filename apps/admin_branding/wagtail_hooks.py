from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.forms import Media
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString
from wagtail import hooks
from wagtail.models import Page


def safe_reverse(viewname: str, *args: Any) -> str:
    try:
        return reverse(viewname, args=args)
    except NoReverseMatch:
        return ""


@hooks.register("insert_global_admin_css")
def global_admin_css() -> SafeString:
    """Inject Odin admin branding CSS (Wagtail admin only)."""
    return format_html('<link rel="stylesheet" href="{}">', static("css/odin-admin.css"))


@hooks.register("construct_main_menu")
def clean_sidebar_menu(_request: Any, menu_items: list[Any]) -> None:
    """Hide generic items so editors focus on content."""
    hidden = {"help", "reports"}
    menu_items[:] = [item for item in menu_items if getattr(item, "name", "") not in hidden]


@dataclass
class ClientQuickActionsPanel:
    """Dashboard panel: quick links to the most common editor areas."""
    order: int = 0

    @property
    def media(self) -> Media:
        return Media()

    def render_html(self, parent_context: dict[str, Any]) -> SafeString:
        request: HttpRequest = parent_context["request"]

        # Settings
        nav_settings_url = safe_reverse("wagtailsettings:edit", "cms_integration", "navigationsettings")
        if not nav_settings_url:
            nav_settings_url = safe_reverse("wagtailsettings:index")

        # Snippets (fallback to snippets index)
        snippets_index = safe_reverse("wagtailsnippets:index")
        speakers_url = safe_reverse("wagtailsnippets:list", "cms_integration", "speaker") or snippets_index
        partners_url = safe_reverse("wagtailsnippets:list", "cms_integration", "partner") or snippets_index

        # Pages fallback
        pages_url = safe_reverse("wagtailadmin_explore_root")

        # Home page edit (best effort)
        home_edit_url = ""
        try:
            root = Page.get_first_root_node()
            homepage = root.get_children().live().specific().first()
            if homepage:
                home_edit_url = safe_reverse("wagtailadmin_pages:edit", homepage.id)
        except Exception:
            home_edit_url = ""

        context = {
            "home_edit_url": home_edit_url,
            "pages_url": pages_url,
            "nav_settings_url": nav_settings_url,
            "speakers_url": speakers_url,
            "partners_url": partners_url,
        }

        html = render_to_string("admin/odin_dashboard_panel.html", context=context, request=request)
        return SafeString(html)


@hooks.register("construct_homepage_panels")
def add_custom_dashboard_panels(_request: HttpRequest, panels: list[Any]) -> None:
    panels[:] = [p for p in panels if getattr(p, "name", "") != "site_summary"]
    panels.insert(0, ClientQuickActionsPanel())
