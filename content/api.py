from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from rest_framework import serializers, viewsets
from . import models
import json
from rest_framework.decorators import detail_route, list_route
from rest_framework import response
import django.db.models

class LocationSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_location(self, obj):
        return dict(type="Point", coordinates=[obj.area.centroid.x, obj.area.centroid.y])

    def get_languages(self, obj):
        return [dict(iso_code=l.language.iso_code, name=l.language.name) for l in obj.content.all()]

    class Meta:
        model = models.Location
        fields = ('id', 'name', 'slug', 'location', 'languages', )


class LocationViewSet(viewsets.ModelViewSet, ):
    queryset = models.Location.objects.filter(enabled=True)
    serializer_class = LocationSerializer

    def get_queryset(self):
        country = self.request.query_params.get('country', None)

        if country is not None:
            queryset = self.queryset.filter(country=country)
        else:
            queryset = self.queryset.none()

        return queryset