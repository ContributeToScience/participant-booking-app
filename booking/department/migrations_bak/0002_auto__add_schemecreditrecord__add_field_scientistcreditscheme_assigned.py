# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SchemeCreditRecord'
        db.create_table(u'department_schemecreditrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('credit_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['department.CreditScheme'])),
            ('scientist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scientist_creditrecord_set', to=orm['auth.User'])),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participant_creditrecord_set', to=orm['auth.User'])),
            ('allocated_credit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'department', ['SchemeCreditRecord'])

        # Adding field 'ScientistCreditScheme.assigned_credit'
        db.add_column(u'department_scientistcreditscheme', 'assigned_credit',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ScientistCreditScheme.remain_credit'
        db.add_column(u'department_scientistcreditscheme', 'remain_credit',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'CreditScheme.department'
        db.add_column(u'department_creditscheme', 'department',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'CreditScheme.total_credit'
        db.add_column(u'department_creditscheme', 'total_credit',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'CreditScheme.remain_credit'
        db.add_column(u'department_creditscheme', 'remain_credit',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ParticipantCreditScheme.required_credit'
        db.add_column(u'department_participantcreditscheme', 'required_credit',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ParticipantCreditScheme.incomplete_credit'
        db.add_column(u'department_participantcreditscheme', 'incomplete_credit',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UniversityDepartment.user'
        db.add_column(u'department_universitydepartment', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SchemeCreditRecord'
        db.delete_table(u'department_schemecreditrecord')

        # Deleting field 'ScientistCreditScheme.assigned_credit'
        db.delete_column(u'department_scientistcreditscheme', 'assigned_credit')

        # Deleting field 'ScientistCreditScheme.remain_credit'
        db.delete_column(u'department_scientistcreditscheme', 'remain_credit')

        # Deleting field 'CreditScheme.department'
        db.delete_column(u'department_creditscheme', 'department_id')

        # Deleting field 'CreditScheme.total_credit'
        db.delete_column(u'department_creditscheme', 'total_credit')

        # Deleting field 'CreditScheme.remain_credit'
        db.delete_column(u'department_creditscheme', 'remain_credit')

        # Deleting field 'ParticipantCreditScheme.required_credit'
        db.delete_column(u'department_participantcreditscheme', 'required_credit')

        # Deleting field 'ParticipantCreditScheme.incomplete_credit'
        db.delete_column(u'department_participantcreditscheme', 'incomplete_credit')

        # Deleting field 'UniversityDepartment.user'
        db.delete_column(u'department_universitydepartment', 'user_id')


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
        u'department.coordinatorcreditscheme': {
            'Meta': {'object_name': 'CoordinatorCreditScheme'},
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credit_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['department.CreditScheme']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'department.creditscheme': {
            'Meta': {'object_name': 'CreditScheme'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remain_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'total_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'university_department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['department.UniversityDepartment']"})
        },
        u'department.participantcreditscheme': {
            'Meta': {'object_name': 'ParticipantCreditScheme'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credit_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['department.CreditScheme']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incomplete_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'required_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'department.schemecreditrecord': {
            'Meta': {'object_name': 'SchemeCreditRecord'},
            'allocated_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credit_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['department.CreditScheme']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participant_creditrecord_set'", 'to': u"orm['auth.User']"}),
            'scientist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scientist_creditrecord_set'", 'to': u"orm['auth.User']"})
        },
        u'department.scientistcreditscheme': {
            'Meta': {'object_name': 'ScientistCreditScheme'},
            'assigned_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'credit_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['department.CreditScheme']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'remain_credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'scientist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'department.universitydepartment': {
            'Meta': {'object_name': 'UniversityDepartment'},
            'coord': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['department']