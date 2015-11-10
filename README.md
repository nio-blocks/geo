Geocode
=======

Geolocate a query to an address and coordinates

Properties
----------
 * Query - the location to geocode
 * output_prop *(hidden)* - The attribute on the signal to add the geo data to. Defaults to **geodata**

Dependencies
------------
[geopy](https://github.com/geopy/geopy)

Commands
--------
None

Input
-----
Any list of signals.

Output
------
Same list of signals as input, but with **location** (or whatever `output_prop` is set to) set to an `AttributeDict` with the following format:

```python
{
  'address': location.address,
  'altitude': location.altitude,
  'latitude': location.latitude,
  'longitude': location.longitude,
  'raw': location.raw
}
```

GeoDistance
===========

Computes the geographic distance between two lat/longs.

This block will add geographic distance data in several different units to incoming signals. Normally, the incoming signals will have the latitude and longitude data for at least one of the points on them. If the block cannot determine both of the points' latitudes and longitudes, the signal will still be notified, but no geodata will be added to the signal.

Properties
----------
 * First Point - the first point to use in the distance calculation
   * latitude: Something that evaluates to a floating point latitude. Use +/- rather than N/S
   * longitude: Something that evaluates to a floating point latitude. Use +/- rather than E/W
 * Second Point - the second point to use in the distance calculation
   * latitude: Something that evaluates to a floating point latitude. Use +/- rather than N/S
   * longitude: Something that evaluates to a floating point latitude. Use +/- rather than E/W
 * Distance Method - The algorithm used to compute the distance. See [Vincenty](https://en.wikipedia.org/wiki/Vincenty's_formulae) or [Great Circle](https://en.wikipedia.org/wiki/Great-circle_distance) on Wikipedia for more information
 * output_prop *(hidden)* - The attribute on the signal to add the geo data to. Defaults to **geodata**
 

Dependencies
------------
[geopy](https://github.com/geopy/geopy)

Commands
--------
None

Input
-----
Any list of signals.

Output
------
Same list of signals as input, but with **geodata** (or whatever `output_prop` is set to) set to an `AttributeDict` with the following format:

```python
{
  'feet': 2842701.55042702,
  'kilometers': 866.4554329011002,
  'meters': 866455.4329011001,
  'miles': 538.3904451566326
}
```
