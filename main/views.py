# -*- coding: utf-8 -*-

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

from content import models, utils


CACHE_LENGTH = getattr(settings, 'CACHE_LENGTH', 60 * 15)


def landing(request):
    context = {}
    location = None
    current_location = {}

    languages = list(models.Language.objects.all().order_by('name'))
    root_locations = models.Location.objects.filter(parent__isnull=True)

    child_locations = [(a, [b for b in a.children.all() if b.enabled]) for a in root_locations]
    root_locations = [a[0] for a in child_locations if len(a[1]) > 0]

    def get_linked(parent):
        link_dictionary = getattr(settings, 'OVERRIDE_SLUG_LINKS', {})
        if parent in link_dictionary:
            links = link_dictionary[parent]
            return list(models.Location.objects.filter(slug__in=links))
        return []

    child_locations = [(a, b + get_linked(a.slug)) for a, b in child_locations]

    if location:
        found_location = location[0] if location else None

        location_content = {}
        for c in found_location.content.all():
            location_content[c.language.iso_code] = {
                "title": c.title,
                "html_url": c.html_url
            }
        current_location = {
            "id": found_location.id,
            "name": found_location.name,
            "slug": found_location.slug,
            "contents": location_content
        }
    context.update({
        "current_location": json.dumps(current_location),
        "languages": languages,
        "locations": settings.LOCATIONS,

        "root_locations": root_locations,
        "child_locations": child_locations,
    })

    return render(request, 'landing.html', context=context, context_instance=RequestContext(request))


def site_map(request):
    query = models.Location.objects.filter(enabled=True,
                                           country__isnull=False)
    query = query.values('country').annotate(count=django.db.models.Count('*'))

    countries = dict([(c['country'].lower(), c['count']) for c in query])
    best_guess = location_best_guess(request, timeout=2)
    return render(request,
                  "site-map.html",
                  {
                      "available_countries": json.dumps(countries),
                      "location": best_guess,
                      "languages": json.dumps(
                          [dict(iso_code=a.iso_code, name=a.name, id=a.id) for a in models.Language.objects.all()]),
                  },
                  RequestContext(request))


def capture_captive(request):
    if 'base_grant_url' in request.GET:
        return redirect("{}?continue_url={}".format(request.GET['base_grant_url'],
                                                    urllib.quote_plus(request.GET['user_continue_url'])))
    else:
        return redirect('/')


@cache_page(CACHE_LENGTH)
def index(request, page_id, language):
    location = models.Location.objects.filter(id=page_id)
    html_content = ""
    from django.utils import translation

    translation.activate(language)


    # Handling Meraki:
    context = {
    }

    if 'base_grant_url' in request.GET:
        context['is_captive'] = True
        context['next'] = "{}?continue_url={}".format(
            request.GET['base_grant_url'],
            urllib.quote_plus(request.GET['user_continue_url'])
        )

        print("Request from meraki: {}".format(' '.join([': '.join(a) for a in request.GET.iterkeys()])))

    if 'provider' in request.GET:
        context['provider'] = request.GET['provider']

    if location:
        location = location[0]

        if location.managed_locally:
            """
            Loading content from a CMS or CMS-like site
            """
            url_parts = [location.slug]
            m = location
            while m.parent:
                url_parts.append(m.parent.slug)
                m = m.parent

            complete_url = '/'.join(reversed(url_parts))

            cms_url = utils.get_cms_url(language, complete_url)

            if cms_url in cache:
                html_content = cache.get(cms_url)
            else:
                html_content = utils.get_cms_page(language, complete_url)
                cache.set(cms_url, html_content)
        else:
            """
            Loading content from a google doc
            """
            html_content = ""

            content = location.content.filter(language__iso_code=language)

            default_content = location.content.all()
            content = content[0] if content else default_content[0] if default_content else None

            if content and content.html_url:
                doc_path = content.html_url
                cached = cache.get(doc_path)
                if cached:
                    html_content = cached
                else:
                    html_content = requests.get(doc_path).text

    languages = list(models.Language.objects.all().order_by('name'))

    context.update({
        "html_content": html_content,
        "languages": languages,
        "location": location,
        "language": language,
        "service_map_enabled": settings.ENABLE_SERVICES or False,
    })

    return render(request, 'index.html', context=context, context_instance=RequestContext(request))


def feedback(request, page_id, language):
    location = models.Location.objects.get(id=page_id)

    if isinstance(settings.FEEDBACK_URL, dict):
        if language in settings.FEEDBACK_URL:
            feedback_url = unicode(settings.FEEDBACK_URL[language]).format(unicode(location.name))
        else:
            feedback_url = unicode(settings.FEEDBACK_URL['en']).format(unicode(location.name))
    else:
        feedback_url = unicode(settings.FEEDBACK_URL).format(unicode(location.name))

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    from . import models as main_models

    main_models.FeedbackClick.objects.create(
        ip_address=ip,
        page=location.name,
    )

    return redirect(feedback_url)


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
            "html_url": c.html_url
        }

    return HttpResponse(json.dumps({
        "id": found_location.id,
        "name": found_location.name,
        "slug": found_location.slug,
        "contents": location_content
    }), content_type='application/json')


def location_best_guess(request, timeout=0.2):
    latitude = 0
    longitude = 0
    country_code = None
    try:
        location_response = requests.get('http://ip-api.com/json/{}'.format(get_ip(request)), timeout=timeout)

        location_info = location_response.json()

        if location_info['status'] == 'success':
            latitude = location_info['lat']
            longitude = location_info['lon']
            if 'countryCode' in location_info:
                country_code = location_info['countryCode'].lower()
    except Exception as e:
        pass

    return {"latitude": latitude, "longitude": longitude, 'countryCode': country_code}


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

    return cache_page(CACHE_LENGTH)(index)(request, location.id, language)


def services(request, slug, service_category=None):
    if 'HTTP_ACCEPT_LANGUAGE' in request.META:
        accept_language = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
        first_language = accept_language[0].split('-')

        if first_language:
            first_language = first_language[0]
    else:
        first_language = 'en'

    location = models.Location.objects.filter(slug=slug)

    if location:
        location = location[0]
    else:
        return redirect('/')

    extent = geojson.Polygon(([(a[0], a[1], 0) for a in location.area.shell.array],))

    print extent

    return render(request,
                  "service-map.html",
                  {
                      "extent": unicode(extent),
                      "slug": location.slug,
                  },
                  RequestContext(request))


def acknowledgements(request):
    return render(request, "acknowledgments.html", {}, RequestContext(request))
