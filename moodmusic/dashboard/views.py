from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def dashboard(request):
    return render(request, "dashboard/dashboard.html", {})


def thanks(request):
    return render(request, "dashboard/thanks.html", {})


def spotify(request):
    return render(request, "dashboard/spotify-connect.html", {})


def datadrop(request):
    return render(request, "dashboard/data-drop.html", {})


def mobile_guide(request):
    return render(request, "dashboard/mobile-surveys.html", {})
