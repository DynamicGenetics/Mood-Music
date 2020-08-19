from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)
    uri = models.CharField(max_length=120)


class Track(models.Model):
    """
    https://developer.spotify.com/console/get-several-tracks/
    https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/
    """

    # Track features (available from user play history call)
    uri = models.CharField(unique=True, max_length=120)
    name = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    duration_ms = models.IntegerField()
    artists = models.ManyToManyField(Artist, related_name="tracks")
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
    track_href = models.CharField(max_length=255)


class UserHistory(models.Model):
    """
    Model to record a users played tracks, as obtained by calls to the
    'user-recently-played' endpoint.
    https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/
    """

    tracks = models.ManyToManyField(Track, through="TrackHistory")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="play_histories"
    )


class TrackHistory(models.Model):
    """Intermediate model that governs the many-to-many relationship between
    tracks and play histories by adding information about the time they were played.

    Popularity is also added to this relationship, because the popularity of a track
    has the potential to change over time.
    """

    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    history = models.ForeignKey(
        UserHistory, related_name="play_histories", on_delete=models.CASCADE
    )
    played_at = models.DateTimeField()
    popularity = models.IntegerField()


class FullUserHistory(models.Model):
    """This table will hold the data submitted by the user at the end of
    the experiment that is sent to them by Spotify. It will be sent in
    JSON format with the four fields placed here.
    """

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="uploaded_history"
    )
    full_history = JSONField()
