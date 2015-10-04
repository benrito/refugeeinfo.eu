from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from . import models
import requests
from ipware.ip import get_ip
import json


def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def location_best_guess(request):
    location_response = requests.get('http://www.telize.com/geoip/{}'.format(get_ip(request)))

    location_info = location_response.json()

    latitude = 0
    longitude = 0

    if 'code' not in location_info or location_info['code'] != 401:
        latitude = location_info['latitude']
        longitude = location_info['longitude']

    return HttpResponse(json.dumps({"latitude": latitude, "longitude": longitude}), content_type="application/json")


def noop(request):
    accept_language = [a.split(';')[0] for a in request.META['HTTP_ACCEPT_LANGUAGE'].split(',')]

    all_languages = list(models.Language.objects.filter(iso_code__in=accept_language))
    sorted_languages = [(a, accept_language.index(a.iso_code)) for a in all_languages]
    sorted_languages.sort(lambda x, y: -x[1])

    sorted_languages = [s[0] for s in sorted_languages]

    # location_response = requests.get('http://www.telize.com/geoip/{}'.format(get_ip(request)))

    location_info = {'code': 401}  # location_response.json()

    latitude = 0
    longitude = 0

    if 'code' not in location_info or location_info['code'] != 401:
        latitude = location_info['latitude']
        longitude = location_info['longitude']

    if sorted_languages:
        return HttpResponse(
            """
            <script>
                    navigator.geolocation.getCurrentPosition(function(a) {{
                     console.log(a.coords.latitude);
                     console.log(a.coords.longitude);
                     }});
            </script>
            Your language is {}, and your location info {} {}"""
            .format(sorted_languages[0].name_in_english, latitude, longitude)
        )

    return HttpResponse(
        """
        <script>
                navigator.geolocation.getCurrentPosition(function(a) {
                 console.log(a.coords.latitude);
                 console.log(a.coords.longitude);
                 });
        </script>
        """ +
        "<br/>".join(accept_language)
        + "<br />"
        + "<br/>".join([s.name for s in sorted_languages])
    )
