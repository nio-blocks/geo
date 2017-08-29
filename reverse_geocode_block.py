from nio.properties import (Property, ObjectProperty, PropertyHolder,
                            VersionProperty)
from nio.util.discovery import discoverable
from .geocode_base import GeocodeBase


class GeoPoint(PropertyHolder):
    latitude = Property(
        title='Latitude', default='{{ $lat }}')
    longitude = Property(
        title='Longitude', default='{{ $lng }}')


@discoverable
class ReverseGeocode(GeocodeBase):

    """ Find the address corresponding to a set of coordinates """

    version = VersionProperty("1.0.0")
    location = ObjectProperty(
        GeoPoint, title='Query Location', default=GeoPoint())

    def _get_query_from_signal(self, signal):
        try:
            latitude = float(self.location().latitude(signal))
            longitude = float(self.location().longitude(signal))
            return (latitude, longitude)
        except:
            self.logger.exception("Unable to evaluate location property")

    def _get_location(self, query):
        return self._geolocator.reverse(query)
