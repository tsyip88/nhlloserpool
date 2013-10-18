# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Matchup'
        db.create_table(u'matchups_matchup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team', to=orm['teams.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team', to=orm['teams.Team'])),
            ('home_team_score', self.gf('django.db.models.fields.SmallIntegerField')(default=-1)),
            ('away_team_score', self.gf('django.db.models.fields.SmallIntegerField')(default=-1)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'matchups', ['Matchup'])

        # Adding model 'PickSet'
        db.create_table(u'matchups_pickset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'matchups', ['PickSet'])

        # Adding model 'Pick'
        db.create_table(u'matchups_pick', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('selected_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.Team'])),
            ('week_number', self.gf('django.db.models.fields.SmallIntegerField')(default=-1)),
            ('pick_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['matchups.PickSet'])),
            ('is_winning_pick', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'matchups', ['Pick'])


    def backwards(self, orm):
        # Deleting model 'Matchup'
        db.delete_table(u'matchups_matchup')

        # Deleting model 'PickSet'
        db.delete_table(u'matchups_pickset')

        # Deleting model 'Pick'
        db.delete_table(u'matchups_pick')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'matchups.matchup': {
            'Meta': {'object_name': 'Matchup'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'to': u"orm['teams.Team']"}),
            'away_team_score': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'to': u"orm['teams.Team']"}),
            'home_team_score': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'matchups.pick': {
            'Meta': {'object_name': 'Pick'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_winning_pick': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pick_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['matchups.PickSet']"}),
            'selected_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teams.Team']"}),
            'week_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'})
        },
        u'matchups.pickset': {
            'Meta': {'object_name': 'PickSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'teams.conference': {
            'Meta': {'object_name': 'Conference'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teams.League']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'teams.division': {
            'Meta': {'object_name': 'Division'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teams.Conference']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'teams.league': {
            'Meta': {'object_name': 'League'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['teams.Division']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['matchups']