import json
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# Set up a varb for the user model
User = get_user_model()


class TokenForm(forms.Form):
    """Form used to input the verification token from Twilio phone number verify API.
    """

    token = forms.CharField(label="Verification Token")


def validate_json(file):
    try:
        history = json.load(file)
        for song in history:
            keys = ["endTime", "artistName", "trackName", "msPlayed"]
            for key in keys:
                if key in song is False:
                    raise ValidationError(
                        "Sorry, this file does not contain the right information."
                    )
    except UnicodeDecodeError:
        raise ValidationError("Sorry, only .json files are accepted.")
    except json.decoder.JSONDecodeError:
        pass
    except (KeyError, TypeError):
        raise ValidationError(
            "Sorry, this file does not contain the right information."
        )
    except Exception:
        raise ValidationError("Sorry, this file isn't valid.")


class UploadListeningHistoryForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        # validators=[validate_json],
    )
