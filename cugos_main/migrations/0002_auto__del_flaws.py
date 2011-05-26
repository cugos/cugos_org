# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Flaws'
        db.delete_table('cugos_main_flaws')


    def backwards(self, orm):
        
        # Adding model 'Flaws'
        db.create_table('cugos_main_flaws', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('severity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('popularity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cugos_main', ['Flaws'])


    models = {
        'cugos_main.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
