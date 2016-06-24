### How would you design a web application that would routinely intake both versions of the JSON, normalize it, and persist it to a database?

1. Use a scheduler to routinely activate a script that ingests JSON from both API providers.
2. Pass the JSON strings to a normalizer function that functions as follows:
3. Both JSON strings are converted to Python objects
4. Common keys (vin, make, model, year, possibly description/nickname) are checked for equality
5. Collapse description and nickname to one field if necessary
6. Convert year to integer
7. Should odometerValue and lastMeasuredValue be collapsed into one value?

   If so, then both values are converted to Decimal, and the highest (and therefore more recent value) is retained. If lastMeasuredValue is higher, convert lastMeasuredTime to a DateTime object.

   If not, then simply retain both values.
8. Copy keys from A and B into a new dictionary and return it.
9. Create a Vehicle model object (see Q3) from normalized dictionary and call save function.

[Code here.](https://github.com/hilgejef/vehicleapp/blob/master/vehicleapp/make_api_calls.py)

### How would you design a web application that would push odometer data to the data consumer as quickly as possible after intaking it from the data providers?

1. Create an API that data consumers can query in an on-demand fashion for up to date information.

[Example here.](http://hilger.pythonanywhere.com/vehicleapp/api/GKUKEEF9AR000010/)
[Code here.](https://github.com/hilgejef/vehicleapp/blob/master/vehicleapp/views.py)

2. Send information via POST request to designated urls

[Code here.](https://github.com/hilgejef/vehicleapp/blob/master/vehicleapp/make_api_calls.py)

3. Other options: email, SMS

### Under a Django architecture, what would the Django code representing the normalized vehicle data look like?

A Vehicle class that inherits from models.Models in models.py and has:

1. CharFields of varying length for vin, make, model, description, unit_type, url, powertrain, fleet and plate.
2. IntegerField for the year.
3. DecimalField for the odometer value.
4. DateTimeField for the last measured time.

[Code here.](https://github.com/hilgejef/vehicleapp/blob/master/vehicleapp/models.py)

### How would you secure the consumer and provider web services?

1. Salt/hash passwords.
2. Enable CSRF protection.
3. SSL/HTTPS
4. Authentications/Permissions/Groups --

   For example, you can restrict the API query view from users who aren't authenticated.