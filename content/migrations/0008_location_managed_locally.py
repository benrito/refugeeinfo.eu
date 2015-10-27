# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20151026_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='managed_locally',
            field=models.BooleanField(default=False),
        ),
    ]
