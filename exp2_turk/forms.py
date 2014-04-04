from django import forms
from django.forms import ModelForm

from django.forms.widgets import RadioSelect
from ppt.models import *
from exp2_turk.models import *

# Surveys
class PptExp2TurkPostSurvey1(ModelForm):
    
    class Meta:
        model = Exp2TurkInitialSurvey1
        exclude = ('user', 'ppt', 'ratedate')
      
class Exp2TurkPostSurvey1(ModelForm):
    
    class Meta:
        model = Exp2TurkPostSurvey1
        exclude = ('user', 'ppt', 'ratedate')