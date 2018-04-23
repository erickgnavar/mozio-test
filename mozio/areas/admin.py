from django.contrib.gis import admin

from .models import ServiceArea


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.OSMGeoAdmin):

    list_display = ('name', 'price',)
    search_fields = ('name',)
    list_filter = ('provider',)
    autocomplete_fields = ('provider',)
