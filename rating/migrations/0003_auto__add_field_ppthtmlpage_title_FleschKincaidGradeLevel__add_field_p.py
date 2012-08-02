# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PptHtmlPage.title_FleschKincaidGradeLevel'
        db.add_column('rating_ppthtmlpage', 'title_FleschKincaidGradeLevel',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'PptHtmlPage.text_FleschKincaidGradeLevel'
        db.add_column('rating_ppthtmlpage', 'text_FleschKincaidGradeLevel',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=5, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PptHtmlPage.title_FleschKincaidGradeLevel'
        db.delete_column('rating_ppthtmlpage', 'title_FleschKincaidGradeLevel')

        # Deleting field 'PptHtmlPage.text_FleschKincaidGradeLevel'
        db.delete_column('rating_ppthtmlpage', 'text_FleschKincaidGradeLevel')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rating.ppt': {
            'Meta': {'object_name': 'Ppt'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'folder': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'html_export_status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'html_parse_version': ('django.db.models.fields.SmallIntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jpg_export_status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'jpg_parse_version': ('django.db.models.fields.SmallIntegerField', [], {'blank': 'True'}),
            'rnd': ('django.db.models.fields.IntegerField', [], {}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'unit_id': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'rating.ppthtmlimage': {
            'Meta': {'object_name': 'PptHtmlImage'},
            'entropy': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '5', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ppt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.Ppt']"}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vector': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'rating.ppthtmlpage': {
            'Meta': {'object_name': 'PptHtmlPage'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'pagetype': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ppt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.Ppt']"}),
            'pptjpg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.PptJpg']", 'blank': 'True'}),
            'text_FleschKincaidGradeLevel': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '5', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'title_FleschKincaidGradeLevel': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '5', 'blank': 'True'})
        },
        'rating.ppthtmlpagepoint': {
            'Meta': {'object_name': 'PptHtmlPagePoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'ppthtmlpage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.PptHtmlPage']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'rating.ppthtmlpagesrc': {
            'Meta': {'object_name': 'PptHtmlPageSrc'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos_height': ('django.db.models.fields.IntegerField', [], {}),
            'pos_left': ('django.db.models.fields.IntegerField', [], {}),
            'pos_top': ('django.db.models.fields.IntegerField', [], {}),
            'pos_width': ('django.db.models.fields.IntegerField', [], {}),
            'ppthtmlimage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.PptHtmlImage']"}),
            'ppthtmlpage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.PptHtmlPage']"})
        },
        'rating.ppthtmlpagetext': {
            'Meta': {'object_name': 'PptHtmlPageText'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pos_height': ('django.db.models.fields.IntegerField', [], {}),
            'pos_left': ('django.db.models.fields.IntegerField', [], {}),
            'pos_top': ('django.db.models.fields.IntegerField', [], {}),
            'pos_width': ('django.db.models.fields.IntegerField', [], {}),
            'ppthtmlpage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.PptHtmlPage']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'rating.pptjpg': {
            'Meta': {'object_name': 'PptJpg'},
            'entropy': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '5', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'height': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ppt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.Ppt']"}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'rating.pptrating': {
            'Meta': {'object_name': 'PptRating'},
            'contentimage': ('django.db.models.fields.IntegerField', [], {}),
            'contenttext': ('django.db.models.fields.IntegerField', [], {}),
            'empty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ppt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.Ppt']"}),
            'ratedate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slideinteresting': ('django.db.models.fields.IntegerField', [], {}),
            'slidenovel': ('django.db.models.fields.IntegerField', [], {}),
            'slidequality': ('django.db.models.fields.IntegerField', [], {}),
            'slidestudy': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'rating.ppttag': {
            'Meta': {'object_name': 'PptTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ppt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.Ppt']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'rating.pptunit': {
            'Meta': {'object_name': 'PptUnit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ppts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rating.Ppt']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'unittype': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'rating.pptunittag': {
            'Meta': {'object_name': 'PptUnitTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rating.PptUnit']"})
        }
    }

    complete_apps = ['rating']