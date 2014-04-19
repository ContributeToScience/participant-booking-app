# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'scientist_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['scientist.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'scientist', ['Category'])

        # Adding unique constraint on 'Category', fields ['parent', 'name']
        db.create_unique(u'scientist_category', ['parent_id', 'name'])

        # Adding model 'LocationInfo'
        db.create_table(u'scientist_locationinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('lng', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('lat', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'scientist', ['LocationInfo'])

        # Adding model 'Research'
        db.create_table(u'scientist_research', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=1024, null=True, blank=True)),
            ('need_participant_num', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_on_web', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.LocationInfo'], null=True, blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('remuneration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='$', max_length=1)),
            ('ethical_permission', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_ethical_permission_reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('further_ethical_permisson_info', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('restrictions', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('remind_research', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remind_participant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_credit', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('is_anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_credit_scheme', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'scientist', ['Research'])

        # Adding model 'ResearchEvent'
        db.create_table(u'scientist_researchevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('research', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Research'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_participant_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_scientist_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'scientist', ['ResearchEvent'])

        # Adding model 'ResearchCategory'
        db.create_table(u'scientist_researchcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Category'])),
            ('research', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Research'])),
        ))
        db.send_create_signal(u'scientist', ['ResearchCategory'])

        # Adding model 'ParticipantResearch'
        db.create_table(u'scientist_participantresearch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('research', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Research'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('award_credit', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'scientist', ['ParticipantResearch'])

        # Adding model 'ScientistResearch'
        db.create_table(u'scientist_scientistresearch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('scientist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('research', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Research'])),
        ))
        db.send_create_signal(u'scientist', ['ScientistResearch'])

        # Adding model 'ParticipantResearchEvent'
        db.create_table(u'scientist_participantresearchevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('research_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.ResearchEvent'])),
        ))
        db.send_create_signal(u'scientist', ['ParticipantResearchEvent'])

        # Adding model 'RemindParticipantInfo'
        db.create_table(u'scientist_remindparticipantinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('research', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Research'])),
            ('time', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='email', max_length=20)),
            ('time_type', self.gf('django.db.models.fields.CharField')(default='minutes', max_length=20)),
        ))
        db.send_create_signal(u'scientist', ['RemindParticipantInfo'])

        # Adding model 'RemindScientistInfo'
        db.create_table(u'scientist_remindscientistinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('research', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scientist.Research'])),
            ('time', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='email', max_length=20)),
            ('time_type', self.gf('django.db.models.fields.CharField')(default='minutes', max_length=20)),
        ))
        db.send_create_signal(u'scientist', ['RemindScientistInfo'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['parent', 'name']
        db.delete_unique(u'scientist_category', ['parent_id', 'name'])

        # Deleting model 'Category'
        db.delete_table(u'scientist_category')

        # Deleting model 'LocationInfo'
        db.delete_table(u'scientist_locationinfo')

        # Deleting model 'Research'
        db.delete_table(u'scientist_research')

        # Deleting model 'ResearchEvent'
        db.delete_table(u'scientist_researchevent')

        # Deleting model 'ResearchCategory'
        db.delete_table(u'scientist_researchcategory')

        # Deleting model 'ParticipantResearch'
        db.delete_table(u'scientist_participantresearch')

        # Deleting model 'ScientistResearch'
        db.delete_table(u'scientist_scientistresearch')

        # Deleting model 'ParticipantResearchEvent'
        db.delete_table(u'scientist_participantresearchevent')

        # Deleting model 'RemindParticipantInfo'
        db.delete_table(u'scientist_remindparticipantinfo')

        # Deleting model 'RemindScientistInfo'
        db.delete_table(u'scientist_remindscientistinfo')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'research': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Research']"}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time_type': ('django.db.models.fields.CharField', [], {'default': "'minutes'", 'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '20'})
        },
        u'scientist.remindscientistinfo': {
            'Meta': {'object_name': 'RemindScientistInfo'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'research': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.Research']"}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time_type': ('django.db.models.fields.CharField', [], {'default': "'minutes'", 'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '20'})
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
            'is_credit_scheme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_on_web': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scientist.LocationInfo']", 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'need_participant_num': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'non_ethical_permission_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remind_participant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remind_research': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remuneration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'restrictions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'total_credit': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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