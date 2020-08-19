from .models import Assessment
from .forms import EMAQuestionForm

from django.shortcuts import render, render_to_response


# Create your views here.

# TODO: figure out how to link the user
def setup_sms(request):
    # aspasas
    assessment = Assessment(user=request.user)
    assessment.save()


def ema_question(request):
    if request.method == "POST":
        form = EMAQuestionForm(data=request.POST)
        form.save()
        return render_to_response("")  # TBD
    else:  # GET
        form = EMAQuestionForm()
        return render_to_response("ema_question.html", {"form": form})
