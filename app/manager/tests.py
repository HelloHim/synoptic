from django.test import TestCase  # noqa: F401

from .models import WaterReading
from sensor.models import Sensor
from django.contrib.gis.geos import Point


class WaterReadingTest(TestCase):
    def setUp(self):
        sensor = Sensor.objects.create(point=Point(0, 0), name='Sensor 1')
        clean = WaterReading.objects.create(
            level=1.5,
            orp=250,
            ph=7,
            bod=1.2,
            temperature=24.4,
            sensor=sensor,
        )

        # Create multiple unclean readings
        unclean_reading = [
            WaterReading(
                level=1.5,
                orp=190,  # orp lower than 200
                ph=7,
                bod=1.2,
                temperature=24.4,
                sensor=sensor,
            ),
            WaterReading(
                level=1.5,
                orp=650,  # orp higher than 650
                ph=7,
                bod=1.2,
                temperature=24.4,
                sensor=sensor,
            ),
            WaterReading(
                level=1.5,
                orp=250,
                ph=9,  # ph is higher than 8.5
                bod=1.2,
                temperature=24.4,
                sensor=sensor,
            ),
            WaterReading(
                level=1.5,
                orp=250,
                ph=5.4,  # ph is lower than 6.5
                bod=1.2,
                temperature=24.4,
                sensor=sensor,
            ),
            WaterReading(
                level=1.5,
                orp=250,
                ph=7,
                bod=2.5,  # bod is higher than 2
                temperature=24.4,
                sensor=sensor,
            ),
            WaterReading(
                level=1.5,
                orp=250,
                ph=7,
                bod=0.2,  # bod is lower than 1
                temperature=24.4,
                sensor=sensor,
            ),
        ]

        # Bulk create the records
        WaterReading.objects.bulk_create(unclean_reading)

        self.clean_id = clean.id
        # for some reason, type hinting is not working here,
        # but this is an attribute of the class

    def test_is_clean(self):
        clean = WaterReading.objects.get(id=self.clean_id)

        self.assertTrue(clean.clean_condition())

    def test_is_dirty(self):
        # Don't get the water that is clean
        dirty = WaterReading.objects.exclude(id=self.clean_id)

        for water in dirty:
            self.assertFalse(water.clean_condition())
