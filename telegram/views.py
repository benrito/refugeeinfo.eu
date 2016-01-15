from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'
import json
import urllib

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.gis.geos import fromstr
from ipware.ip import get_ip
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import django.db.models
import geojson
from django.conf import settings
import requests
from django.utils import translation

from content import models, utils


def receive_telegram(request, token):
    content_type = request.META.get('CONTENT_TYPE')
    if 'json' in content_type:
        print('Received JSON')
        content = json.loads(request.body)
        print(json.dumps(content))
    else:
        print('No JSON in request')
        print(request.body)
    return HttpResponse()