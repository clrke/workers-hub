# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0012_auto_20150815_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
