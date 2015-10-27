from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.contrib.gis.db import models
from django_countries.fields import CountryField


class Language(models.Model):
    name = models.CharField(max_length=100)
    name_in_english = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=40)

    def __unicode__(self):
        return unicode('{} ({})'.format(self.name_in_english, self.iso_code))


class Location(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    area = models.PolygonField()
    enabled = models.NullBooleanField(null=True, default=True)
    country = CountryField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children")
    managed_locally = models.BooleanField(default=False,)
    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.name)


class LocationContent(models.Model):
    title = models.CharField(max_length=100)
    language = models.ForeignKey(Language)
    html_url = models.URLField(blank=True, null=True, )
    parent = models.ForeignKey(Location, related_name="content")

    def __unicode__(self):
        return unicode(self.title)


class AuthorizationToken(models.Model):
    type = models.PositiveIntegerField(blank=True, null=True, default=1, choices=((1, 'Google Drive'),))
    token_text = models.TextField(blank=True, null=True)