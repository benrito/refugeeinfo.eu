from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.conf import settings

from lxml import etree
import requests
from StringIO import StringIO


def get_cms_url(language, slug):
    return settings.CMS_URL + '/{}/{}/{}/'.format(language, settings.CMS_ENVIRONMENT, slug)


def get_cms_page(language, slug):
    cms_url = get_cms_url(language, slug)
    cms_url_en = get_cms_url(language, slug)

    r = requests.get(cms_url,
                     headers={"Accept-Language": language},
                     auth=(settings.CMS_USER, settings.CMS_PASSWORD)
    )

    if r.status_code == 200:
        html_content = r.text
    elif language != 'en':
        r = requests.get(cms_url_en,
                         headers={"Accept-Language": language},
                         auth=(settings.CMS_USER, settings.CMS_PASSWORD)
        )
        if r.status_code == 200:
            html_content = r.text
        else:
            html_content = ""
    else:
        html_content = ""

    return _get_body_content(html_content)


def _get_body_content(text):
    result = text

    try:
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(text), parser)
        body = tree.getroot().xpath('body')

        if len(body):
            body = body[0]
            result = ""
            for c in body.getchildren():
                result += etree.tostring(c, pretty_print=True, method="html")
    except Exception as e:
        pass

    return result