from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm


User = get_user_model()


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomSignupForm(SignupForm):
    # These are form items that aren't saved to a model instance.
    # However, we need people to indicate that they have understood before continuing.
    seen_information = forms.BooleanField(
        initial=False,
        required=True,
        label="""I have read and understood the information sheet and had the opportunity to ask the researcher
         any questions and/or to discuss any concerns.""",
    )
    voluntary_participation = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that my participation is voluntary and that I am free to withdraw at any time
         without giving any reason, and without any implication for my legal rights.""",
    )
    data_unwithdrawable = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that once my data have been anonymised, and my personal data deleted at the end
         of the study, it may not be possible to remove my data if I wish to withdraw.""",
    )
    data_collected = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that the research team will collect and store my Spotify listening history, my answers
         to the short daily surveys, and my answers to surveys I complete at the beginning of the study.""",
    )
    confidentiality = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that the information I give will be kept strictly confidential. My consent depends on the
         University of Bristol complying with its duties and obligations under
         General Data Protection Regulations 2018.""",
    )
    data_access = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that only members of the research team will have access to my personal, identifiable
         data, and that it will be destroyed after the study has concluded.""",
    )
    data_stored_longterm = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that my anonymised data will be held in a controlled research data repository and understand
     that my name or other identifying information will NOT be included.""",
    )
    could_be_reused = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that my anonymised data could be used by other researchers in publications stemming from
     this work, or for teaching and policy purposes.""",
    )
    breaking_confidentiality = forms.BooleanField(
        initial=False,
        required=True,
        label="""I understand that confidentiality may need to be broken if there is a concern about serious harm to
     myself or others.""",
    )
    consent_granted = forms.BooleanField(
        initial=False,
        required=True,
        label="""I give my full consent for taking part in this research study.""",
    )

    name = forms.CharField(max_length=30, label="Full Name")

    # Specify the first couple of fields in this order. This appear at the top,
    # and then any unspecified fields are below.
    field_order = ["name", "email", "password1", "password2"]

    def save(self, request):
        # Instructions https://django-allauth.readthedocs.io/en/latest/forms.html
        user = super(CustomSignupForm, self).save(request)

        user.name = self.cleaned_data["name"]
        # Note that email is saved through adapters.py to restrict non bristol addresses
        user.email = self.cleaned_data["email"]
        user.consent_granted = self.cleaned_data["consent_granted"]
        user.save()
        return user
