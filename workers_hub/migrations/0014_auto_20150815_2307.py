# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0013_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profession',
            name='workers',
        ),
        migrations.AddField(
            model_name='worker',
            name='professions',
            field=models.ManyToManyField(to='workers_hub.Profession', blank=True),
        ),
    ]
