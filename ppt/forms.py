from django import forms
from django.forms import ModelForm

from django.forms.widgets import RadioSelect
from ppt.models import *


# Process a new file
class PptForm(ModelForm):

#
#    file = forms.FileField(
#            label='Upload a file',
#            help_text='max. 42 megabytes'
#    )
#    units = forms.ModelMultipleChoiceField(queryset=PptUnit.objects.filter(unittype='Experiment'))
    
    class Meta:
        model = Ppt
        fields = ('pptfile', 'title','description', 'pptunit')
