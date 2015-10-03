from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'', views.index),
]
