from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'lookup$', views.location_from_device, name="lookup-device"),
    url(r'page/(?P<page_id>\d+)/(?P<language>[a-zA-Z]+)/$', views.index),

    url(r'(?P<slug>[a-zA-Z]+)/(?P<language>[a-zA-Z]+)//?$', views.slug_index, name="slug_index" ),

    url(r'(?P<slug>[a-zA-Z]+)/?$', views.slug_no_language, ),

    url(r'$', views.landing),

]
