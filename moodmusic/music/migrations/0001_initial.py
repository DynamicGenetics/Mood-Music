# Generated by Django 3.0.5 on 2020-10-16 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("uri", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uri", models.CharField(max_length=120, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("album_name", models.CharField(max_length=255)),
                ("duration_ms", models.IntegerField()),
                ("danceability", models.FloatField()),
                ("energy", models.FloatField()),
                ("key", models.IntegerField()),
                ("loudness", models.FloatField()),
                ("mode", models.IntegerField()),
                ("speechiness", models.FloatField()),
                ("acousticness", models.FloatField()),
                ("instrumentalness", models.FloatField()),
                ("liveness", models.FloatField()),
                ("valence", models.FloatField()),
                ("tempo", models.FloatField()),
                ("time_signature", models.IntegerField()),
                ("track_href", models.CharField(max_length=255)),
                (
                    "artists",
                    models.ManyToManyField(related_name="tracks", to="music.Artist"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TrackHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("played_at", models.DateTimeField()),
                ("popularity", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="UserHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tracks",
                    models.ManyToManyField(
                        through="music.TrackHistory", to="music.Track"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="play_histories",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="trackhistory",
            name="history",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="play_histories",
                to="music.UserHistory",
            ),
        ),
        migrations.AddField(
            model_name="trackhistory",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="music.Track"
            ),
        ),
        migrations.CreateModel(
            name="FullUserHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("end_time", models.DateTimeField()),
                ("artist", models.CharField(max_length=600)),
                ("track_name", models.CharField(max_length=600)),
                ("ms_played", models.IntegerField()),
                ("time_added", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploaded_history",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
