# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('name_in_english', models.CharField(max_length=100)),
                ('iso_code', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('area', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='content.Location', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocationTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('language', models.ForeignKey(to='content.Language')),
                ('parent', models.ForeignKey(to='content.Location')),
            ],
        ),
    ]
