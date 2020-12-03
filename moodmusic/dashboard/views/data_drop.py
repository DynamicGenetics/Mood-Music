import json
import os
import logging
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView

from moodmusic.dashboard.forms import UploadListeningHistoryForm
from moodmusic.music.models import FullUserHistory

logger = logging.getLogger(__name__)


class DataDropView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = UploadListeningHistoryForm
    template_name = "dashboard/data-drop.html"
    # success_url = reverse_lazy("dashboard:thanks")
    success_message = "Thank you! Your file/s were sucessfully saved."

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("file_field")
        if form.is_valid():
            for f in files:
                # First check the file extension
                try:
                    validate_ext(f)
                except ValidationError:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        """Please make sure you are uploading a file ending in .json""",
                    )
                    return self.form_invalid(form)
                # Then try and catch for errors in the json
                try:
                    handle_uploaded_file(f, request.user)
                except ValidationError:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        """Sorry, this document does not contain the expected data.
                        Please check that you are uploading a 'StreamingHistory' file
                         and try again.""",
                    )
                    return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """Overwrite success view to remain on the same page"""
        return self.request.path


datadrop = DataDropView.as_view()


def validate_ext(file):
    """Make sure file name passed ends in .json. Raise ValidationError otherwise."""
    ext = os.path.splitext(file.name)[1]
    valid_extensions = [".json"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Sorry, only .json files are accepted.")


def handle_uploaded_file(file, user):
    """For each uploaded JSON file, save the
    fields we are interested in to the database """

    # Get the file from the InMemoryUploadedObject
    file = file.file

    try:
        history = json.load(file)
    except AttributeError:
        history = json.load(file.decode("utf-8"))

    # Check the file is not empty
    if len(history) == 0:
        raise ValidationError("Empty JSON.")

    # Generate all the objects first and then do a
    # bulk save to the database. This avoids too many data-
    # base calls.
    try:
        songs = [
            FullUserHistory(
                user=user,
                end_time=datetime.strptime(song["endTime"], "%Y-%m-%d %H:%M").replace(
                    tzinfo=timezone.utc  # This converts from naive to timeaware TZ
                ),
                artist=song["artistName"],
                track_name=song["trackName"],
                ms_played=int(song["msPlayed"]),
            )
            for song in history
        ]

        # Save to database
        FullUserHistory.objects.bulk_create(songs)

    except (TypeError, KeyError):
        # These two errors will be raised if the JSON file is not consisten with the
        # format expected.
        raise ValidationError(
            """This is not the expected file format. Please check
    that you are uploading a 'StreamingHistory' file."""
        )
    except Exception as e:
        # TODO logger.exception("File upload was not completed and raised an Exception.")
        raise e
