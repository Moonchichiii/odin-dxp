from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # Django admin
    path("django-admin/", admin.site.urls),

    # Wagtail admin
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    # Your JSON API
#    path("api/", include("apps.api.urls")),

    # Your HTMX / UI endpoints
    #path("ui/", include("apps.ui.urls")),

    # Our core views
    path("", include(("apps.core.urls", "core"), namespace="core")),

]

# Wagtail's page serving
urlpatterns += [
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
