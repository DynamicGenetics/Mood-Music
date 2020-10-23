import os
import time
import logging
import spotipy
from social_django.utils import load_strategy
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from ..models import Artist, Track, UserHistory

logger = logging.getLogger(__name__)

# Auth object should remain consistent for all users and calls
auth = SpotifyOAuth(
    client_id=os.environ["SPOTIFY_CLIENT_ID"],
    client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
    scope="user-read-recently-played",
    redirect_uri=reverse("dashboard:thanks"),
)


def run():
    users = get_user_model().objects.all()

    for user in users:
        try:
            save_recent_history(user)
        except ObjectDoesNotExist:
            logger.warning(
                "No social_auth.usersocialauth record for user: {}".format(user.id)
            )
            pass


def save_recent_history(user: get_user_model()):
    """Given a recent play history json object, save the relevant
    data into the database.

    Parameters
    ----------
    user: User
        A Django User object
    """

    # Get the user's authentication token
    social = user.social_auth.get(provider="spotify")  # Python Social Auth
    access_token = social.get_access_token(load_strategy())  # Python Social Auth
    sp = spotipy.Spotify(auth=access_token)  # Spotipy

    try:
        # Get the user's recent history as a json object
        history = sp.current_user_recently_played()
    except spotipy.SpotifyException as e:
        if e.http_status == 429:
            logger.warning("Rate Limit error receieved (HTTP Status 429). Waiting...")
            time.sleep(int(e.msg["Retry-After"]))
            history = sp.current_user_recently_played()
        elif e.http_status == 401:
            logger.info(
                "Access token expired for user {}. Refreshing now...".format(user.id)
            )
            social.refresh_token(load_strategy())
            access_token = social.get_access_token(load_strategy())
            sp = spotipy.Spotify(auth=access_token)  # Recreate the Spotify auth obj.
            history = (
                sp.current_user_recently_played()
            )  # Try getting the history again.
            logger.info(
                "Access token refreshed for user {}, and history retrieved.".format(
                    user.id
                )
            )
        else:
            logger.warning(
                "Unknown error recieved. HTTP Status: {}. Message: {}.".format(
                    e.http_status, e.msg
                )
            )
            # Wait 10 seconds and try again, just in case.
            time.sleep(10)
            history = sp.current_user_recently_played()

    # Initiate the UserHistory object for the user
    userhistory, _created = UserHistory.objects.get_or_create(user=user)

    for item in history["items"]:

        # Create or get the Track object - extra API call required for 'Create'
        try:
            new_track = Track.objects.get(uri=item["track"]["uri"])
        except Track.DoesNotExist:
            # If does not exist, then need to get the song features too
            try:
                features = sp.audio_features(item["track"]["id"])
            except spotipy.SpotifyException as e:
                if e.http_status == 429:
                    time.sleep(
                        e.msg["Retry-After"] + 1
                    )  # Reason for +1 here: https://stackoverflow.com/questions/30548073/spotify-web-api-rate-limits
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

    logger.info("Listening history saved for user: {}".format(user.id))
