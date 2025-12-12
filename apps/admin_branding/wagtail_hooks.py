from typing import Any

from django.forms import Media
from django.http import HttpRequest
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import SafeString
from wagtail import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css() -> SafeString:
    """Injects the sleek Odin DXP branding CSS."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/odin-admin.css")
    )


@hooks.register('register_admin_branding')
def branding() -> str:
    return '/'


@hooks.register('construct_main_menu')
def clean_sidebar_menu(request: Any, menu_items: list[Any]) -> None:
    """
    Hides generic items. We want them to focus on Content.
    """
    # Hide Help and Reports for non-superusers (or everyone if you prefer)
    hidden_items = ['help', 'reports']
    menu_items[:] = [item for item in menu_items if item.name not in hidden_items]


class CommandPanel:
    order: int = 10

    # ✅ This prevents the AttributeError
    @property
    def media(self) -> Media:
        return Media()

    def render_html(self, parent_context: dict[str, Any]) -> SafeString:
        return format_html(
            """
            <div class="odin-dashboard-card">
                <div class="odin-dashboard-header">
                    <h2>DXP Odin
                        <span
                            style="font-size:0.5em; vertical-align:middle; border:1px solid #10b981; color:#10b981;
                                   padding:2px 6px; border-radius:4px; margin-left:10px;">
                            LIVE
                        </span>
                    </h2>
                    <p style="color:#94a3b8; margin:0;">Event Intelligence & Orchestration Engine</p>
                </div>
                <div class="odin-status-grid">
                    <div class="status-item">
                        <span class="label">Environment</span>
                        <span class="value">Production</span>
                    </div>
                    <div class="status-item">
                        <span class="label">Active Event</span>
                        <span class="value" style="color:white;">World Summit AI</span>
                    </div>
                    <div class="status-item">
                        <span class="label">System Health</span>
                        <span class="value">100% Operational</span>
                    </div>
                </div>
            </div>
            """
        )


@hooks.register('construct_homepage_panels')
def add_custom_dashboard_panels(request: HttpRequest, panels: list[Any]) -> None:
    # Remove default Wagtail welcome
    panels[:] = [p for p in panels if getattr(p, 'name', '') != 'site_summary']
    # Add our custom panel
    panels.insert(0, CommandPanel())
