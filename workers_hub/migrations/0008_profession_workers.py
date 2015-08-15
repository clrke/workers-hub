# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0007_auto_20150815_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='workers',
            field=models.ManyToManyField(to='workers_hub.Worker'),
        ),
    ]
