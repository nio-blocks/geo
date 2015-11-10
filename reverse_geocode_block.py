from enum import Enum
from geopy.geocoders import Nominatim
from nio.metadata.properties import ExpressionProperty, StringProperty, \
    ObjectProperty, PropertyHolder
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.util.attribute_dict import AttributeDict


class GeoPoint(PropertyHolder):
    latitude = ExpressionProperty(
        title='Latitude', default='{{ $lat }}', attr_default=AttributeError)
    longitude = ExpressionProperty(
        title='Longitude', default='{{ $lng }}', attr_default=AttributeError)


@Discoverable(DiscoverableType.block)
class ReverseGeocode(Block):

    """ Find the address corresponding to a set of coordinates """

    location = ObjectProperty(GeoPoint, title='Query Location')
    output_prop = StringProperty(
        title='Output Attribute', default='location', visible=False)

    def __init__(self):
        super().__init__()
        self._geolocator = None

    def configure(self, context):
        super().configure(context)
        self._geolocator = Nominatim()

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            self._add_location_to_signal(signal)
        self.notify_signals(signals)

    def _add_location_to_signal(self, signal):
        """ Adds location data to the signal """
        try:
            latitude = float(self.location.latitude(signal))
            longitude = float(self.location.longitude(signal))
            latlong = (latitude, longitude)
        except:
            self._logger.exception("Unable to evaluate location property")
            setattr(signal, self.output_prop, None)
            return
        try:
            self._logger.debug(
                "Geocode location \"{}\"".format(latlong))
            location = self._geolocator.reverse(latlong)
            self._logger.debug(
                "Geocode result for location \"{}\": {}".format(latlong, location))
            if not location:
                self._logger.warning(
                    "No geocode loaction for location: {}".format(latlong))
                return
            location_dict = AttributeDict({
                'address': location.address,
                'altitude': location.altitude,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'raw': location.raw
            })
            setattr(signal, self.output_prop, location_dict)
        except:
            self._logger.exception(
                "Unable to geocode location from location: {}".format(latlong))
        finally:
            if not getattr(signal, self.output_prop, None):
                setattr(signal, self.output_prop, None)
