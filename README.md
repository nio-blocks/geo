GeoDistance
===========
Computes the geographic distance between two lat/longs. This block will add geographic distance data in several different units to incoming signals. Normally, the incoming signals will have the latitude and longitude data for at least one of the points on them. If the block cannot determine both of the points' latitudes and longitudes, the signal will still be notified, but no geodata will be added to the signal.

Properties
----------
- **distance_method**: The algorithm used to compute the distance. See [Vincenty](https://en.wikipedia.org/wiki/Vincenty's_formulae) or [Great Circle](https://en.wikipedia.org/wiki/Great-circle_distance) on Wikipedia for more information.
- **output_prop**: The attribute on the signal to add the geo data to.
- **point_1**: The first point to use in the distance calculation.
- **point_2**: The second point to use in the distance calculation.

Inputs
------
- **default**: Signals with latitude and longitude data for distance calculation.

Outputs
-------
- **default**: Input signals enriched with geo data.

Commands
--------
None

Dependencies
------------
[geopy](https://github.com/geopy/geopy)

Input
-----
Any list of signals.

Output
------
Same list of signals as input, but with `geodata` (or whatever `output_prop` is set to) set to an `AttributeDict` with the following format:
```python
{
  'feet': 2842701.55042702,
  'kilometers': 866.4554329011002,
  'meters': 866455.4329011001,
  'miles': 538.3904451566326
}
```

Geocode
=======
Geolocate a query to an address and coordinates.

Properties
----------
- **output_prop**: The attribute on the signal to add the geo data to.
- **query**: The location to geocode.

Inputs
------
- **default**: Signals with with a location to geolocate.

Outputs
-------
- **default**: Input signals enriched with geo data.

Commands
--------
None

Dependencies
------------
[geopy](https://github.com/geopy/geopy)

Input
-----
Any list of signals.

Output
------
Same list of signals as input, but with `geodata` (or whatever `output_prop` is set to) set to an `AttributeDict` with the following format:
```python
{
  'address': location.address,
  'altitude': location.altitude,
  'latitude': location.latitude,
  'longitude': location.longitude,
  'raw': location.raw
}
```

ReverseGeocode
==============
Find the address corresponding to a set of coordinates.

Properties
----------
- **location**: The location to geocode.
- **output_prop**: The attribute on the signal to add the geo data to.

Inputs
------
- **default**: Signals with with a latitude and longitude to geolocate.

Outputs
-------
- **default**: Input signals enriched with geo data.

Commands
--------
None

Dependencies
------------
[geopy](https://github.com/geopy/geopy)

Input
-----
Any list of signals.

Output
------
Same list of signals as input, but with `geodata` (or whatever `output_prop` is set to) set to an `AttributeDict` with the following format:
```python
{
  'address': location.address,
  'altitude': location.altitude,
  'latitude': location.latitude,
  'longitude': location.longitude,
  'raw': location.raw
}
```

