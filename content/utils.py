from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.conf import settings

from lxml import etree
from lxml.cssselect import CSSSelector

import requests
from StringIO import StringIO


def get_cms_url(language, slug):
    return settings.CMS_URL + '/{}/{}/{}/'.format(language, settings.CMS_ENVIRONMENT, slug)


def get_cms_page(language, slug):
    cms_url = get_cms_url(language, slug)
    cms_url_en = get_cms_url(language, slug)

    print('Requesting: ', cms_url)

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
    """
    Takes in HTML from the CMS, removes headers, footers and Javascript and spits out the content to be cached.

    It also goes into the content looks for all <tables /> and adds a div.table-responsive around it
    :param text:
    :return:
    """
    result = text

    try:
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(text), parser)
        selector = CSSSelector('div.cms-content')

        body = selector(tree.getroot())

        if len(body):
            result = ""
            for c in body:
                table_selector = CSSSelector('table:not(.toc)')
                for table in table_selector(c):
                    # Removes Table from HTML
                    parent = table.getparent()
                    sibling = table.getprevious()
                    parent.remove(table)
                    # Attaches a div to it
                    d = etree.Element('div', attrib={"class": "table-responsive"})
                    d.append(table)

                    # Inserts into back to the document at the same point
                    parent.insert(parent.index(sibling) + 1, d)

                result += etree.tostring(c, pretty_print=True, method="html")
    except Exception as e:
        pass

    return result