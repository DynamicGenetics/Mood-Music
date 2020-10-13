from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", view=views.dashboard, name="dashboard"),
    path("thanks", view=views.thanks, name="thanks"),
    path("spotify-connect", view=views.spotify, name="spotify"),
    path("mobile-surveys", view=views.mobile_guide, name="mobile_guide"),
    path("data-drop", views.datadrop, name="datadrop"),
    path("consent", views.ConsentView.as_view(), name="consent"),
]
