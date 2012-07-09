from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

from rating.utility import parseInt
from django.conf import settings


### TODO
# Remove column old_id from rating_pptunit (refers to id in ppt db)

class Ppt(models.Model):
	filename = models.CharField(max_length=240)
	folder = models.CharField(max_length=240)
	rnd = models.IntegerField()
	source_url = models.CharField(max_length=240)
	
	unit_id = models.IntegerField() # OLD, use m2m reference now. 
	user = models.ForeignKey(User)

	STATUS = (
				(u'0', u'Not processed'),
				(u'1', u'Started'),
				(u'2', u'Converted'),
				(u'E', u'Error'),
		)

	
	# Only allow alpha, numeric, _, and . in filename w max len of 100
	def getuploadedpath(instance):
		filename, ext = os.path.splitext(filename)
		if not (ext.upper() == '.PPT' or ext.upper() == '.PPTX'): ext = '.ppt' 

		filename = filename.replace(' ', '_')
		valid = '_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
		filename = ''.join(c for c in filename if c in valid)

		return filename[:96] + ext

	file = models.FileField(upload_to=getuploadedpath)
	jpg_export_status = models.CharField(max_length=1, choices=STATUS, default='0')
	jpg_parse_version = models.SmallIntegerField(blank=True)
	html_export_status = models.CharField(max_length=1, choices=STATUS, default='0')
	html_parse_version = models.SmallIntegerField(blank=True)
	
	def jpgs(self):
		jpg = '%suserfiles/pptfile/%s/%s/jpg/' % (settings.PPT_FILEPATH, self.user_id, self.id )
		username = self.user.username
		
		if not os.path.exists(jpg):
			return []
		
		jpgs = []
		for j in os.listdir(jpg):
			if j[-3:] == 'JPG': jpgs.append('/user/%s/ppt/%s/jpg/%s' % (username,self.id,j))
		
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
	height = models.IntegerField(blank=True)
	width = models.IntegerField(blank=True)
	
	ppt = models.ForeignKey(Ppt)
	
	def get_absolute_path(self, user=None):
		if user==None:
			user = self.ppt.user
		
		return "%s/userfiles/pptfile/%s/%s/jpg/%s" % (
				settings.PPT_FILEPATH, user.id, self.ppt_id, self.filename)
	
	def get_absolute_url(self, user=None):
		if user==None:
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
	template = models.BooleanField()
	vector = models.BooleanField()
	
	ppt = models.ForeignKey(Ppt)
	
	def get_absolute_url(self):
		user = self.ppt.user
		return "/user/%s/ppt/%s/img/%s" % (user.username, self.ppt_id, self.filename)
	
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
			jpg = PptJpg.objects.filter(ppt_id=self.ppt_id,filename=filename)
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
			(u'Book', u'Book'),
			(u'Website', u'Website'),
			(u'PearsonBookFile', u'PearsonBookFile'),
			(u'MoodleCourse', u'MoodleCourse'),
	)
	title = models.CharField(max_length=200, db_index=True)
	unittype = models.CharField(max_length=254, choices=UNIT_TYPES, blank=True)
	description = models.TextField()
	url = models.TextField()

	ppts = models.ManyToManyField(Ppt)

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
	
	ratedate = models.DateTimeField('date rated',auto_now=True)
	empty = models.BooleanField()
	contentimage = models.IntegerField(choices=RATING_CHOICES)
	contenttext = models.IntegerField(choices=RATING_CHOICES)
	slidenovel = models.IntegerField(choices=RATING_CHOICES)
	slidestudy = models.IntegerField(choices=RATING_CHOICES)
	slidequality= models.IntegerField(choices=RATING_CHOICES)
	slideinteresting = models.IntegerField(choices=RATING_CHOICES)
	
	user = models.ForeignKey(User)
	ppt = models.ForeignKey(Ppt)
	
	def get_absolute_url(self):
		return self.ppt.get_absolute_url()
	
	
	def __unicode__(self):
		return "<PptRating ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)

