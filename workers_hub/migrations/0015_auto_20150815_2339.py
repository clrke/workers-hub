# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0014_auto_20150815_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='cost',
            field=models.FloatField(),
        ),
    ]
