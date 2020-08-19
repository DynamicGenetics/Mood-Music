import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth

from ..models import Artist, Track, UserHistory


def run():
    users = get_user_model().objects.all()

    for user in users:
        spotify_obj = get_recent_history(user)
        save_recent_history(spotify_obj, user)


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
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://127.0.0.1:8000/",
            username=user_uid,
        )
    )

    return sp


def save_recent_history(sp: spotipy.Spotify, user: get_user_model()):
    """Given a recent play history json object, save the relevant
    data into the database.

    Parameters
    ----------
    history : dict
        A json object containing recently played songs.
    user: User
        A Django User object
    """

    # Get the users recent history as a json object
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
