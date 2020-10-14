from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import ConsentForm


class ConsentView(CreateView):
    """View to display the consent form"""

    template_name = "dashboard/consent-form.html"
    form_class = ConsentForm
    success_url = reverse_lazy("accounts:signup")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


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
