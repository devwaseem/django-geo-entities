import codecs
import csv
import re
from contextlib import closing
from decimal import Decimal
from typing import Any

import requests
from django.db import transaction
from django_rich.management import RichCommand
from rich.status import Status

from django_geo_entities.models import (
    GeoCity,
    GeoCountry,
    GeoRegion,
    GeoState,
    GeoSubRegion,
)


class Command(RichCommand):
    help = "Download and update the data required geo entities"
    csv_base_url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/"

    def handle(self, *args: Any, **options: Any) -> None:
        with transaction.atomic(), self.console.status(
            "Starting..."
        ) as status:
            self.add_regions(status=status)
            self.add_subregions(status=status)
            self.add_countries(status=status)
            self.add_states(status=status)
            self.add_cities(status=status)

    def add_regions(self, *, status: Status) -> None:
        status.update("Downloading regions.csv...")
        with closing(
            thing=requests.get(
                url=self.csv_base_url + "regions.csv",
                stream=True,
            )
        ) as r:
            status.update("Saving Regions to DB...")
            reader = csv.reader(
                codecs.iterdecode(r.iter_lines(), "utf-8"),
                delimiter=",",
                quotechar='"',
            )
            next(reader)  # skip the header
            GeoRegion.objects.bulk_create(
                [
                    GeoRegion(
                        id=int(row[0]),
                        name=row[1],
                    )
                    for row in reader
                ],
                ignore_conflicts=True,
            )
            self.console.print("Regions saved to DB")

    def add_subregions(self, *, status: Status) -> None:
        status.update("Downloading subregions.csv...")
        with closing(
            thing=requests.get(
                url=self.csv_base_url + "subregions.csv",
                stream=True,
            )
        ) as r:
            status.update("Saving Subregions to DB...")
            reader = csv.reader(
                codecs.iterdecode(r.iter_lines(), "utf-8"),
                delimiter=",",
                quotechar='"',
            )
            next(reader)  # skip the header
            GeoSubRegion.objects.bulk_create(
                [
                    GeoSubRegion(
                        id=int(row[0]),
                        name=row[1],
                        region_id=int(row[2]),
                    )
                    for row in reader
                ],
                ignore_conflicts=True,
            )
            self.console.print("Subregions saved to DB")

    def add_countries(self, *, status: Status) -> None:
        status.update("Downloading countries.csv...")
        with closing(
            thing=requests.get(
                url=self.csv_base_url + "countries.csv",
                stream=True,
            )
        ) as r:
            status.update("Saving Countries to DB...")
            reader = csv.reader(
                codecs.iterdecode(r.iter_lines(), "utf-8"),
                delimiter=",",
                quotechar='"',
            )
            next(reader)  # skip the header
            model_list = []
            for row in reader:
                phone_code = ""
                if match := re.search(r"[\d-]", row[5]):
                    phone_code = match.group()

                model_list.append(
                    GeoCountry(
                        id=int(row[0]),
                        name=row[1],
                        iso3=row[2],
                        iso2=row[3],
                        numeric_code=row[4],
                        phone_code=phone_code,
                        capital=row[6],
                        currency=row[7],
                        currency_name=row[8],
                        currency_symbol=row[9],
                        tld=row[10],
                        native=row[11],
                        region_id=row[13],
                        subregion_id=row[15],
                        nationality=row[16],
                    )
                )
            GeoCountry.objects.bulk_create(model_list, ignore_conflicts=True)
            self.console.print("Countries saved to DB")

    def add_states(self, *, status: Status) -> None:
        status.update("Downloading states.csv...")
        with closing(
            thing=requests.get(
                url=self.csv_base_url + "states.csv",
                stream=True,
            )
        ) as r:
            status.update("Saving States to DB...")
            reader = csv.reader(
                codecs.iterdecode(r.iter_lines(), "utf-8"),
                delimiter=",",
                quotechar='"',
            )
            next(reader)  # skip the header
            GeoState.objects.bulk_create(
                [
                    GeoState(
                        id=int(row[0]),
                        country_id=int(row[2]),
                        name=row[1],
                        code=row[5],
                        latitude=Decimal(float(row[7])) if row[7] else None,
                        longitude=Decimal(float(row[8])) if row[8] else None,
                    )
                    for row in reader
                ],
                ignore_conflicts=True,
            )
            self.console.print("States saved to DB")

    def add_cities(self, *, status: Status) -> None:
        status.update("Downloading cities.csv...")
        with closing(
            thing=requests.get(
                url=self.csv_base_url + "cities.csv",
                stream=True,
            )
        ) as r:
            status.update("Saving cities to DB...")
            reader = csv.reader(
                codecs.iterdecode(r.iter_lines(), "utf-8"),
                delimiter=",",
                quotechar='"',
            )
            next(reader)  # skip the header
            GeoCity.objects.bulk_create(
                [
                    GeoCity(
                        id=int(row[0]),
                        state_id=int(row[2]),
                        name=row[1],
                        latitude=Decimal(float(row[8])) if row[8] else None,
                        longitude=Decimal(float(row[9])) if row[9] else None,
                    )
                    for row in reader
                ],
                ignore_conflicts=True,
            )
            self.console.print("Cities saved to DB")
