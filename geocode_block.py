from enum import Enum
from geopy.geocoders import Nominatim
from nio.metadata.properties import ExpressionProperty, StringProperty
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.util.attribute_dict import AttributeDict


@Discoverable(DiscoverableType.block)
class Geocode(Block):

    """ Geolocate a query to an address and coordinates """

    query = ExpressionProperty(title='Query', default='175 5th Avenue NYC')
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
            query = self.query(signal)
        except:
            self._logger.exception("Unable to evaluate query")
            return
        try:
            self._logger.debug(
                "Geocode query \"{}\"".format(query))
            location = self._geolocator.geocode(query)
            self._logger.debug(
                "Geocode result for query \"{}\": {}".format(query, location))
            if not location:
                self._logger.warning(
                    "No geocode loaction for query: {}".format(query))
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
                "Unable to geocode location from query: {}".format(query))
        finally:
            if not getattr(signal, self.output_prop, None):
                setattr(signal, self.output_prop, None)
