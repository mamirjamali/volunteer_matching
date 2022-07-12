from django.db import models
from django.contrib.auth.models import User

import geocoder
import os

from django.contrib.gis.db import models as gismoedls
from django.contrib.gis.geos import Point
# Create your models here.


class VolunteerCategory(models.TextChoices):
    water_and_land = ('Water & Land volunteering'(
        'Litter picking',
        'Tree planting & care',
        'Biodiversity protection',
        'Monitoring water quality'
    )
    )
    animal_protection = ('Animal Protection Volunteering'(
        'Animal rescue shelters',
        'Farm sanctuaries',
        'Hunt saboteurs',
        'Wildlife'
    )
    )


class PreferdTime(models.TextChoices):
    weekends = "Weekends"
    weekdays = "Weekdays"


class Volunteers(models.Model):
    email = models.ForeignKey(User.email, on_delete=CASCADE)
    address = models.CharField(max_length=100, null=False)
    volunteering_category = models.CharField(
        max_length=100,
        choices=VolunteerCategory.choices
        default=VolunteerCategory.water_and_land
    )
    preferd_time = models.CharField(
        max_length=100,
        choices=PreferdTime.choices
        default=PreferdTime.weekends
    )
    point = gismoedls.PointField(default=Point(0.0, 0.0))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapquest(self.address, key=os.environ.get('GEOCODER_API'))

        print(g)

        lng = g.lng
        lat = g.lat

        self.point = Point(lng, lat)
        super(Volunteers, self).save(*args, **kwargs)
