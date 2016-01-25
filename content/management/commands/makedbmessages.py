from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

import os

from django.core.management.base import BaseCommand
from content import models
from django.core.cache import cache
from content import utils


class Command(BaseCommand):
    help = 'Sync Docs from Folder Structure into Content'

    def handle(self, *args, **options):
        locations = models.Location.objects.all()
        for location in locations:
            print ("msgid \"{}\"".format(location.name))
            print ("msgstr \"\"")
            print("")