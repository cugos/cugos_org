# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Project'
        db.create_table('cugos_main_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('cugos_main', ['Project'])

        # Adding model 'Event'
        db.create_table('cugos_main_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('cugos_main', ['Event'])

        # Adding model 'Flaws'
        db.create_table('cugos_main_flaws', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('popularity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('severity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('cugos_main', ['Flaws'])


    def backwards(self, orm):
        
        # Deleting model 'Project'
        db.delete_table('cugos_main_project')

        # Deleting model 'Event'
        db.delete_table('cugos_main_event')

        # Deleting model 'Flaws'
        db.delete_table('cugos_main_flaws')


    models = {
        'cugos_main.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'cugos_main.flaws': {
            'Meta': {'object_name': 'Flaws'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'severity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'cugos_main.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cugos_main']
