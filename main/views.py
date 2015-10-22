import json

from django.shortcuts import render, redirect
from django.template import RequestContext
import requests
from django.contrib.gis.geos import fromstr
from ipware.ip import get_ip
from django.http import HttpResponse, Http404
from django.core.cache import cache

from content import models

GOOGLE_API_KEY = 'AIzaSyBj1Eu5IP1NB9UOlxKdsI693LYLjIE5NXo'
from django.views.decorators.cache import cache_page


def landing(request):
    ip_position = location_best_guess(request)
    point = 'POINT({} {})'.format(ip_position['longitude'], ip_position['latitude'])
    geopoint = fromstr(point, srid=4326)

    current_location = {}

    location = models.Location.objects.filter(area__intersects=geopoint, enabled=True).order_by('-parent')
    languages = list(models.Language.objects.all().order_by('name'))

    if location:
        found_location = location[0] if location else None

        location_content = {}
        for c in found_location.content.all():
            location_content[c.language.iso_code] = {
                "title": c.title,
                "google_doc": c.google_doc
            }
        current_location = {
            "id": found_location.id,
            "name": found_location.name,
            "slug": found_location.slug,
            "contents": location_content
        }

    return render(request, 'landing.html', context={
        "current_location": json.dumps(current_location),
        "languages": languages,
    }, context_instance=RequestContext(request))


@cache_page(60 * 15)
def index(request, page_id, language):
    # doc_path = 'https://docs.google.com/document/d/1NCCHyLKiSI7yHIZjbBGiIUg5_jFUOdTwgOa4vJjkYzM/pub?embedded=true'
    google_doc = '<h1 style="color: white">Your location is not supported by this platform.</h1>'
    location = models.Location.objects.filter(id=page_id)

    if location:
        location = location[0]

        content = location.content.filter(language__iso_code=language)

        default_content = location.content.all()
        content = content[0] if content else default_content[0] if default_content else None

        if content and content.google_doc:
            doc_path = content.google_doc
            cached = cache.get(doc_path)
            if cached:
                google_doc = cached
            else:
                google_doc = requests.get(doc_path).text

    return render(request, 'index.html', context={
        "google_doc": google_doc
    }, context_instance=RequestContext(request))


def depth(location):
    d = 0
    parent = location.parent
    while parent:
        d += 1
        parent = parent.parent

    return d


def location_from_device(request):
    lnglat = request.GET['lnglat']
    point = 'POINT({})'.format(lnglat)
    geopoint = fromstr(point, srid=4326)

    location = sorted(models.Location.objects.filter(area__intersects=geopoint, enabled=True), key=lambda x: -depth(x))

    if not location:
        raise Http404()

    found_location = location[0] if location else None

    location_content = {}
    for c in found_location.content.all():
        location_content[c.language.iso_code] = {
            "title": c.title,
            "google_doc": c.google_doc
        }

    return HttpResponse(json.dumps({
        "id": found_location.id,
        "name": found_location.name,
        "slug": found_location.slug,
        "contents": location_content
    }), content_type='application/json')


def location_best_guess(request):
    latitude = 0
    longitude = 0

    try:
        location_response = requests.get('http://ip-api.com/json/{}'.format(get_ip(request)))

        location_info = location_response.json()

        if location_info['status'] == 'success':
            latitude = location_info['lat']
            longitude = location_info['lon']
    except Exception as e:
        pass

    return {"latitude": latitude, "longitude": longitude}


def slug_no_language(request, slug):
    if 'HTTP_ACCEPT_LANGUAGE' in request.META:
        accept_language = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
        first_language = accept_language[0].split('-')

        if first_language:
            first_language = first_language[0]
    else:
        first_language = 'en'

    return slug_index(request, slug, first_language)


def slug_index(request, slug, language):
    locations = models.Location.objects.filter(slug=slug)

    if not locations:
        return redirect('/')

    location = locations[0]

    return cache_page(60 * 15)(index)(request, location.id, language)
