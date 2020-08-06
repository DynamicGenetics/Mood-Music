from .models import EMAQuestion
from django.forms import ModelForm


class EMAQuestionForm(ModelForm):

    class Meta:
        model = EMAQuestion
        fields = ['happiness', 'energy']
