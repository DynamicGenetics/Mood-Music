import json
import pytest
from contextlib import contextmanager  # For does_not_raise
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase

from moodmusic.dashboard.views.data_drop import (
    validate_ext,
    handle_uploaded_file,
    save_music_history,
    DataDropView,
)
from moodmusic.music.models import FullUserHistory
from pretend_data import VALID_DATA, INVALID_DATA


User = get_user_model()

# Docs: https://docs.pytest.org/en/stable/example/parametrize.html#parametrizing-conditional-raising
@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (".pdf", pytest.raises(ValidationError)),
        (".doc", pytest.raises(ValidationError)),
        (".docx", pytest.raises(ValidationError)),
        ("", pytest.raises(ValidationError)),
        (".txt", pytest.raises(ValidationError)),
        (".json", does_not_raise()),
    ],
)
def test_validate_ext(test_input, expected):
    """Test that only .json files are accepted.
    """
    file_name = "data" + test_input
    test_file = SimpleUploadedFile(name=file_name, content=b"Some content")
    with expected:
        validate_ext(test_file)


# class TestHandleUploadedFile(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="test@bristol.ac.uk", password="12345"
#         )

#     # This is currently not working as I can't find an input format that allows
#     # me to mock the file upload????
#     def test_handle_uploaded_file(self):
#         # handle_uploaded_file(
#         #     (SimpleUploadedFile(name="data", content=INVALID_DATA)), user=self.user,
#         # )
#         # assert pytest.raises(KeyError)
#         pass

#     def test_save_music_history(self):
#         save_music_history(VALID_DATA, self.user)
#         assert FullUserHistory.objects.filter(artist="David Bowie").exists()
#         assert FullUserHistory.objects.filter(track_name="Landslide").exists()

#     def test_save_music_history_fails(self):
#         save_music_history(INVALID_DATA, self.user)
#         assert pytest.raises(KeyError)


# class TestSaveUserHistory(TestCase):
