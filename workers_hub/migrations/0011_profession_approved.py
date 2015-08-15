# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers_hub', '0010_request_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
