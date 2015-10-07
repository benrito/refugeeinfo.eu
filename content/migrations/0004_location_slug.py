# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20151004_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='slug',
            field=models.SlugField(max_length=200, null=True, blank=True),
        ),
    ]
