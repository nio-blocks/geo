from nio.properties import Property
from nio.util.discovery import discoverable
from .geocode_base import GeocodeBase


@discoverable
class Geocode(GeocodeBase):

    """ Geolocate a query to an address and coordinates """

    query = Property(title='Query', default='175 5th Avenue NYC')

    def _get_query_from_signal(self, signal):
        try:
            return self.query(signal)
        except:
            self.logger.exception("Unable to evaluate query")

    def _get_location(self, query):
        return self._geolocator.geocode(query)
