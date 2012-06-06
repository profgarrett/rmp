from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
	
	#unit = models.ForeignKey(Unit)
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		return "<Ppt %s, %s,%s>" % (self.id, self.folder, self.filename)


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
	
	def __unicode__(self):
		return "<PptRating ('%s', '%s', '%s' )" % (self.id, self.user, self.ppt)
