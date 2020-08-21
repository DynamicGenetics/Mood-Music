from django.urls import path
from . import views

urlpatterns = [
    path("", views.respond_to_incoming_message, name="ema"),
]
