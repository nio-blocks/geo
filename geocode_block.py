from nio.metadata.properties import ExpressionProperty
from nio.common.discovery import Discoverable, DiscoverableType
from .geocode_base import GeocodeBase


@Discoverable(DiscoverableType.block)
class Geocode(GeocodeBase):

    """ Geolocate a query to an address and coordinates """

    query = ExpressionProperty(title='Query', default='175 5th Avenue NYC',
                               attr_default=AttributeError)

    def _get_query_from_signal(self, signal):
        try:
            return self.query(signal)
        except:
            self._logger.exception("Unable to evaluate query")

    def _get_location(self, query):
        return self._geolocator.geocode(query)
