import json
from datetime import datetime, timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from moodmusic.dashboard.forms import UploadListeningHistoryForm
from moodmusic.music.models import FullUserHistory


class DataDropView(LoginRequiredMixin, FormView):
    form_class = UploadListeningHistoryForm
    template_name = "dashboard/data-drop.html"
    success_url = reverse_lazy("dashboard:thanks")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("file_field")
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f, request.user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


datadrop = DataDropView.as_view()


def handle_uploaded_file(file, user):
    """For each uploaded JSON file, save the
    fields we are interested in to the database """

    try:
        history = json.load(file)
    except json.decoder.JSONDecodeError:
        history = json.load(file.decode("utf-8"))

        # Generate all the objects first and then do a
        # bulk save to the database. This avoids too many data-
        # base calls.
    try:
        songs = [
            FullUserHistory(
                user=user,
                end_time=datetime.strptime(song["endTime"], "%Y-%m-%d %H:%M").replace(
                    tzinfo=timezone.utc
                ),
                artist=song["artistName"],
                track_name=song["trackName"],
                ms_played=int(song["msPlayed"]),
            )
            for song in history
        ]

        # Save to database
        FullUserHistory.objects.bulk_create(songs)

    except Exception as e:
        # TODO: Insert logging!
        raise e
