from django import forms
from django.forms import ModelForm

from django.forms.widgets import RadioSelect
from ppt.models import *
from exp1.models import *

# Surveys
class PptInitialSurvey1(ModelForm):
    
    class Meta:
        model = PptInitialSurvey1
        exclude = ('user', 'ppt', 'ratedate')

class PptPostSlideSurvey1(ModelForm):
    
    class Meta:
        model = PptPostSlideSurvey1
        exclude = ('user', 'ppt', 'ratedate')


class PptTopicA(ModelForm):
    
    class Meta:
        model = PptTopicA
        exclude = ('user', 'ppt', 'ratedate')

class PptTopicB(ModelForm):
    
    class Meta:
        model = PptTopicB
        exclude = ('user', 'ppt', 'ratedate')

class PptTopicC(ModelForm):
    
    class Meta:
        model = PptTopicC
        exclude = ('user', 'ppt', 'ratedate')

class PptTopicD(ModelForm):
    
    class Meta:
        model = PptTopicD
        exclude = ('user', 'ppt', 'ratedate')

class PptTopicE(ModelForm):
    
    class Meta:
        model = PptTopicE
        exclude = ('user', 'ppt', 'ratedate')
