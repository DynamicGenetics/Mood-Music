from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models


class Artist(models.Model):
    name = models.CharField()


class Track(models.Model):
    """
    https://developer.spotify.com/console/get-several-tracks/
    https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/
    """

    # Track features (available from user play history call)
    spotify_id = models.CharField(unique=True)
    name = models.CharField()
    album_name = models.CharField()
    artists = models.ManyToManyField(Artist, on_delete=models.CASCADE)
    duration_ms = models.IntegerField()
    popularity = models.IntegerField()
    # Audio analysis features (separate API call)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.IntegerField()
    track_href = models.CharField()


class APIPlayHistory(models.Model):
    """

    https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/
    """

    track = models.ForeignKey(Track)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    played_at = models.DateTimeField()


class RequestPlayHistory(models.Model):
    """This table will hold the data submitted by the user at the end of
    the experiment that is sent to them by Spotify. It will be sent in
    JSON format with the four fields placed here.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    full_history = JSONField()
