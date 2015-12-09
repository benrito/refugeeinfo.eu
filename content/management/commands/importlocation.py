from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.core.management.base import BaseCommand
from content import models
from django.utils.text import slugify
import sys
import json
from django.contrib.gis import geos
import requests
import xmltodict
import gzip
import tarfile
from StringIO import StringIO
import tempfile
import os
import shutil

class Command(BaseCommand):
    help = 'Load GeoJSON and gets the location out of it'


    def handle(self, *args, **options):
        json_input = False
        if not json_input:
            original_url = 'https://s3.amazonaws.com/osm-polygons.mapzen.com/'
            countries = requests.get(original_url).text
            countries = xmltodict.parse(countries)
            for i, c in enumerate(countries['ListBucketResult']['Contents'][1:], start=1):
                print("{}: {}".format(i, c['Key']))
            country_index = raw_input('Enter selected country: ')
            if not country_index:
                return
            selected = countries['ListBucketResult']['Contents'][int(country_index)]
            response = requests.get(original_url + selected['Key'])

            tar_file = tarfile.open(mode='r:gz', fileobj=StringIO(response.content))

            tmpdir = tempfile.mkdtemp()
            tar_file.extractall(tmpdir)

            json_file_path = os.path.join(tmpdir, os.listdir(tmpdir)[0])
            all_files = os.listdir(json_file_path)

            for i, f in enumerate(all_files, start=1):
                print("{}: {}".format(i, f))

            level_index = raw_input('Enter selected file: ')
            if not level_index:
                return

            selected_file = all_files[int(level_index)-1]
            with open(os.path.join(json_file_path, selected_file)) as f:
                current_json = f.read()

            content = json.loads(current_json)
            features = content['features']

            shutil.rmtree(tmpdir)
        else:
            sys.stdin = open('/dev/tty')
            content = json.loads(json_input)
            features = content['features']

        locations = sorted([a for a in features if 'name:en' in a['properties']],
                           key=lambda x: x['properties']['name:en'])

        for i, l in enumerate(locations):
            print("{}: {} ({})".format(i + 1, l['properties']['name:en'], l['properties']['name']))

        feature_index = raw_input('Enter selected feature: ')
        if not feature_index:
            return

        if feature_index.lower() == 'all':
            to_be_merged = [geos.GEOSGeometry(json.dumps(a['geometry'])) for a in features]
            feature = to_be_merged[0]
            for i in range(1, len(to_be_merged)):
                feature = feature.union(to_be_merged[i])

        elif ',' in feature_index:
            indices = [int(a) for a in feature_index.split(',')]
            to_be_merged = [geos.GEOSGeometry(json.dumps(locations[a - 1]['geometry'])) for a in indices]
            feature = to_be_merged[0]
            for i in range(1, len(to_be_merged)):
                feature = feature.union(to_be_merged[i])

        else:
            feature_index = int(feature_index)
            print(locations[feature_index - 1]['properties']['name'])

            feature_json = json.dumps(locations[feature_index - 1]['geometry'])

            feature = geos.GEOSGeometry(feature_json)

        is_new_location = raw_input('Is this a new location? (y/N) ')
        is_new_location = True if 'Y' in is_new_location.upper() else False

        merged = feature.convex_hull if len(feature) > 3 else feature[0]
        #merged = merged.simplify(tolerance=0.01)

        if is_new_location:
            location_name = raw_input('Name of location: ')
            location_slug = slugify(location_name)
            country = raw_input('Country: ')
            parent_id = raw_input('Parent Id: ')
            location = models.Location.objects.create(
                name=location_name,
                country=country,
                slug=location_slug,
                parent_id=int(parent_id) if parent_id else None,
                area=merged,
            )
        else:
            location_id = raw_input('Location Id: ')
            location = models.Location.objects.get(id=int(location_id))
            location.area = merged
            location.save()