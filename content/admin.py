from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.contrib.gis import admin

from .models import Location, Language, LocationContent, AuthorizationToken


def disable_location(modeladmin, request, queryset):
    queryset.update(enabled=False)


disable_location.short_description = 'Disable location'


def enable_location(modeladmin, request, queryset):
    queryset.update(enabled=True)


enable_location.short_description = 'Enable location'


class LocationTitleInline(admin.StackedInline):
    model = LocationContent
    ordering = ('language', )
    extra = 0


class LocationAdmin(admin.GeoModelAdmin):
    default_lat = 48.69096
    default_lon = 12.480469
    default_zoom = 5
    openlayers_url = "https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js"

    inlines = [
        LocationTitleInline,
    ]
    list_display = ('id', 'name', 'country', 'enabled')
    list_filter = ('country',)
    search_fields = ('name', )
    prepopulated_fields = {"slug": ('name',)}
    actions = [enable_location, disable_location]


admin.site.register(Location, LocationAdmin)
admin.site.register(Language, admin.ModelAdmin)
admin.site.register(AuthorizationToken, admin.ModelAdmin)
