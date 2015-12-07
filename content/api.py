from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from rest_framework import serializers, viewsets
from . import models
from django.core.cache import cache

from StringIO import StringIO
from lxml import etree
from lxml.cssselect import CSSSelector


class LocationSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    # content = serializers.SerializerMethodField()
    # parent_id = serializers.SerializerMethodField()

    def get_location(self, obj):
        return dict(type="Point", coordinates=[obj.area.centroid.x, obj.area.centroid.y])

    def get_languages(self, obj):
        return [dict(iso_code=l.language.iso_code, name=l.language.name) for l in obj.content.all()]

    def get_content(self, obj):

        url_parts = [obj.slug]
        m = obj
        while m.parent:
            url_parts.append(m.parent.slug)
            m = m.parent

        complete_url = '/'.join(reversed(url_parts))
        parse_content = lambda l: (l.language.iso_code, self._fetch_from_cache(l.language.iso_code, complete_url))

        content = dict([parse_content(l) for l in obj.content.all()])
        return content

    def get_parent_id(self, obj):
        return obj.parent_id

    @staticmethod
    def _fetch_from_cache(language, url):
        from . import utils

        cms_url = utils.get_cms_url(language, url)

        if cms_url in cache:
            html = cache.get(cms_url)
        else:
            html = utils.get_cms_page(language, url)
            cache.set(cms_url, html)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser).getroot()
        toc = CSSSelector('.toc')

        # Removing all table of contents
        for table in toc(tree):
            table.getparent().remove(table)

        title = CSSSelector('.page-title')(tree)[0]
        title.getparent().remove(title)

        elements = list(CSSSelector('.cms-content')(tree)[0])

        headers = [i for i, e in enumerate(elements) if CSSSelector('.section-header')(e)]

        page_contents = []

        for i, h in enumerate(headers):
            element = elements[h]
            if (i + 1) == len(headers):
                contents = elements[h + 1:]
            else:
                contents = elements[h + 1:headers[i + 1]]

            for e in elements:
                if 'dir' in e.attrib:
                    del e.attrib['dir']

            section_title = CSSSelector('a[name]')(element)[0].text
            section_body = ""
            for c in contents:
                section_body += etree.tostring(c, pretty_print=True, method="html")

            page_contents.append({
                "is_important": True if CSSSelector('.important')(element) else False,
                "title": section_title,
                "body": section_body
            })

        return {
            "title": title.text,
            "contents": page_contents
        }

    class Meta:
        model = models.Location
        fields = (
            'id',
            'name',
            'slug',
            'location',
            'languages',
            #'content',
            #'parent_id'
        )


class LocationViewSet(viewsets.ModelViewSet, ):
    queryset = models.Location.objects.filter(enabled=True)
    serializer_class = LocationSerializer


    def get_queryset(self):
        country = self.request.query_params.get('country', None)

        if country is not None:
            queryset = self.queryset.filter(country=country)
        else:
            queryset = self.queryset.none()

        return queryset