# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ppt'
        db.create_table('rating_ppt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('folder', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('rnd', self.gf('django.db.models.fields.IntegerField')()),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('unit_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('jpg_export_status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('jpg_parse_version', self.gf('django.db.models.fields.SmallIntegerField')(blank=True)),
            ('html_export_status', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('html_parse_version', self.gf('django.db.models.fields.SmallIntegerField')(blank=True)),
        ))
        db.send_create_signal('rating', ['Ppt'])

        # Adding model 'PptJpg'
        db.create_table('rating_pptjpg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ppt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.Ppt'])),
        ))
        db.send_create_signal('rating', ['PptJpg'])

        # Adding model 'PptHtmlImage'
        db.create_table('rating_ppthtmlimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('template', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vector', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ppt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.Ppt'])),
        ))
        db.send_create_signal('rating', ['PptHtmlImage'])

        # Adding model 'PptHtmlPage'
        db.create_table('rating_ppthtmlpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pagetype', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ppt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.Ppt'])),
            ('pptjpg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.PptJpg'], blank=True)),
        ))
        db.send_create_signal('rating', ['PptHtmlPage'])

        # Adding model 'PptHtmlPagePoint'
        db.create_table('rating_ppthtmlpagepoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('ppthtmlpage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.PptHtmlPage'])),
        ))
        db.send_create_signal('rating', ['PptHtmlPagePoint'])

        # Adding model 'PptHtmlPageSrc'
        db.create_table('rating_ppthtmlpagesrc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ppthtmlpage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.PptHtmlPage'])),
            ('ppthtmlimage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.PptHtmlImage'])),
            ('pos_left', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_width', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_top', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_height', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('rating', ['PptHtmlPageSrc'])

        # Adding model 'PptHtmlPageText'
        db.create_table('rating_ppthtmlpagetext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('pos_left', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_width', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_top', self.gf('django.db.models.fields.IntegerField')()),
            ('pos_height', self.gf('django.db.models.fields.IntegerField')()),
            ('ppthtmlpage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.PptHtmlPage'])),
        ))
        db.send_create_signal('rating', ['PptHtmlPageText'])

        # Adding model 'PptUnit'
        db.create_table('rating_pptunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('unittype', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rating', ['PptUnit'])

        # Adding M2M table for field ppts on 'PptUnit'
        db.create_table('rating_pptunit_ppts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pptunit', models.ForeignKey(orm['rating.pptunit'], null=False)),
            ('ppt', models.ForeignKey(orm['rating.ppt'], null=False))
        ))
        db.create_unique('rating_pptunit_ppts', ['pptunit_id', 'ppt_id'])

        # Adding model 'PptUnitTag'
        db.create_table('rating_pptunittag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.PptUnit'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
        ))
        db.send_create_signal('rating', ['PptUnitTag'])

        # Adding model 'PptTag'
        db.create_table('rating_ppttag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ppt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.Ppt'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
        ))
        db.send_create_signal('rating', ['PptTag'])

        # Adding model 'PptRating'
        db.create_table('rating_pptrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ratedate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('empty', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contentimage', self.gf('django.db.models.fields.IntegerField')()),
            ('contenttext', self.gf('django.db.models.fields.IntegerField')()),
            ('slidenovel', self.gf('django.db.models.fields.IntegerField')()),
            ('slidestudy', self.gf('django.db.models.fields.IntegerField')()),
            ('slidequality', self.gf('django.db.models.fields.IntegerField')()),
            ('slideinteresting', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ppt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rating.Ppt'])),
        ))
        db.send_create_signal('rating', ['PptRating'])


    def backwards(self, orm):
        # Deleting model 'Ppt'
        db.delete_table('rating_ppt')

        # Deleting model 'PptJpg'
        db.delete_table('rating_pptjpg')

        # Deleting model 'PptHtmlImage'
        db.delete_table('rating_ppthtmlimage')

        # Deleting model 'PptHtmlPage'
        db.delete_table('rating_ppthtmlpage')

        # Deleting model 'PptHtmlPagePoint'
        db.delete_table('rating_ppthtmlpagepoint')

        # Deleting model 'PptHtmlPageSrc'
        db.delete_table('rating_ppthtmlpagesrc')

        # Deleting model 'PptHtmlPageText'
        db.delete_table('rating_ppthtmlpagetext')

        # Deleting model 'PptUnit'
        db.delete_table('rating_pptunit')

        # Removing M2M table for field ppts on 'PptUnit'
        db.delete_table('rating_pptunit_ppts')

        # Deleting model 'PptUnitTag'
        db.delete_table('rating_pptunittag')

        # Deleting model 'PptTag'
        db.delete_table('rating_ppttag')

        # Deleting model 'PptRating'
        db.delete_table('rating_pptrating')


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
            'title': ('django.db.models.fields.TextField', [], {})
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