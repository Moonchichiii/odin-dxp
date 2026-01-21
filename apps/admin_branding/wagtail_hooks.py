from __future__ import annotations

import logging
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
from wagtail.admin.menu import MenuItem
from wagtail.models import Site

logger = logging.getLogger(__name__)


def safe_reverse(viewname: str, *args: Any, **kwargs: Any) -> str:
    try:
        return reverse(viewname, args=args, kwargs=kwargs)
    except NoReverseMatch as e:
        logger.debug("NoReverseMatch for %s args=%s kwargs=%s (%s)", viewname, args, kwargs, e)
        return ""


def snippet_list_url(app_label: str, model_name: str) -> str:
    url = safe_reverse(f"wagtailsnippets_{app_label}_{model_name}:list")
    if url:
        return url

    url = safe_reverse("wagtailsnippets:list", app_label, model_name)
    if url:
        return url

    return safe_reverse("wagtailsnippets:index") or ""


def get_site_home_edit_url(request: HttpRequest) -> str:
    try:
        site = Site.find_for_request(request)
        if not site or not site.root_page:
            return ""

        root = site.root_page.specific

        # Import lazily to avoid any chance of early app-loading issues.
        from apps.cms_integration.models import HomePage  # noqa: WPS433

        if not isinstance(root, HomePage):
            return ""

        return safe_reverse("wagtailadmin_pages:edit", root.id)
    except Exception:
        logger.exception("Failed to resolve Site homepage edit URL")
        return ""


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
        snippet_list_url("cms_integration", "sponsor"),  # ✅ updated
        icon_name="dollar-sign",  # ✅ clearer semantic icon
        order=210,
        classname="odin-menu-sponsors",
    )


@hooks.register("register_admin_menu_item")
def register_partners_menu_item() -> MenuItem:
    return MenuItem(
        "Partners",
        snippet_list_url("cms_integration", "partner"),  # ✅ new menu item
        icon_name="group",
        order=211,
        classname="odin-menu-partners",
    )


@hooks.register("construct_main_menu")
def clean_sidebar_menu(_request: Any, menu_items: list[Any]) -> None:
    hidden = {"help", "reports"}

    # Hide "snippets" only if our custom snippet list URLs resolve.
    if (
        snippet_list_url("cms_integration", "speaker")
        and snippet_list_url("cms_integration", "sponsor")
        and snippet_list_url("cms_integration", "partner")
    ):
        hidden.add("snippets")

    menu_items[:] = [item for item in menu_items if getattr(item, "name", "") not in hidden]


@dataclass
class ClientQuickActionsPanel:
    order: int = 0

    @property
    def media(self) -> Media:
        return Media()

    def render_html(self, parent_context: dict[str, Any]) -> SafeString:
        request: HttpRequest = parent_context["request"]

        settings_index = safe_reverse("wagtailsettings:index")
        header_settings_url = (
            safe_reverse("wagtailsettings:edit", "cms_integration", "headersettings") or settings_index
        )
        footer_settings_url = (
            safe_reverse("wagtailsettings:edit", "cms_integration", "footersettings") or settings_index
        )
        cookie_settings_url = (
            safe_reverse("wagtailsettings:edit", "cms_integration", "cookiesettings") or settings_index
        )
        flash_sale_url = safe_reverse("wagtailsettings:edit", "cms_integration", "flashsalesettings") or settings_index

        speakers_url = snippet_list_url("cms_integration", "speaker")
        sponsors_url = snippet_list_url("cms_integration", "sponsor")
        partners_url = snippet_list_url("cms_integration", "partner")

        pages_url = safe_reverse("wagtailadmin_explore_root")
        home_edit_url = get_site_home_edit_url(request)
        nexus_edit_url = home_edit_url or pages_url

        context = {
            "home_edit_url": home_edit_url,
            "pages_url": pages_url,
            "header_settings_url": header_settings_url,
            "footer_settings_url": footer_settings_url,
            "flash_sale_url": flash_sale_url,
            "nexus_edit_url": nexus_edit_url,
            "speakers_url": speakers_url,
            "sponsors_url": sponsors_url,
            "partners_url": partners_url,
            "cookie_settings_url": cookie_settings_url,
        }

        html = render_to_string("admin/odin_dashboard_panel.html", context=context, request=request)
        return SafeString(html)


@hooks.register("construct_homepage_panels")
def add_custom_dashboard_panels(_request: HttpRequest, panels: list[Any]) -> None:
    panels[:] = [p for p in panels if getattr(p, "name", "") != "site_summary"]
    panels.insert(0, ClientQuickActionsPanel())
