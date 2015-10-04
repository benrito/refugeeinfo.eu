# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20151004_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationcontent',
            name='parent',
            field=models.ForeignKey(related_name='content', to='content.Location'),
        ),
    ]
