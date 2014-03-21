from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os


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
    description = models.TextField()
    pptfile = models.FileField(upload_to=getuploadedpath)
    jpg_export_status = models.CharField(max_length=1, choices=STATUS, default='0')
    jpg_export_version = models.SmallIntegerField(blank=True)
    
    user = models.ForeignKey(User)
    

    def get_absolute_url(self):
        return '/user/%s/ppt/%s/' % (self.user.username, self.id)
    
    def get_absolute_filepath(self):
        return '%suserfiles/%s' % (settings.PPT_FILEPATH, self.file.name)
    
    def __unicode__(self):
        return "<Ppt %s, %s,%s>" % (self.id, self.folder, self.filename)


# Model for storing results jpg generated files
class PptJpg(models.Model):
    filename = models.CharField(max_length=255)
    size = models.IntegerField(blank=True)
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



class PptUnit(models.Model):
    UNIT_TYPES = (
            (u'Experiment', u'Experiment'),
    )
    title = models.CharField(max_length=200, db_index=True)
    unittype = models.CharField(max_length=254, choices=UNIT_TYPES, blank=True)
    description = models.TextField()

    ppts = models.ManyToManyField(Ppt, blank=True)

    def get_absolute_url(self):
        return '/unit/%s/' % (self.id,)

    def __unicode__(self):
        return "<PptUnit %s, %s >" % (self.id, self.title)

