from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
