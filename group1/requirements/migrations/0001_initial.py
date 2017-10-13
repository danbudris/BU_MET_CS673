# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(default=b'', max_length=1024, blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(default=b'', max_length=1024, blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'permissions': (('own_project', 'Can own and create projects'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=b'project_files')),
                ('project', models.ForeignKey(to='requirements.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(default=b'', max_length=1024, blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('reason', models.CharField(default=b'', max_length=1024, blank=True)),
                ('test', models.CharField(default=b'', max_length=1024, blank=True)),
                ('hours', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1, max_length=1, choices=[(1, b'Unstarted'), (2, b'Started'), (3, b'Completed'), (4, b'Accepted')])),
                ('points', models.IntegerField(default=0, max_length=1, choices=[(0, b'0 Not Scaled'), (1, b'1 Point'), (2, b'2 Points'), (3, b'3 Points'), (4, b'4 Points'), (5, b'5 Points')])),
                ('pause', models.BooleanField(default=False)),
                ('iteration', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='requirements.Iteration', null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(to='requirements.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=1024)),
                ('comment', models.CharField(default=b'', max_length=1024)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('story', models.ForeignKey(to='requirements.Story')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=1024)),
                ('story', models.ForeignKey(to='requirements.Story')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=128)),
                ('project', models.ForeignKey(to='requirements.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='requirements.UserAssociation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iteration',
            name='project',
            field=models.ForeignKey(to='requirements.Project'),
            preserve_default=True,
        ),
    ]
