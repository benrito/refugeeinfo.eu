# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('google_doc', models.URLField(null=True, blank=True)),
                ('language', models.ForeignKey(to='content.Language')),
                ('parent', models.ForeignKey(to='content.Location')),
            ],
        ),
        migrations.RemoveField(
            model_name='locationtitle',
            name='language',
        ),
        migrations.RemoveField(
            model_name='locationtitle',
            name='parent',
        ),
        migrations.DeleteModel(
            name='LocationTitle',
        ),
    ]
