# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0011_profession_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='workers',
            field=models.ManyToManyField(to='workers_hub.Worker', blank=True),
        ),
    ]
