from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:url_id>", views.redirect_to_url, name="redirect_to_url"),
]
