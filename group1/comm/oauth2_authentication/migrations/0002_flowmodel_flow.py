# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowmodel',
            name='flow',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
