from django import forms
from django.forms import ModelForm

from django.forms.widgets import RadioSelect
from rating.models import *


ppts = Ppt.objects.filter(user_id=1)

for p in ppts:
    if p.jpg_export_status == 'E':
        p.jpg_export_status = 0
        p.html_export_status = 0
        p.jpg_parse_version = None
        p.html_parse_version = None
        p.file = p.getuploadedpath(p.file.name)
        p.save()
        print p.file.name


# Process a new file
class PptForm(ModelForm):

    file = forms.FileField(
            label='Upload a file',
            help_text='max. 42 megabytes'
    )
    #units = forms.ModelMultipleChoiceField(queryset=PptUnit.objects.all())
    units = forms.ModelMultipleChoiceField(queryset=PptUnit.objects.filter(title='OSCON 2012'))
    
    class Meta:
        model = Ppt
        exclude = ('user', 'filename', 'folder', 'rnd', 'unit_id', \
            'jpg_export_status', 'html_export_status', \
            'jpg_parse_version', 'html_parse_version')


# Create a form for creating ratings
class PptClassifyImageForm(ModelForm):
    RATING_CHOICES = (
        (u'None', u'None'),  # not categorized
        (u'Chart', u'C(h)art'),
        (u'Code', u'(C)ode'),  # code sample
        (u'Fluff Image', u'(F)luff Image'),  # Pretty, but no additional meaning to text
        (u'Design Element', u'(D)esign Element'),  # Making things pretty/layout
        (u'Diagram/Illustration', u'(a) Diagram/Illustration'),  # Visual representative of idea beyond restating text
        (u'Equation', u'(E)quation'),
        (u'Table', u'(T)able'),
        (u'Text', u'Te(x)t'),  # Text mis-categorized as an image.
        (u'Screenshot', u'(S)creenshot'),  # print-screen
        (u'Picture', u'(P)icture'),  # Useful picture
        (u'z Recode', u'Recode'),
    )
    
    classification = forms.ChoiceField(widget=RadioSelect,
            choices=RATING_CHOICES,
            initial='None',
            label='Image classification')
    
    class Meta:
        model = PptHtmlImage
        fields = ('classification', 'id', 'filename')


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
