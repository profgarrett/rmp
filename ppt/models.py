from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os



class PptUnit(models.Model):
    UNIT_TYPES = (
            (u'Experiment', u'Experiment'),
    )
    title = models.CharField(max_length=200, db_index=True)
    unittype = models.CharField(max_length=254, choices=UNIT_TYPES, blank=True)
    description = models.TextField()

    def get_absolute_url(self):
        return '/unit/%s/' % (self.id,)

    def __str__(self):
        return "<PptUnit %s, %s >" % (self.id, self.title)


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

        return 'pptfile/%s/%s' % (self.user_id, filename[:20] + ext)


    title = models.CharField(max_length=240, default='', blank=True)
    description = models.TextField(default='', blank=True)
    pptfile = models.FileField(upload_to=getuploadedpath)
    jpg_export_status = models.CharField(max_length=1, choices=STATUS, default='0')
    jpg_export_version = models.SmallIntegerField(default='0')
    
    user = models.ForeignKey(User)
    pptunit = models.ForeignKey(PptUnit)

    def get_absolute_url(self):
        return '/user/%s/ppt/%s/' % (self.user.username, self.id)
    
    def get_absolute_filepath(self):
        return '%suserfiles/%s' % (settings.PPT_FILEPATH, self.file.name)
    
    def __str__(self):
        return "<Ppt %s, %s, %s>" % (self.id, self.title, self.pptfile)


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
        
        return "/media/pptfile/%s/jpg_%s/%s" % (user.id, self.ppt_id, self.filename)
    
    def __str__(self):
        return '<PptJpg %s, %s, %s>' % (self.id, self.filename, self.ppt)

