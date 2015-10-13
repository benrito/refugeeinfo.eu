from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

import os

import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client

from django.core.management.base import BaseCommand
from content import models


class Command(BaseCommand):
    help = 'Refresh tokens'

    def handle(self, *args, **options):
        gdrive_tokens = models.AuthorizationToken.objects.filter(type=1)
        for t in gdrive_tokens:
            credentials_text = t.token_text
            credentials = oauth2client.client.Credentials.new_from_json(credentials_text)

            credentials.refresh(httplib2.Http())

            t.token_text = credentials.to_json()
            t.save()

            print ("Refreshed Google Drive")