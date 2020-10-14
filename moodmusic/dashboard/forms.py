from django import forms
from django.contrib.auth import get_user_model

# Set up a varb for the user model
User = get_user_model()


class BootstrapInput(forms.TextInput):
    def __init__(self, placeholder, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapInput, self).__init__(
            attrs={"class": "form-control input-sm", "placeholder": placeholder}
        )

    def bootwrap_input(self, input_tag):
        classes = "col-xs-{n} col-sm-{n} col-md-{n}".format(n=self.size)

        return """<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               """.format(
            classes=classes, input_tag=input_tag
        )

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapInput, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class BootstrapSelect(forms.Select):
    """Class from the Twilio Verify example, providing
    formatting for the VerificationForm.
    """

    def __init__(self, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapSelect, self).__init__(
            attrs={"class": "form-control input-sm",}
        )

    def bootwrap_input(self, input_tag):
        classes = "col-xs-{n} col-sm-{n} col-md-{n}".format(n=self.size)

        return """<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               """.format(
            classes=classes, input_tag=input_tag
        )

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapSelect, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class TokenForm(forms.Form):
    """Form used to input the verification token from Twilio phone number verify API.
    """

    token = forms.CharField(widget=BootstrapInput("Verification Token", size=6))
