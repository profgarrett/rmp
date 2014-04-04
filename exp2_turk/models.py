from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os


from ppt.models import *


class Exp2TurkInitialSurvey1(models.Model):
    INFORM_CHOICES = (
        (1, u'Very Uninformed'),
        (2, u'Moderately Uninformed'),
        (3, u'Slightly Uninformed'),
        (4, u'Slightly Informed'),
        (5, u'Moderately Informed'),
        (6, u'Very Informed'),
    )

    INTEREST_CHOICES = (
        (0, u'Do not know what this is'),
        (1, u'Very Uninterested'),
        (2, u'Moderately Uninterested'),
        (3, u'Slightly Uninterested'),
        (4, u'Slightly Interested'),
        (5, u'Moderately Interested'),
        (6, u'Very Interested'),
    )

    AGREE7_CHOICES = (
        (1, u'Strongly Disagree'),
        (2, u'Moderately Disagree'),
        (3, u'Slightly Disagree'),
        (4, u'Neutral'),
        (5, u'Slightly Agree'),
        (5, u'Moderately Agree'),
        (7, u'Strongly Agree'),
    )
    
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)

    # Rate Knowledge
    informwikipediation = models.IntegerField(choices=INFORM_CHOICES, help_text="Rate your knowledge in the following topics", verbose_name='Wikipedia')
    informebook = models.IntegerField(choices=INFORM_CHOICES,help_text="Rate your knowledge in the following topics", verbose_name='e-books on Amazon Kindle')
    informselfpublish = models.IntegerField(choices=INFORM_CHOICES,  help_text="Rate your knowledge in the following topics",verbose_name='Self-publishing a novel')
    informcouchsurfing = models.IntegerField(choices=INFORM_CHOICES,  help_text="Rate your knowledge in the following topics",verbose_name='Couchsurfing')
    informandroidapp = models.IntegerField(choices=INFORM_CHOICES,  help_text="Rate your knowledge in the following topics",verbose_name='Creating an Android app')
    
    # Rate Interest
    interestwikipediacosts = models.IntegerField(choices=INTEREST_CHOICES, help_text="Rate your interest in the following topics", verbose_name='How much Wikipedia costs to run')
    interestviewebook = models.IntegerField(choices=INTEREST_CHOICES, help_text="Rate your interest in the following topics", verbose_name='How consumers view e-books')
    interestselfpublish = models.IntegerField(choices=INTEREST_CHOICES, help_text="Rate your interest in the following topics", verbose_name='How to self-publish your own book')
    interesttravel = models.IntegerField(choices=INTEREST_CHOICES, help_text="Rate your interest in the following topics", verbose_name="Travel on the cheap by visiting people's homes")
    interestapp = models.IntegerField(choices=INTEREST_CHOICES, help_text="Rate your interest in the following topics", verbose_name='Ceating your own app for mobile phones')
    
    # PowerPoint
    pptlearn = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="The use of PowerPoint is helpful in increasing learning in the classroom ")
    pptinterest = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="The use of PowerPoint increases student interest (entertainment value) of a college class ")
    pptgrade = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="The use of PowerPoint can help a student get a better grade in the class ")

    ppttext = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I generally prefer slides that provide full text of the lecture material (i.e., everything the professor wants me to know is completely written out on the slide)")
    pptread = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I find it helpful for professors to read the PowerPoint slides as they are presented")
    pptboring = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I find it boring when the professor says the same things the PowerPoint slides say ")
    pptdiscussion = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I find it helpful for professors to use the PowerPoint slides as discussion points for the lectures ")
    pptkeyphrases = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I generally prefer slides that provide key phrase outlines of the lecture material ")

    pptvisual = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I generally find visual elements (e.g., pictures/charts/graphics/maps) helpful in PowerPoint presentations")
    pptnotext = models.IntegerField(choices=AGREE7_CHOICES, help_text="PowerPoint", verbose_name="I prefer slides that contain pictures, graphs, charts, or maps only")
    
    def get_absolute_url(self):
        return '/survey/Exp2TurkInitialSurvey1/$s' % (self.id)
    
    def __str__(self):
        return "<Exp2TurkInitialSurvey1 (%s, %s, %s )" % (self.id, self.ratedate, self.user.username)


class Exp2TurkPostSurvey1(models.Model):
    AVERAGE5_CHOICES = (
        (1, u'Poor'),
        (2, u'Below Average'),
        (3, u'Average'),
        (4, u'Above Average'),
        (5, u'Excellent'),
    )

    ALWAYS5_CHOICES = (
        (1, u'Hardly ever'),
        (2, u'Occasionally'),
        (3, u'Sometimes'),
        (4, u'Frequently'),
        (5, u'Almost always'),
    )

    AGREE7_CHOICES = (
        (0, u''),
        (1, u'Strongly Disagree'),
        (2, u'Moderately Disagree'),
        (3, u'Slightly Disagree'),
        (4, u'Neutral'),
        (5, u'Slightly Agree'),
        (5, u'Moderately Agree'),
        (7, u'Strongly Agree'),
    )

    EFFECTIVE6_CHOICES = (
        (1, u'Very infeffective'),
        (2, u'Moderately infeffective'),
        (3, u'Slightly Ineffective'),
        (4, u'Slightly Effective'),
        (5, u'Moderately Effective'),
        (6, u'Very Effective'),
    )

    EFFECTIVE7_CHOICES = (
        (1, u'Very infeffective'),
        (2, u'Moderately infeffective'),
        (3, u'Slightly Ineffective'),
        (4, u'Neutral'),
        (5, u'Slightly Effective'),
        (6, u'Moderately Effective'),
        (7, u'Very Effective'),
    )
    
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)

    # Overall
    overallpresentation = models.IntegerField(choices=AVERAGE5_CHOICES, verbose_name='Rate the presentation overall ')    
    overallinstructor = models.IntegerField(choices=AVERAGE5_CHOICES, verbose_name='Rate the instructor overall')    

    # Instructor
    instructorclear = models.IntegerField(choices=ALWAYS5_CHOICES, verbose_name='The speaker explained material clearly ')    
    instructorfocus = models.IntegerField(choices=EFFECTIVE7_CHOICES, verbose_name='It was easy for me personally to stay focused on the material ')    
    instructorinterest = models.IntegerField(choices=EFFECTIVE7_CHOICES, verbose_name='The instructor was effective in maintaining my interest in the material ')    

    # PowerPoint
    ppteffective = models.IntegerField(choices=EFFECTIVE6_CHOICES, verbose_name='How effective was the PowerPoint')    
    pptkey = models.IntegerField(choices=EFFECTIVE6_CHOICES, verbose_name='The PowerPoint emphasized key points during the lecture')    
    pptremember = models.IntegerField(choices=EFFECTIVE6_CHOICES, verbose_name='The PowerPoint resulted in information being easier to remember ')    
    pptexamples = models.IntegerField(choices=EFFECTIVE6_CHOICES, verbose_name='The PowerPoint made examples presented clearer ')    
    ppttextrecall = models.IntegerField(choices=EFFECTIVE6_CHOICES, verbose_name='The PowerPoint text will help me recall content ')    
    pptimagerecall = models.IntegerField(choices=EFFECTIVE6_CHOICES, verbose_name='The PowerPoint visual images will help me recall content  ')    

    # Questions
    q1 = models.IntegerField(
        verbose_name='Createspace does which of the following?',
        choices=(
            (1, u'Prints physical books for independent authors'),
            (2, u'Creates audiobooks for independent authors'),
            (3, u'Creates digital books for independent authors'),
            (4, u'Sells books created by regular publishers'),))
    q2 = models.IntegerField(
        verbose_name='What is the primary benefit of publishing on CreateSpace or Amazon Kindle?',
        choices=(
            (1, u'Author control & convenience'),
            (2, u'Book quality control'),
            (3, u'Distribution to real bookstores'),
            (4, u'Access to reviewers'),))
    q3 = models.IntegerField(
        verbose_name='How hard is it to self-publish on Amazon Kindle or CreateSpace?',
        choices=(
            (1, u'Very easy, anyone can do it'),
            (2, u'Easy, but requires a lot of technical knowhow'),
            (3, u'Difficult, you need Amazon to approve your book'),
            (4, u'Very difficult, you need a publisher to approve your book'),))
    q4 = models.IntegerField(
        verbose_name='Which of the following steps does publishing on Kindle/CreateSpace require?',
        choices=(
            (1, u'Literary Agent'),
            (2, u'Review by editor'),
            (3, u'Printing '),
            (4, u'None of the above'),))
    q5 = models.IntegerField(
        verbose_name='Choose the best summary of the presentation',
        choices=(
            (1, u'Self-publishing is available for the technically-minded authors'),
            (2, u'Self-publishing will expand the traditional publishing market'),
            (3, u'Self-publishing will destroy the traditional book market '),
            (4, u'Self-publishing is affordable, easy, and accessible'),))

    
    def get_absolute_url(self):
        return '/survey/Exp2TurkPostSurvey1/$s' % (self.id)
    
    def __str__(self):
        return "<Exp2TurkPostSurvey1 ('%s', '%s', %s )" % (self.id, self.user.username, self.ppt.filename)