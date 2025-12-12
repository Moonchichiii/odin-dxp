from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("hx/ping/", views.hx_ping, name="htmx-ping"),
]
