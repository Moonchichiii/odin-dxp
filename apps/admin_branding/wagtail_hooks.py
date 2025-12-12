from typing import Any

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


class CommandPanel:
    order: int = 10

    def render_html(self, parent_context: dict[str, Any]) -> SafeString:
        # A custom "Mission Control" panel
        return format_html(
            """
            <div class="odin-dashboard-card">
                <div class="odin-dashboard-header">
                    <div class="odin-logo-mark">⚡</div>
                    <div>
                        <h2>DXP Odin <span class="badge">v1.0</span></h2>
                        <p>Event Intelligence Orchestration</p>
                    </div>
                </div>
                <div class="odin-status-grid">
                    <div class="status-item">
                        <span class="label">System Status</span>
                        <span class="value text-emerald">Operational</span>
                    </div>
                    <div class="status-item">
                        <span class="label">Cache Layer</span>
                        <span class="value text-emerald">Redis Active</span>
                    </div>
                    <div class="status-item">
                        <span class="label">Media Engine</span>
                        <span class="value text-blue">Cloudinary Connected</span>
                    </div>
                </div>
            </div>
            """
        )


@hooks.register('construct_homepage_panels')
def add_custom_dashboard_panels(request: HttpRequest, panels: list[Any]) -> None:
    panels[:] = [p for p in panels if getattr(p, 'name', '') != 'site_summary']
    # Add our custom panel
    panels.insert(0, CommandPanel())
