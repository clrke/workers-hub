# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0004_auto_20150815_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='request',
            field=models.ForeignKey(default='1', to='workers_hub.Request'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='range_max',
            field=models.IntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='range_min',
            field=models.IntegerField(default='0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='subject',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
    ]
