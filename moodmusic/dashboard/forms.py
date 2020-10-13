from django import forms
from moodmusic.users.models import Consent


class ConsentForm(forms.ModelForm):
    class Meta:
        model = Consent
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        """Override the init method to get the user object with the request.
        This requires passing request.user when this form is called.
        """
        self.user = kwargs.pop("user", "")
        super(ConsentForm, self).__init__(*args, **kwargs)
