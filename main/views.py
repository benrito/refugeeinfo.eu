from django.shortcuts import render
from django.template import RequestContext
import requests

from ipware.ip import get_ip

GOOGLE_API_KEY = 'AIzaSyBj1Eu5IP1NB9UOlxKdsI693LYLjIE5NXo'


def landing(request):
    ip_position = location_best_guess(request)
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={}, {}&key={}'.format(
        ip_position['latitude'],
        ip_position['longitude'],
        GOOGLE_API_KEY)
    reverse_geocode = requests.get(geocode_url).json()

    return render(request, 'landing.html', context={
        "ip_position": ip_position,
        "ip": get_ip(request),
        "geocode": reverse_geocode,
    }, context_instance=RequestContext(request))


def index(request):
    doc_path = 'https://docs.google.com/document/d/1NCCHyLKiSI7yHIZjbBGiIUg5_jFUOdTwgOa4vJjkYzM/pub?embedded=true'
    google_doc = requests.get(doc_path).text
    return render(request, 'index.html', context={
        "google_doc": google_doc
    }, context_instance=RequestContext(request))


def location_best_guess(request):
    location_response = requests.get('http://www.telize.com/geoip/{}'.format(get_ip(request)))

    location_info = location_response.json()

    latitude = 0
    longitude = 0

    if 'code' not in location_info or location_info['code'] != 401:
        latitude = location_info['latitude']
        longitude = location_info['longitude']

    return {"latitude": latitude, "longitude": longitude}
