# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0003_auto_20150815_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('request', models.ForeignKey(to='workers_hub.Request')),
            ],
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
