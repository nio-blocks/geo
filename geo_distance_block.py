from enum import Enum
from geopy.distance import great_circle, vincenty
from nio.metadata.properties import PropertyHolder, ExpressionProperty, \
    ObjectProperty, StringProperty, SelectProperty
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.util.attribute_dict import AttributeDict


class GeoPoint(PropertyHolder):
    latitude = ExpressionProperty(
        title='Latitude', default='{{ $lat }}', attr_default=AttributeError)
    longitude = ExpressionProperty(
        title='Longitude', default='{{ $lng }}', attr_default=AttributeError)


class DistanceType(Enum):
    Vincenty = vincenty
    GreatCircle = great_circle


@Discoverable(DiscoverableType.block)
class GeoDistance(Block):

    """ Compute the distance between two geographic points """

    point_1 = ObjectProperty(GeoPoint, title='First Point')
    point_2 = ObjectProperty(GeoPoint, title='Second Point')
    distance_method = SelectProperty(
        DistanceType, title='Distance Method', default=DistanceType.Vincenty)
    output_prop = StringProperty(
        title='Output Attribute', default='geodata', visible=False)

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            self._add_geodata_to_signal(signal)
        self.notify_signals(signals)

    def _add_geodata_to_signal(self, signal):
        """ Adds distance data to the signal """
        try:
            # The format expected by geopy is a tuple of two floats
            point_1 = (float(self.point_1.latitude(signal)),
                       float(self.point_1.longitude(signal)))
            point_2 = (float(self.point_2.latitude(signal)),
                       float(self.point_2.longitude(signal)))
        except:
            # If we can't build our points, we won't add the data to the
            # signal, but we still want the signal to pass through the block
            self._logger.exception("Unable to evaluate lat/lng")
            return

        try:
            # Use the configured distance method to retrieve the geopy distance
            distance = self.distance_method.value(point_1, point_2)

            # We will add some useful units to the signal
            geo_data = AttributeDict({
                "miles": distance.miles,
                "kilometers": distance.km,
                "meters": distance.meters,
                "feet": distance.feet
            })
            setattr(signal, self.output_prop, geo_data)
        except:
            self._logger.exception("Unable to compute distance")
