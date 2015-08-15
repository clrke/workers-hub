# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0005_auto_20150815_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profession',
            name='user',
        ),
    ]
