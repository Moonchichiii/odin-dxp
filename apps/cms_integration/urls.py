from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("hx/sponsors/", views.hx_sponsors, name="hx-sponsors"),
    path("hx/speakers/", views.hx_speakers, name="hx-speakers"),
    path("hx/ping/", views.hx_ping, name="htmx-ping"),
]
