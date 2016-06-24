import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from . import models

Vehicle = models.Vehicle

def api(request, vin):
    if request.method == "GET":
        vehicle = Vehicle.objects.filter(vin=vin).all()

        if vehicle:
            data = json.loads(serializers.serialize("json", vehicle))[0]["fields"]
        else:
            data = {}

        return HttpResponse(json.dumps(data))

