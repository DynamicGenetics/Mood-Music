"""Views that control the phone number verification process, using Twilio's Verify API.

These views will request an authentication code from the API for the number the user
provides, and the use the API again the verify that the user provided code is as excepted.

Further documentation about the Verify API is available here: https://www.twilio.com/docs/verify/api.

The file moodmusic/dashboard/twilio_client.py contains the authentication codes for the API calls."""

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django.http import HttpResponseRedirect

from moodmusic.dashboard.twilio_client import verification_checks, verifications
from moodmusic.dashboard.forms import TokenForm


class PhoneVerificationView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ["phone_number"]
    template_name = "dashboard/phone-verification.html"

    def get_form(self, form_class=None):
        form = super(PhoneVerificationView, self).get_form(form_class)
        # This widget defaults to a UK number, unless a country code is specified
        form.fields["phone_number"].widget = PhoneNumberInternationalFallbackWidget()
        return form

    def form_valid(self, form):
        self.request.session["phone_number"] = form.cleaned_data["phone_number"].as_e164
        # Send the phone number to Twilio to generate a verification code
        verifications(form.cleaned_data["phone_number"].as_e164, via="sms")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        # NB this is really important for authorisation!
        # Makes sure that only the logged in user's number is shown.
        return self.request.user

    def get_success_url(self):
        return reverse("dashboard:token_validation")


phone_verification = PhoneVerificationView.as_view()


@login_required
def token_validation(request):
    if request.method == "POST":
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = verification_checks(
                request.session["phone_number"], form.cleaned_data["token"]
            )

            if verification.status == "approved":
                request.session["is_verified"] = True
                # Update user record in the database
                request.user.phone_verified = True
                request.user.save()
                return redirect("dashboard:verified")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    """Sorry, that token was not correct. Please try again, or go back
                        to check your phone number is correct.""",
                )
                HttpResponseRedirect(request.path_info)
    else:
        form = TokenForm()
    return render(request, "dashboard/token-validation.html", {"form": form})


@login_required
def verified(request):
    """View to confirm to user that their number is verified"""
    # If the request doesn't contain the expected payload just redirect
    if "is_verified" in request.session:
        if request.session["is_verified"]:
            return render(request, "dashboard/verified.html")
    else:
        return redirect("dashboard:phone_verification")
