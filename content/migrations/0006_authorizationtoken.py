# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_location_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveIntegerField(default=1, null=True, blank=True, choices=[(1, 'Google Drive')])),
                ('token_text', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
