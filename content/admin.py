from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.contrib.gis import admin

from .models import Location, Language, LocationContent,AuthorizationToken


class LocationTitleInline(admin.StackedInline):
    model = LocationContent
    ordering = ('language', )
    extra = 0


class LocationAdmin(admin.GeoModelAdmin):
    default_lat = 48.69096
    default_lon = 12.480469
    default_zoom = 5

    inlines = [
        LocationTitleInline,
    ]
    list_display = ('id', 'name', 'country', 'enabled')
    list_filter = ('country',)
    search_fields = ('name', )
    prepopulated_fields = {"slug": ('name',)}


admin.site.register(Location, LocationAdmin)
admin.site.register(Language, admin.ModelAdmin)
admin.site.register(AuthorizationToken, admin.ModelAdmin)
