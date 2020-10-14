from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", view=views.dashboard, name="index"),
    path("thanks/", view=views.thanks, name="thanks"),
    path("spotify-connect/", view=views.spotify, name="spotify"),
    path("mobile-surveys/", view=views.mobile_guide, name="mobile_guide"),
    path("data-drop/", views.datadrop, name="datadrop"),
    path("verification/", views.phone_verification, name="phone_verification"),
    path("verification/token/", views.token_validation, name="token_validation"),
    path("verified/", views.verified, name="verified"),
]
