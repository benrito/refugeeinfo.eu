# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=200, null=True, blank=True)),
                ('page', models.CharField(max_length=200, null=True, blank=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
