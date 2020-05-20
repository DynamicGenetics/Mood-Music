from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html', {})

def thanks(request):
    return render(request, 'thanks.html', {})