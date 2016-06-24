import datetime
import json
import urllib
from decimal import Decimal
from django.utils import timezone
from django.core import serializers
from . import api_simulator
from . import models

simulate_api_call = api_simulator.simulate_api_call
Vehicle = models.Vehicle
Tracker = models.Tracker

def normalize_json(a_type_json, b_type_json):
	a_type_json = json.loads(a_type_json)
	b_type_json = json.loads(b_type_json)["vehicle"]
	vehicle = {}

	# Check that shared keys are symmetric
	assert a_type_json["vin"] == b_type_json["vin"]
	assert a_type_json["year"] == b_type_json["year"]
	assert a_type_json["make"] == b_type_json["make"]
	assert a_type_json["model"] == b_type_json["model"]
	assert a_type_json["year"] == b_type_json["year"]

	# Should nickname and description not match? Comment out 1st
	# line and comment in second line
	assert a_type_json["description"] == b_type_json["nickname"]
	# vehicle["nickname"] = b_type_json["nickname"]

	# Copy k/vs from a_type_json to vehicle
	for key in ["vin", "make", "model", "powertrain",
				"plate", "description", "fleet"]:
		vehicle[key] = a_type_json[key]

	# Copy k/vs from b_type_json to vehicle:
	vehicle["url"] = b_type_json["url"]
	vehicle["unit_type"] = b_type_json["unitType"]

	# Copy year, converting to int
	vehicle["year"] = int(a_type_json["year"])

	# Create decimal values for odometer value each json type
	a_odom_value = Decimal(a_type_json["odometer"]["lastMeasuredValue"])
	b_odom_value = Decimal(b_type_json["odometerValue"])

	# The method used here is to collapse odometer values into one by
	# prioritizing the highest (and therefore most recent) value
	# Another, possibly better option could be to preserve both values in
	# the vehicle dictionary (an a_odom_value key and a b_odom_value key)
	if a_odom_value >= b_odom_value:
		vehicle["odometer_value"] = a_odom_value

		# Create a datetime object from lastMeasuredtime
		# Split lastMeasuredTime into year ... microseconds
		date, time = a_type_json["odometer"]["lastMeasuredTime"].split("T")
		year, month, day = date.split("-")
		time, microseconds = time.split(".")
		hour, minute, second = time.split(":")

		# Convert year ... microseconds into integers, and pass to datetime.datetime
		fulltime = map(int, [year, month, day, hour, minute, second, microseconds])
		last_measured_time = datetime.datetime(*fulltime)

		vehicle["last_measured_time"] = last_measured_time

	else:
		vehicle["odometer_value"] = b_odom_value

		# This is arguable, but here I've chosen to set last_measured_time to None
		# in instances where the b_type odometer value is the most recent.
		vehicle["last_measured_time"] = None

	return vehicle

# Simulates making an API call, normalizes the 'received' JSON data, creates
# a vehicle object from the normalized data and saves it to the db
def make_api_calls():
    data = normalize_json(*simulate_api_call())
    vehicle = Vehicle(**data)
    vehicle.save()

    # This part sends post data to trackers for vin number
    send_to_trackers(data["vin"])

# This function searches for all trackers with a specified vin number, then
# sends post data to the urls associated with that tracker
def send_to_trackers(vin):
    vehicle = Vehicle.objects.filter(vin=vin).all()
    vehicle_dic = json.loads(serializers.serialize("json", vehicle))[0]["fields"]

    trackers = Tracker.objects.filter(vin=vin).all()
    for tracker in trackers:
        send_post_data(tracker.url, vehicle_dic)

# This function converts a k/v dictionary into 2-tuples which are then
# sent as post data to a specified url
def send_post_data(url, json_dic):
    params = []
    for k, v in json_dic.items():
        params.append((k, v))

    urllib.request.urlopen(url, data=urllib.parse.urlencode(params).encode('utf-8'))

# For testing, calls make_api_call
if __name__ == "__main__":
    vin = make_api_calls()
    print("Saved vehicle {} data".format(vin))

