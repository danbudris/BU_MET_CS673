# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_authentication', '0002_flowmodel_flow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowmodel',
            name='flow',
        ),
    ]
