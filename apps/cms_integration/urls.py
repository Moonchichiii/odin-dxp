from django.urls import path

from . import views

app_name = "cms_integration"

urlpatterns = [
    path("sponsors/", views.hx_sponsors, name="hx-sponsors"),
    path("speakers/", views.hx_speakers, name="hx-speakers"),
    path("ping/", views.hx_ping, name="htmx-ping"),
]
