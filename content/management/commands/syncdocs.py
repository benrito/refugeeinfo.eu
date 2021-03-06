from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

import os

import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client

from django.core.management.base import BaseCommand
from content import models
import requests
from django.core.cache import cache
from content import utils


class Command(BaseCommand):
    help = 'Sync Docs from Folder Structure into Content'

    def handle(self, *args, **options):
        locations = models.Location.objects.filter(managed_locally=True)
        for location in locations:
            url_parts = [location.slug]
            m = location
            while m.parent:
                url_parts.append(m.parent.slug)
                m = m.parent

            complete_url = '/'.join(reversed(url_parts))

            languages = models.Language.objects.all()
            for l in languages:
                cms_url = utils.get_cms_url(l.iso_code, complete_url)
                html_content = utils.get_cms_page(l.iso_code, complete_url)
                cache.set(cms_url, html_content)
        try:
            gdrive_tokens = models.AuthorizationToken.objects.filter(type=1)
            if not gdrive_tokens:
                return

            credentials_text = gdrive_tokens[0].token_text
            credentials = oauth2client.client.Credentials.new_from_json(credentials_text)

            documents, includes = self._list_folders(credentials)

            for key in documents.iterkeys():
                document_link = documents[key]['exportLinks']['text/html']

                try:
                    if '-' in key:
                        identifier = key.split('-')
                        location = models.Location.objects.filter(slug='-'.join(identifier[:-1]), managed_locally=False)
                        language = models.Language.objects.filter(iso_code=identifier[-1])

                        if location and language:
                            location = location[0]
                            language = language[0]

                            existing_content = models.LocationContent.objects.filter(parent=location,
                                                                                     language=language)
                            if existing_content:
                                content = existing_content[0]
                                content.html_url = document_link
                                content.title = location.name
                                content.save()
                            else:
                                models.LocationContent.objects.create(parent=location, language=language,
                                                                      title=location.name,
                                                                      html_url=document_link)

                            content = requests.get(document_link).text
                            cache.set(document_link, content)
                except Exception as e:
                    print(e.message)
                    print("Error loading one of the files: {}.".format(key))
        except Exception as e:
            pass

        self.stdout.write('Successfully created/updated content!')

    def _list_folders(self, credentials):
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v2', http=http)

        folder_id = os.environ.get('FOLDER_ID', '')

        request = service.children().list(folderId=folder_id,
                                          q="mimeType= 'application/vnd.google-apps.document'"
                                            " or mimeType= 'application/vnd.google-apps.folder'")

        main_folder = request.execute().get('items', [])
        expanded = [e for e in self._expand_folder(service, main_folder) if 'exportLinks' in e]

        documents = dict([(p['title'], p) for p in expanded if 'include' not in p['title']])
        includes = dict([(p['title'], p) for p in expanded if 'include' in p['title']])

        return documents, includes

    def _expand_folder(self, service, parent):
        children = []
        for p in parent:
            f = service.files().get(fileId=p['id']).execute()
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                grand_children = service.children().list(folderId=f['id']).execute().get('items', [])
                children += self._expand_folder(service, grand_children)

            children.append(f)

        return children
