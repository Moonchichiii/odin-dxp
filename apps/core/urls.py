from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("hx/ping/", views.hx_ping, name="htmx-ping"),
]
