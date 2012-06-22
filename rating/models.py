from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

from rating.utility import parseInt
from django.conf import settings

if False:
	class Unit(models.Model):
		UNIT_TYPES = (
				(u'Book', u'Book'),
				(u'Website', u'Website'),
				(u'PearsonBookFile', u'PearsonBookFile'),
				(u'MoodleCourse', u'MoodleCourse'),
		)
		
		title = models.CharField(max_length=254)
		unittype = models.CharField(max_length=254, choices=UNIT_TYPES)
		
		def __unicode__(self):
			return "<Unit %s, %s,%s>" % (self.id, self.title, self.unittype)


class Ppt(models.Model):
	filename = models.CharField(max_length=240)
	folder = models.CharField(max_length=240)
	rnd = models.IntegerField()
	source_url = models.TextField()
	
	unit_id = models.IntegerField() #models.ForeignKey(Unit)
	user = models.ForeignKey(User)
	
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
	
	def __unicode__(self):
		return "<Ppt %s, %s,%s>" % (self.id, self.folder, self.filename)


# File for an uploaded ppt 
class PptUploadedFile(models.Model):
	STATUS = (
				(u'0', u'Not processed'),
				(u'1', u'Started'),
				(u'E', u'Error'),
				(u'2', u'Converted'),
		)
	
	# Only allow alpha, numeric, and . in filename w max len of 70
	def getuploadedpath(instance, filename):
		valid = '.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
		filename = ''.join(c for c in filename if c in valid)
		filename = filename[:70] 
		return 'pptfile/%s/%s/%s' % (instance.ppt.user_id, instance.ppt.id, filename )
	
	ppt = models.ForeignKey(Ppt)
	file = models.FileField(upload_to=getuploadedpath)
	
	exported_to_jpg = models.CharField(max_length=1, choices=STATUS)
	exported_to_html = models.CharField(max_length=1, choices=STATUS)
	
	
	def __unicode__(self):
		return '<PptUploadedFile %s, %s, %s>' % (self.id, self.ppt.id, self.ppt.user.username)


# Model for storing results of parsing html
class PptJpg(models.Model):
	parseVersion = models.SmallIntegerField()
	md5 = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)
	size = models.IntegerField()
	height = models.IntegerField()
	width = models.IntegerField()
	
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
	parseVersion = models.SmallIntegerField()
	md5 = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)
	size = models.IntegerField()
	height = models.IntegerField()
	width = models.IntegerField()
	
	ppt = models.ForeignKey(Ppt)
	
	def get_absolute_url(self):
		user = self.ppt.user
		return "/user/%s/ppt/%s/img/%s" % (user.username, self.ppt_id, self.filename)
	
	def __unicode__(self):
		return '<PptHtmlImage %s, %s, %s>' % (self.id, self.filename, self.ppt)


# Model for storing results of parsing html
class PptHtmlPage(models.Model):
	parseVersion = models.SmallIntegerField()
	HTML_TYPES = (
				(u'M', u'Master'),
				(u'S', u'Slide'),
				(u'O', u'Outline'),
		)
	
	md5 = models.CharField(max_length=255)
	filename = models.CharField(max_length=255)
	pagetype = models.CharField(max_length=1, choices=HTML_TYPES)
	html = models.TextField()
	ppt = models.ForeignKey(Ppt)
	
	_cache = None

	def jpg(self):
		if self._cache == None: self._cache = {}

		if '_jpg' not in self._cache:
			filename = 'Slide%s.JPG' % self.order()
			jpg = PptJpg.objects.filter(ppt_id=self.ppt_id,filename=filename)
			if len(jpg) > 0:
				self._cache['jpg'] = jpg[0]
			else:
				self._cache['jpg'] = None

		return self._cache['jpg']


	def order(self):
		return parseInt(self.filename)
	
	def get_absolute_url(self):
		user = self.ppt.user
		return "/user/%s/ppt/%s/img/%s" % (user.username, self.ppt_id, self.filename)
	
	def __unicode__(self):
		return '<PptHtmlPage %s, %s, %s, %s>' % (self.id, self.pagetype, self.filename, self.ppt)


# Model for storing results of parsing html
class PptHtmlPageSrc(models.Model):
	parseVersion = models.SmallIntegerField()
	
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
	parseVersion = models.SmallIntegerField()
	md5 = models.CharField(max_length=255)
	text = models.TextField()
	
	pos_left = models.IntegerField()
	pos_width = models.IntegerField()
	pos_top = models.IntegerField()
	pos_height = models.IntegerField()
	
	ppthtmlpage = models.ForeignKey(PptHtmlPage)
	
	def __unicode__(self):
		return '<PptHtml %s>' % (self.id)



class PptTag(models.Model):
	ppt = models.ForeignKey(Ppt)
	tag = models.CharField(max_length=200, db_index=True)
	
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

