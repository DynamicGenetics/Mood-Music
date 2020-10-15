from django.contrib.auth import get_user_model

from .services import get_recent_history, save_recent_history

# Create your views here.


def recently_played(user: get_user_model()):
    "Request recently played list and save it to db"

    history = get_recent_history(user)
    save_recent_history(history, user)
