from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = 'reyrodrigues'

from django.contrib.gis import admin

from .models import Location, Language, LocationContent


class LocationTitleInline(admin.StackedInline):
    model = LocationContent
    ordering = ('language', )
    extra = 0


class LocationAdmin(admin.ModelAdmin):
    inlines = [
        LocationTitleInline,
    ]
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name', )


admin.site.register(Location, LocationAdmin)
admin.site.register(Language, admin.ModelAdmin)
