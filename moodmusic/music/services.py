import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth

from .models import Artist, Track, UserHistory
from .secrets import CLIENT_ID, CLIENT_SECRET


def get_user_histories():
    users = get_user_model().objects.all()

    for user in users:
        history = get_recent_history(user)
        save_recent_history(history, user)


def get_recent_history(user: get_user_model()) -> dict:
    """For a given user, gets their recent play history from the
    Spotify API.

    Parameters
    ----------
    user : User
        A Django User object

    Returns
    -------
    dict
        A json object containing recently played songs. The format of
        this object can be found
        [here](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/).
    """
    # Get this user's social app username from the UserSocialAuth table
    user_uid = UserSocialAuth.objects.get(user=user).uid

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="user-read-recently-played",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri="http://127.0.0.1:8000/",
            username=user_uid,
        )
    )

    return sp.current_user_recently_played()


def save_recent_history(history: dict, user: get_user_model()):
    """Given a recent play history json object, save the relevant
    data into the database.

    Parameters
    ----------
    history : dict
        A json object containing recently played songs.
    user: User
        A Django User object
    """

    # Initiate the UserHistory object for the user
    userhistory = UserHistory.objects.get_or_create(user=user)

    for item in history["items"]:

        # Create or get the Track object
        new_track, _created = Track.objects.get_or_create(
            uri=item["track"]["uri"],
            name=item["track"]["name"],
            album_name=item["track"]["album"]["name"],
            duration_ms=item["track"]["duration_ms"],
        )

        # Create or get the Artist objects
        for artist in item["track"]["artists"]:
            new_artist, _created = Artist.objects.get_or_create(
                name=artist["name"], uri=artist["uri"]
            )
            # Add the artist to Track
            new_track.artist.add(new_artist)

        # Add the track to UserHistory via TrackHistory class
        userhistory.tracks.add(
            new_track,
            through_defaults={
                "played_at": item["played_at"],
                "popularity": item["track"]["popularity"],
            },
        )


if __name__ == "__main__":
    get_user_histories()
