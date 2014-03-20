from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

#from rating.utility import parseInt
#from django.conf import settings


### TODO
# Remove column old_id from rating_pptunit (refers to id in ppt db)

class Ppt(models.Model):

    # Processing status
    STATUS = (
                (u'0', u'Not processed'),
                (u'1', u'Started'),
                (u'2', u'Converted'),
                (u'E', u'Error'),
        )

    # Only allow alpha, numeric, _, and . in filename w max len of 100
    def getuploadedpath(self, filename):
        filename, ext = os.path.splitext(filename)
        if not (ext.upper() == '.PPT' or ext.upper() == '.PPTX'):
            ext = '.ppt'

        filename = filename.replace(' ', '_')
        valid = '_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        filename = ''.join(c for c in filename if c in valid)

        return 'pptfile/%s/%s/%s' % (self.user_id, self.id, filename[:96] + ext)

    title = models.CharField(max_length=240)
    filename = models.CharField(max_length=240)
    folder = models.CharField(max_length=240)
    rnd = models.IntegerField()
    source_url = models.CharField(max_length=240)
    
    unit_id = models.IntegerField()  # OLD, use m2m reference now.
    user = models.ForeignKey(User)

    file = models.FileField(upload_to=getuploadedpath)
    jpg_export_status = models.CharField(max_length=1, choices=STATUS, default='0')
    jpg_parse_version = models.SmallIntegerField(blank=True)
    html_export_status = models.CharField(max_length=1, choices=STATUS, default='0')
    html_parse_version = models.SmallIntegerField(blank=True)

    slide_title_avg_length = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    slide_points_FleschKincaidGradeLevel = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    slide_words_sum = models.IntegerField(blank=True, null=True)

    def jpgs(self):
        jpg = '%suserfiles/pptfile/%s/%s/jpg/' % (settings.PPT_FILEPATH, self.user_id, self.id)
        username = self.user.username
        print jpg
        if not os.path.exists(jpg):
            print 'not'
            return []
        
        jpgs = []
        for j in os.listdir(jpg):
            if j[-3:] == 'JPG':
                jpgs.append('/user/%s/ppt/%s/jpg/%s' % (username, self.id, j))
        
        return jpgs
    
    def get_absolute_url(self):
        return '/user/%s/ppt/%s/' % (self.user.username, self.id)
    
    def get_absolute_filepath(self):
        return '%suserfiles/%s' % (settings.PPT_FILEPATH, self.file.name)
    
    def __unicode__(self):
        return "<Ppt %s, %s,%s>" % (self.id, self.folder, self.filename)


# Model for storing results of parsing html
class PptJpg(models.Model):
    md5 = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    entropy = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    height = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    
    ppt = models.ForeignKey(Ppt)
    
    def get_absolute_path(self, user=None):
        if user == None:
            user = self.ppt.user
        
        return "%s/userfiles/pptfile/%s/%s/jpg/%s" % (
                settings.PPT_FILEPATH, user.id, self.ppt_id, self.filename)
    
    def get_absolute_url(self, user=None):
        if user == None:
            user = self.ppt.user
        
        return "/user/%s/ppt/%s/jpg/%s" % (user.username, self.ppt_id, self.filename)
    
    def __unicode__(self):
        return '<PptJpg %s, %s, %s>' % (self.id, self.filename, self.ppt)


# Model for storing results of parsing html
class PptHtmlImage(models.Model):
    md5 = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    size = models.IntegerField()
    height = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    entropy = models.DecimalField(max_digits=9, decimal_places=5, blank=True, null=True)
    template = models.BooleanField()
    vector = models.BooleanField()
    
    ppt = models.ForeignKey(Ppt)
    
    def get_absolute_url(self):
        user = self.ppt.user
        return "/user/%s/ppt/%s/img/%s" % (user.username, self.ppt_id, self.filename)

    def get_absolute_path(self, user=None):
        if user == None:
            user = self.ppt.user
        
        return "%s/userfiles/pptfile/%s/%s/html_files/%s" % (
                settings.PPT_FILEPATH, user.id, self.ppt_id, self.filename)
    
    # Is the passed image a vector type?
    def filename_is_vector(self, filename=None):
        filename, ext = os.path.splitext(filename or self.filename)
        return ext in ['.wmz', '.emz', '.pcz']

    def __unicode__(self):
        return '<PptHtmlImage %s, %s, %s>' % (self.id, self.filename, self.ppt)


# Model for storing results of parsing html
class PptHtmlPage(models.Model):
    HTML_TYPES = (
                (u'M', u'Master'),
                (u'S', u'Slide'),
                (u'O', u'Outline'),
        )
    
    md5 = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    pagetype = models.CharField(max_length=1, choices=HTML_TYPES)
    html = models.TextField()
    title = models.TextField()
    order = models.IntegerField(blank=True)

    ppt = models.ForeignKey(Ppt)
    # note: not all html slides have a corresponding jpg slide.  if a slide is empty, it doesn't always
    # get exported as an image.
    pptjpg = models.ForeignKey(PptJpg, blank=True)

    # Setting the jpg reference requires having an order.  The filename doesn't tell us anything about the
    # order of the slides, as they can be re-arranged, deleted, etc...  Relies upon knowing order from the
    # parser looking at the outline file.
    def setjpg(self):

        if self.pptjpg_id is None and not self.order is None:
            filename = 'Slide%s.JPG' % self.order
            jpg = PptJpg.objects.filter(ppt_id=self.ppt_id, filename=filename)
            if len(jpg) > 0:
                self.pptjpg = jpg[0]

    def get_absolute_url(self):
        user = self.ppt.user
        return "/user/%s/ppt/%s/img/%s" % (user.username, self.ppt_id, self.filename)
    
    def __unicode__(self):
        return '<PptHtmlPage %s, %s, %s, %s>' % (self.id, self.pagetype, self.filename, self.ppt)


# Model for storing parsed points from the outline file.
class PptHtmlPagePoint(models.Model):
    text = models.TextField()
    order = models.IntegerField()
    ppthtmlpage = models.ForeignKey(PptHtmlPage)

    def __unicode__(self):
        return '<PptHtmlPagePoint %s, %s, %s>' % (self.id, self.text, self.ppthtmlpage)


# Model for storing results of parsing html
class PptHtmlPageSrc(models.Model):
    ppthtmlpage = models.ForeignKey(PptHtmlPage)
    ppthtmlimage = models.ForeignKey(PptHtmlImage)
    
    pos_left = models.IntegerField()
    pos_width = models.IntegerField()
    pos_top = models.IntegerField()
    pos_height = models.IntegerField()
    
    def get_absolute_url(self):
        return self.ppthtmlimage.get_absolute_url()
    
    def __unicode__(self):
        return '<PptHtml %s>' % (self.id)


# Model for storing results of parsing html
class PptHtmlPageText(models.Model):
    md5 = models.CharField(max_length=255)
    text = models.TextField()
    
    pos_left = models.IntegerField()
    pos_width = models.IntegerField()
    pos_top = models.IntegerField()
    pos_height = models.IntegerField()
    
    ppthtmlpage = models.ForeignKey(PptHtmlPage)
    
    def __unicode__(self):
        return '<PptHtml %s>' % (self.id)


class PptUnit(models.Model):
    UNIT_TYPES = (
            (u'Experiment', u'Experiment'),
            (u'Book', u'Book'),
            (u'Website', u'Website'),
            (u'PearsonBookFile', u'PearsonBookFile'),
            (u'MoodleCourse', u'MoodleCourse'),
    )
    title = models.CharField(max_length=200, db_index=True)
    unittype = models.CharField(max_length=254, choices=UNIT_TYPES, blank=True)
    description = models.TextField()
    url = models.TextField(blank=True)

    ppts = models.ManyToManyField(Ppt, blank=True)

    def get_absolute_url(self):
        return '/unit/%s/' % (self.id,)

    def __unicode__(self):
        return "<PptUnit %s, %s >" % (self.id, self.title)


class PptUnitTag(models.Model):
    unit = models.ForeignKey(PptUnit)
    tag = models.CharField(max_length=200, db_index=True)

    def get_absolute_url(self):
        return '/tag/%s/' % (self.tag,)

    def __unicode__(self):
        return "<PptUnitTag %s %s>" % (self.unit, self.tag)


class PptTag(models.Model):
    ppt = models.ForeignKey(Ppt)
    tag = models.CharField(max_length=200, db_index=True)
    
    def get_absolute_url(self):
        return '/tag/%s/' % (self.tag,)
    
    def __unicode__(self):
        return "<PptTag %s %s>" % (self.ppt, self.tag)


class PptRating(models.Model):
    RATING_CHOICES = (
        (0, u''),
        (1, u'Strongly Agree'),
        (2, u'Agree'),
        (3, u'Neutral'),
        (4, u'Disagree'),
        (5, u'Strongly Disagree'),
    )
    
    ratedate = models.DateTimeField('date rated', auto_now=True)
    empty = models.BooleanField()
    contentimage = models.IntegerField(choices=RATING_CHOICES)
    contenttext = models.IntegerField(choices=RATING_CHOICES)
    slidenovel = models.IntegerField(choices=RATING_CHOICES)
    slidestudy = models.IntegerField(choices=RATING_CHOICES)
    slidequality = models.IntegerField(choices=RATING_CHOICES)
    slideinteresting = models.IntegerField(choices=RATING_CHOICES)
    
    user = models.ForeignKey(User)
    ppt = models.ForeignKey(Ppt)
    
    def get_absolute_url(self):
        return self.ppt.get_absolute_url()
    
    def __unicode__(self):
        return "<PptRating ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)


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


