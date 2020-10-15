import json
from datetime import datetime, timezone
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth import get_user_model
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .twilio_client import verification_checks, verifications
from .forms import TokenForm, UploadListeningHistoryForm
from moodmusic.music.models import FullUserHistory


@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html", {})


@login_required
def thanks(request):
    return render(request, "dashboard/thanks.html", {})


@login_required
def spotify(request):
    return render(request, "dashboard/spotify-connect.html", {})


@login_required
def mobile_guide(request):
    return render(request, "dashboard/mobile-surveys.html", {})


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
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, "dashboard/token-validation.html", {"form": form})


@login_required
def verified(request):
    """View to confirm to user that their number is verified"""
    if not request.session["is_verified"]:
        return redirect("dashboard:phone_verification")
    return render(request, "dashboard/verified.html")


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
    fields we are interested in to the database"""
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
