from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os


from ppt.models import *

class PptInitialSurvey1(models.Model):
    INFORM_CHOICES = (
        (0, u''),
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
        (0, u''),
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
        return '/survey/PptInitialSurvey1/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptInitialSurvey1 ('%s', '%s' )" % (self.id, self.ppt)


class PptPostSlideSurvey1(models.Model):
    AVERAGE5_CHOICES = (
        (0, u''),
        (1, u'Poor'),
        (2, u'Below Average'),
        (3, u'Average'),
        (4, u'Above Average'),
        (5, u'Excellent'),
    )

    ALWAYS5_CHOICES = (
        (0, u''),
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
        (0, u''),
        (1, u'Very infeffective'),
        (2, u'Moderately infeffective'),
        (3, u'Slightly Ineffective'),
        (4, u'Slightly Effective'),
        (5, u'Moderately Effective'),
        (6, u'Very Effective'),
    )

    EFFECTIVE7_CHOICES = (
        (0, u''),
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

    
    def get_absolute_url(self):
        return '/survey/PptPostSlideSurvey1/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptPostSlideSurvey1 ('%s', '%s' )" % (self.id, self.user)


class PptTopicA(models.Model):
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)

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
        return '/survey/PptTopicA/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptTopicA ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)



class PptTopicB(models.Model):
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)

    # Questions
    q1 = models.IntegerField(
        verbose_name='How are eBooks different from print books',
        choices=(
            (1, u'They are the same'),
            (2, u'eBooks allow for lower writing quality'),
            (3, u'eBooks last forever'),
            (4, u'eBooks are better'),))
    q2 = models.IntegerField(
        verbose_name='Do self-published eBooks',
        choices=(
            (1, u"Improve the average book's quality"),
            (2, u"Decrease the average book's quality"),
            (3, u"Have no effect on the average book's quality"),))
    q3 = models.IntegerField(
        verbose_name='Do self-published eBooks',
        choices=(
            (1, u'Increase the total number of writing niches'),
            (2, u'Decrease the number of writing niches'),
            (3, u'Have no effect'),
            (4, u''),))
    q4 = models.IntegerField(
        verbose_name='Readers believe that',
        choices=(
            (1, u'eBooks are more valuable than traditional books'),
            (2, u'eBooks are equally valuable than traditional books'),
            (3, u'eBooks are less valuable than traditional books'),))
    q5 = models.IntegerField(
        verbose_name='Kindle Singles are',
        choices=(
            (1, u'Shorter books'),
            (2, u'Have lower cost'),
            (3, u'Higher royalties'),
            (4, u'All of the above'),))
    q6 = models.IntegerField(
        verbose_name='vi.   Pricing is not based on',
        choices=(
            (1, u'Quality of writing'),
            (2, u'Marketing budget'),
            (3, u"Reader's perception of value"),
            (4, u'Length of book'),))

    def get_absolute_url(self):
        return '/survey/PptTopicB/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptTopicB ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)



class PptTopicC(models.Model):
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)

    # Questions
    q1 = models.IntegerField(
        verbose_name='Couchsurfing members are',
        choices=(
            (1, u'All over the world'),
            (2, u'Mostly in the North & South American Hemisphere'),
            (3, u'Mostly in the US & Europe'),
            (4, u'Mostly in the US'),))
    q2 = models.IntegerField(
        verbose_name="Couchsurfing's primary goal is",
        choices=(
            (1, u'Allowing house owners to rent properties'),
            (2, u'Creating small local communities'),
            (3, u'Connecting people'),
            (4, u'To help the environment by sharing cars'),))
    q3 = models.IntegerField(
        verbose_name='Courchsurfing is a',
        choices=(
            (1, u'Business'),
            (2, u'Charity'),
            (3, u'Certified B Corporation'),
            (4, u'A non-governmental charity organization'),))
    q4 = models.IntegerField(
        verbose_name='Courchsurfers emphasize',
        choices=(
            (1, u'Meeting important people internationally'),
            (2, u"Experiencing local culture & people's homes"),
            (3, u'Drinking and eating high-end cuisine'),
            (4, u'Exercising'),))
    q5 = models.IntegerField(
        verbose_name='Courchsurfers emphasize',
        choices=(
            (1, u'Internationally'),
            (2, u'Local'),
            (3, u'Local and International'),))
    q6 = models.IntegerField(
        verbose_name='Courchsurfing will',
        choices=(
            (1, u'Replace the hotel industry'),
            (2, u'Weaken the hotel industry'),
            (3, u'Help the hotel industry'),))

    def get_absolute_url(self):
        return '/survey/PptTopicC/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptTopicC ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)



class PptTopicD(models.Model):
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)

    # Questions
    q1 = models.IntegerField(
        verbose_name='What are the following are not one of the three basic types of apps?',
        choices=(
            (1, u'Data'),
            (2, u'Games'),
            (3, u'Business'),
            (4, u'Functional'),))
    q2 = models.IntegerField(
        verbose_name='What is a reasonable estimate for a game',
        choices=(
            (1, u'$3,000-8,000'),
            (2, u'$3,000-50,000'),
            (3, u'$8,000-75,000'),
            (4, u'$8,000-150,000'),))
    q3 = models.IntegerField(
        verbose_name='How much does a developer typically cost per hour?',
        choices=(
            (1, u'$25'),
            (2, u'$50'),
            (3, u'$100'),
            (4, u'$200'),))
    q4 = models.IntegerField(
        verbose_name='What approach should you not use to create your app?',
        choices=(
            (1, u'Hire a professional'),
            (2, u'Learn how yourself'),
            (3, u'Outsource overseas'),
            (4, u'Have a student do it'),))
    q5 = models.IntegerField(
        verbose_name='Which takes longer to develop',
        choices=(
            (1, u'Apple iOS Apps'),
            (2, u'Android Apps'),
            (3, u'Neither'),))
    q6 = models.IntegerField(
        verbose_name='How easy is it to create an app?',
        choices=(
            (1, u'Very easy'),
            (2, u'Very easy, but hard to have high quality'),
            (3, u'Hard, and hard to have high quality '),
            (4, u'Very hard, hire a professional!'),))
    q7 = models.IntegerField(
        verbose_name='How expensive is a professional developer',
        choices=(
            (1, u'Very expensive'),
            (2, u'Slightly more expensive'),
            (3, u'Same as a normal worker'),
            (4, u'Slightly more inexpensive'),
            (5, u'Very inexpensive'),))


    def get_absolute_url(self):
        return '/survey/PptTopicD/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptTopicD ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)



class PptTopicE(models.Model):
    ratedate = models.DateTimeField('date', auto_now=True)
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)

    # Questions
    q1 = models.IntegerField(
        verbose_name='How much does it cost to host Wikipedia?',
        choices=(
            (1, u'10-90 thousand dollars yearly'),
            (2, u'100-900 thousand dollars yearly'),
            (3, u'10-90 million dollars yearly'),
            (4, u'100-900 million dollars yearly'),))
    q2 = models.IntegerField(
        verbose_name='Which is not an example of a major cost of Wikipedia',
        choices=(
            (1, u'Bandwidth'),
            (2, u'Servers'),
            (3, u'Development of software'),
            (4, u'Paid editors'),))
    q3 = models.IntegerField(
        verbose_name='Wikipedia gets most of its revenue from',
        choices=(
            (1, u'Advertising'),
            (2, u'Donations'),
            (3, u'None, volunteer'),
            (4, u'Government'),))
    q4 = models.IntegerField(
        verbose_name="Which has been the biggest increase in Wikipedia's costs?",
        choices=(
            (1, u'Editors'),
            (2, u'Travel='),
            (3, u'Fundraising'),
            (4, u'Technical Infrastructure'),))
    q5 = models.IntegerField(
        verbose_name='How many locations does Wikipedia have?',
        choices=(
            (1, u'Only one'),
            (2, u'Two headquarters, and 2 data centers'),
            (3, u'Two in the US, and 10 overseas'),
            (4, u'100+ international data centers'),))
    q6 = models.IntegerField(
        verbose_name="Where can you find information on Wikipedia's costs?",
        choices=(
            (1, u"They are private; you can't"),
            (2, u'You have to rely on their tax reports'),
            (3, u'Only yearly audits are available'),
            (4, u'You can find them on Wikipedia'),))


    def get_absolute_url(self):
        return '/survey/PptTopicE/$s' % (self.id)
    
    def __unicode__(self):
        return "<PptTopicE ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)