import os
import spotipy


from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timestamp
from social_django.models import UserSocialAuth

from ..models import Artist, Track, UserHistory


def run():
    users = get_user_model().objects.all()

    for user in users:
        save_recent_history(user)


# This is adapted from https://github.com/plamere/spotipy/issues/555
class CustomAuthManager:
    def __init__(self, user):
        self.auth = SpotifyOAuth(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://127.0.0.1:8000/",
        )
        self.auth_info = UserSocialAuth.objects.get(user=user).extra_data

    @property
    def access_token(self):
        return self._current_token

    @access_token.setter
    def access_token(self, user):
        now = timezone.now()

        recorded_token = self.auth_info["access_token"]
        # if no token or token about to expire soon
        if not recorded_token or self.auth_info["expires_at"] > now.timestamp() + 60:
            new_auth_info = self.auth.refresh_access_token(
                self.auth_info["refresh_token"]
            )

        UserSocialAuth.objects.get(user=user).extra_data = new_auth_info

        self._current_token = new_auth_info["access_token"]

        return self._current_token["access_token"]


spotify = spotipy.Spotify(auth_manager=CustomAuthManager(user))


def save_recent_history(sp: spotipy.Spotify, user: get_user_model()):
    """Given a recent play history json object, save the relevant
    data into the database.

    Parameters
    ----------
    user: User
        A Django User object
    """

    # Get the user's authentication token
    try:
        user_auth = UserSocialAuth.objects.get(user=user).extra_data["access_token"]
        sp = spotipy.Spotify(auth=user_auth)
    except spotipy.exceptions.SpotifyException:
        sp = SpotifyOAuth(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            scope="user-read-recently-played",
            redirect_uri="http://127.0.0.1:8000/",
        )

    sp = spotipy.Spotify(auth=user_auth)

    # Get the user's recent history as a json object
    history = sp.current_user_recently_played()

    # Initiate the UserHistory object for the user
    userhistory, _created = UserHistory.objects.get_or_create(user=user)

    for item in history["items"]:

        # Create or get the Track object - extra API call required for 'Create'
        try:
            new_track = Track.objects.get(uri=item["track"]["uri"])
        except Track.DoesNotExist:
            # If does not exist, then need to get the song features too
            features = sp.audio_features(item["track"]["id"])

            # Set up the track object
            new_track = Track(
                uri=item["track"]["uri"],
                name=item["track"]["name"],
                album_name=item["track"]["album"]["name"],
                duration_ms=item["track"]["duration_ms"],
                danceability=features[0]["danceability"],
                energy=features[0]["energy"],
                key=features[0]["key"],
                loudness=features[0]["loudness"],
                mode=features[0]["mode"],
                speechiness=features[0]["speechiness"],
                acousticness=features[0]["acousticness"],
                instrumentalness=features[0]["instrumentalness"],
                liveness=features[0]["liveness"],
                valence=features[0]["valence"],
                tempo=features[0]["tempo"],
                time_signature=features[0]["time_signature"],
                track_href=features[0]["track_href"],
            )
            new_track.save()

        # Create or get the Artist objects associated with the track
        for artist in item["track"]["artists"]:
            new_artist, _created = Artist.objects.get_or_create(
                name=artist["name"], uri=artist["uri"]
            )
            # Add the artist to Track
            new_track.artists.add(new_artist)

        # Add the track to UserHistory via TrackHistory class
        userhistory.tracks.add(
            new_track,
            through_defaults={
                "played_at": item["played_at"],
                "popularity": item["track"]["popularity"],
            },
        )
