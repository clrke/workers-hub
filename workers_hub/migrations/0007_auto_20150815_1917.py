# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0006_remove_profession_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='user',
        ),
        migrations.AddField(
            model_name='proposal',
            name='worker',
            field=models.ForeignKey(default='1', to='workers_hub.Worker'),
            preserve_default=False,
        ),
    ]
