# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RemindScientistInfo'
        db.create_table(u'scientist_remindscientistinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('days', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('hours', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('minutes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'scientist', ['RemindScientistInfo'])

        # Adding model 'RemindParticipantInfo'
        db.create_table(u'scientist_remindparticipantinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('days', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('hours', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('minutes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'scientist', ['RemindParticipantInfo'])

        # Deleting field 'Research.remind_participant_message'
        db.delete_column(u'scientist_research', 'remind_participant_message')

        # Deleting field 'Research.remind_research_before_minutes'
        db.delete_column(u'scientist_research', 'remind_research_before_minutes')

        # Deleting field 'Research.remind_research_message'
        db.delete_column(u'scientist_research', 'remind_research_message')

        # Deleting field 'Research.remind_participant_before_days'
        db.delete_column(u'scientist_research', 'remind_participant_before_days')

        # Deleting field 'Research.remind_participant_before_minutes'
        db.delete_column(u'scientist_research', 'remind_participant_before_minutes')

        # Deleting field 'Research.remind_research_before_hours'
        db.delete_column(u'scientist_research', 'remind_research_before_hours')

        # Deleting field 'Research.remind_participant_before_hours'
        db.delete_column(u'scientist_research', 'remind_participant_before_hours')

        # Deleting field 'Research.remind_research_before_days'
        db.delete_column(u'scientist_research', 'remind_research_before_days')

        # Adding field 'Research.remind_scientist_info'
        db.add_column(u'scientist_research', 'remind_scientist_info',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.RemindScientistInfo'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_participant_info'
        db.add_column(u'scientist_research', 'remind_participant_info',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.RemindParticipantInfo'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'RemindScientistInfo'
        db.delete_table(u'scientist_remindscientistinfo')

        # Deleting model 'RemindParticipantInfo'
        db.delete_table(u'scientist_remindparticipantinfo')

        # Adding field 'Research.remind_participant_message'
        db.add_column(u'scientist_research', 'remind_participant_message',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_research_before_minutes'
        db.add_column(u'scientist_research', 'remind_research_before_minutes',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_research_message'
        db.add_column(u'scientist_research', 'remind_research_message',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_participant_before_days'
        db.add_column(u'scientist_research', 'remind_participant_before_days',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_participant_before_minutes'
        db.add_column(u'scientist_research', 'remind_participant_before_minutes',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_research_before_hours'
        db.add_column(u'scientist_research', 'remind_research_before_hours',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_participant_before_hours'
        db.add_column(u'scientist_research', 'remind_participant_before_hours',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Research.remind_research_before_days'
        db.add_column(u'scientist_research', 'remind_research_before_days',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Research.remind_scientist_info'
        db.delete_column(u'scientist_research', 'remind_scientist_info_id')

        # Deleting field 'Research.remind_participant_info'
        db.delete_column(u'scientist_research', 'remind_participant_info_id')


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
        u'scientist.category': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['scientist.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'scientist.locationinfo': {
            'Meta': {'object_name': 'LocationInfo'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'lng': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'scientist.participantresearch': {
            'Meta': {'object_name': 'ParticipantResearch'},
            'award_credit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'research': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Research']"})
        },
        u'scientist.participantresearchevent': {
            'Meta': {'object_name': 'ParticipantResearchEvent'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'research_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.ResearchEvent']"})
        },
        u'scientist.remindparticipantinfo': {
            'Meta': {'object_name': 'RemindParticipantInfo'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'minutes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'scientist.remindscientistinfo': {
            'Meta': {'object_name': 'RemindScientistInfo'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'days': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'minutes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'scientist.research': {
            'Meta': {'object_name': 'Research'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'$'", 'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'ethical_permission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'further_ethical_permisson_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_on_web': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.LocationInfo']", 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'need_participant_num': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'non_ethical_permission_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remind_participant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remind_participant_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.RemindParticipantInfo']", 'null': 'True', 'blank': 'True'}),
            'remind_research': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remind_scientist_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.RemindScientistInfo']", 'null': 'True', 'blank': 'True'}),
            'remuneration': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'restrictions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'total_credit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'scientist.researchcategory': {
            'Meta': {'object_name': 'ResearchCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Category']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'research': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Research']"})
        },
        u'scientist.researchevent': {
            'Meta': {'object_name': 'ResearchEvent'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_participant_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_scientist_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'research': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Research']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'scientist.scientistresearch': {
            'Meta': {'object_name': 'ScientistResearch'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'research': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Research']"}),
            'scientist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['scientist']