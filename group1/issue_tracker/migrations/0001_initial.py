# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('requirements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=2000)),
                ('issue_type', models.CharField(max_length=20, choices=[(b'Bug', b'Bug'), (b'Feature', b'Feature Request'), (b'Internal Cleanup', b'Internal Cleanup')])),
                ('status', models.CharField(default=b'new', max_length=20, choices=[(b'Open-New', b'New'), (b'Open-Assigned', b'Assigned'), (b'Open-Accepted', b'Accepted'), (b'Closed-Fixed', b'Fixed'), (b'Closed-Verified', b'Verified'), (b'Closed-Working as Intended', b'Working as Intended'), (b'Closed-Obsolete', b'Obsolete'), (b'Closed-Duplicate', b'Duplicate')])),
                ('priority', models.CharField(max_length=20, choices=[(b'High', b'High'), (b'Medium', b'Medium'), (b'Low', b'Low')])),
                ('submitted_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('closed_date', models.DateTimeField(null=True, editable=False)),
                ('assignee', models.ForeignKey(related_name='assignee', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(to='requirements.Project', null=True)),
                ('reporter', models.ForeignKey(related_name='reporter', to=settings.AUTH_USER_MODEL, null=True)),
                ('verifier', models.ForeignKey(related_name='verifier', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=2000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_comment', models.BooleanField(default=True)),
                ('issue_id', models.ForeignKey(related_name='comments', blank=True, to='issue_tracker.Issue', null=True)),
                ('poster', models.ForeignKey(related_name='comments', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
