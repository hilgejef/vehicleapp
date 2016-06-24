from django.db import models

class Vehicle(models.Model):
    # These fields are shared between both JSON types
    vin = models.CharField(max_length=17, primary_key=True)
    make = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    year = models.IntegerField()
    description = models.CharField(max_length=256)
    odometer_value = models.DecimalField(decimal_places=6, max_digits=16)

    # These fields aren't shared between both JSON types, and can be
    # null in instances where one JSON type has been received while the
    # other has not.
    unit_type = models.CharField(max_length=64, null=True)
    url = models.CharField(max_length=256, null=True)
    powertrain = models.CharField(max_length=32, null=True)
    fleet = models.CharField(max_length=128, null=True)
    plate = models.CharField(max_length=7, null=True)
    last_measured_time = models.DateTimeField(null=True)

class Tracker(models.Model):
    username = models.CharField(max_length=64)
    vin = models.CharField(max_length=17)
    url = models.CharField(max_length=256)