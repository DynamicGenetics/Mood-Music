from django.urls import path
from .views import views

urlpatterns = [
    path("", views.respond_to_incoming_message, name="ema"),
    path("startsession", views.start_survey_session, name="startsession"),
]
