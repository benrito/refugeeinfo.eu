from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.conf.urls import url, include
from . import views

from content import api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'locations', api.LocationViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^map/', views.map),
    url(r'^lookup$', views.location_from_device, name="lookup-device"),
    url(r'^page/(?P<page_id>\d+)/(?P<language>[a-zA-Z]+)/$', views.index),

    url(r'^(?P<slug>[a-zA-Z\-0-9]+)/(?P<language>[a-zA-Z]+)/?$', views.slug_index, name="slug_index"),

    url(r'^(?P<slug>[a-zA-Z\-0-9]+)/?$', views.slug_no_language, ),

    url(r'^/?$', views.landing),

]
