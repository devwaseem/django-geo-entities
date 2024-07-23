from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models.manager import Manager


class GeoRegion(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        ordering = ["name"]

    if TYPE_CHECKING:
        subregion_set = Manager["GeoSubRegion"]
        country_set = Manager["GeoCountry"]

    def __str__(self) -> str:
        return self.name


class GeoSubRegion(models.Model):
    id = models.AutoField(primary_key=True)

    region = models.ForeignKey(
        to=GeoRegion,
        on_delete=models.CASCADE,
        related_name="subregion_set",
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "SubRegion"
        verbose_name_plural = "SubRegions"
        ordering = ["name"]

    if TYPE_CHECKING:
        country_set = Manager["GeoCountry"]

    def __str__(self) -> str:
        return self.name


class GeoCountry(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    numeric_code = models.CharField(max_length=4)
    phone_code = models.CharField(max_length=10)
    capital = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    currency_name = models.CharField(max_length=255)
    currency_symbol = models.CharField(max_length=255)
    tld = models.CharField(max_length=10)
    native = models.CharField(max_length=255)
    region = models.ForeignKey(
        to=GeoRegion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="country_set",
    )
    subregion = models.ForeignKey(
        to=GeoSubRegion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="country_set",
    )
    nationality = models.CharField(max_length=255)

    if TYPE_CHECKING:
        state_set = Manager["GeoState"]

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class GeoState(models.Model):
    id = models.AutoField(primary_key=True)

    country = models.ForeignKey(
        to=GeoCountry,
        on_delete=models.CASCADE,
        related_name="state_set",
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    latitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )

    if TYPE_CHECKING:
        city_set = Manager["GeoState"]

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class GeoCity(models.Model):
    id = models.AutoField(primary_key=True)

    state = models.ForeignKey(
        to=GeoState,
        on_delete=models.CASCADE,
        related_name="city_set",
    )
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)
