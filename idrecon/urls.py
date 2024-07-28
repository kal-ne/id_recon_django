from django.urls import path

from . import views

urlpatterns = [
    path("identity", views.IdentityView.as_view(), name="identity")
]
