from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .twilio_client import verification_checks, verifications
from .forms import TokenForm


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
def datadrop(request):
    return render(request, "dashboard/data-drop.html", {})


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
    if not request.session["is_verified"]:
        return redirect("dashboard:phone_verification")
    return render(request, "dashboard/verified.html")
