from django import forms
from django.forms import ModelForm

from django.forms.widgets import RadioSelect
from rating.models import *


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


# Create a form for creating ratings
class PptRatingForm(ModelForm):
    RATING_CHOICES = (
        (1, u'Strongly Agree'),
        (2, u'Agree'),
        (3, u'Neutral'),
        (4, u'Disagree'),
        (5, u'Strongly Disagree'),
        (0, u'Unknown or NA'),
    )
    
    contentimage = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            initial=1,
            label='These slides have a lot of images')
    contenttext = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            label='These slides have a lot of text')
    slidenovel = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            label='These slides would help me stay interested during class')
    slidestudy = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            label='These slides would help me prepare for class or study for tests')
    slidequality = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            label='These slides are professional quality')
    slideinteresting = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            label='These slides are interesting')
    
    class Meta:
        model = PptRating
        exclude = ('user', 'ppt', 'ratedate', 'empty')


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
