from django import forms
from django.forms import ModelForm

from django.forms.widgets import RadioSelect
from ppt.models import *


# Process a new file
class PptForm(ModelForm):

    file = forms.FileField(
            label='Upload a file',
            help_text='max. 42 megabytes'
    )
    #units = forms.ModelMultipleChoiceField(queryset=PptUnit.objects.all())
    units = forms.ModelMultipleChoiceField(queryset=PptUnit.objects.filter(unittype='Experiment'))
    
    class Meta:
        model = Ppt
        exclude = ('user', 'filename', 'folder', 'rnd', 'unit_id', \
            'jpg_export_status', 'html_export_status', \
            'jpg_parse_version', 'html_parse_version')
