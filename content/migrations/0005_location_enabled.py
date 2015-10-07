# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_location_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='enabled',
            field=models.NullBooleanField(default=True),
        ),
    ]
