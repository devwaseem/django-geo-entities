from django.contrib import admin

from django_geo_entities.models import (
    GeoCity,
    GeoCountry,
    GeoRegion,
    GeoState,
    GeoSubRegion,
)


@admin.register(GeoRegion)
class GeoRegionAdmin(admin.ModelAdmin):  # type: ignore
    list_per_page = 20


@admin.register(GeoSubRegion)
class GeoSubRegionAdmin(admin.ModelAdmin):  # type: ignore
    list_select_related = ["region"]
    list_display = ["name", "region"]
    list_filter = ["region"]
    list_per_page = 20


@admin.register(GeoCountry)
class GeoCountryAdmin(admin.ModelAdmin):  # type: ignore
    list_select_related = ["region", "subregion"]
    list_display = ["name", "iso3", "iso2", "currency", "region", "subregion"]
    list_filter = ["region", "subregion"]
    list_per_page = 20


@admin.register(GeoState)
class GeoStateAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ["name", "country", "code"]
    list_filter = ["country"]
    list_per_page = 20


@admin.register(GeoCity)
class GeoCityAdmin(admin.ModelAdmin):  # type: ignore
    list_select_related = ["state", "state__country", "state__country__region"]
    list_display = ["name", "state", "country_display", "region_display"]
    list_filter = ["state", "state__country"]
    list_per_page = 20

    def country_display(self, obj: GeoCity) -> str:
        return str(obj.state.country.name)

    def region_display(self, obj: GeoCity) -> str:
        if (
            (state := obj.state)
            and (country := state.country)
            and (region := country.region)
        ):
            return str(region.name)
        return "-"
