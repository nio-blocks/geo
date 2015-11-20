from nio.metadata.properties import ExpressionProperty, \
    ObjectProperty, PropertyHolder
from nio.common.discovery import Discoverable, DiscoverableType
from .geocode_base import GeocodeBase


class GeoPoint(PropertyHolder):
    latitude = ExpressionProperty(
        title='Latitude', default='{{ $lat }}', attr_default=AttributeError)
    longitude = ExpressionProperty(
        title='Longitude', default='{{ $lng }}', attr_default=AttributeError)


@Discoverable(DiscoverableType.block)
class ReverseGeocode(GeocodeBase):

    """ Find the address corresponding to a set of coordinates """

    location = ObjectProperty(GeoPoint, title='Query Location')

    def _get_query_from_signal(self, signal):
        try:
            latitude = float(self.location.latitude(signal))
            longitude = float(self.location.longitude(signal))
            return (latitude, longitude)
        except:
            self._logger.exception("Unable to evaluate location property")

    def _get_location(self, query):
        return self._geolocator.reverse(query)
