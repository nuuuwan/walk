import json
import math
from dataclasses import dataclass
from functools import cached_property

from utils import Log

from utils_future.Angle import Angle

log = Log('LatLng')


@dataclass
class LatLng:
    lat: float
    lng: float

    DIRECTION_MODE = 'w'

    @cached_property
    def tuple(self):
        return self.lat, self.lng

    def __str__(self) -> str:
        return f'{self.lat:.06f}N,{self.lng:.06f}E'

    def distance(self, other: 'LatLng') -> float:
        lat1, lng1 = self.tuple
        lat2, lng2 = other.tuple

        R = 6371.0

        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)

        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad)
            * math.cos(lat2_rad)
            * math.sin(dlng / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    @cached_property
    def url_google_maps_place(self) -> str:
        return f'https://www.google.com/maps/place/{self}'
    
    @cached_property
    def url_google_maps_street_view(self) -> str:
        lat, lng = self.tuple
        return f'http://maps.google.com/maps?q=&layer=c&cbll={lat},{lng}&cbp='

    @staticmethod
    def from_center(
        latlng_center: 'LatLng', radius: float, theta: 'Angle'
    ) -> 'LatLng':
        latc, lngc = latlng_center.tuple
        LAT_FACTOR = 1
        return LatLng(
            latc + radius * LAT_FACTOR * math.cos(theta.rad),
            lngc + radius * math.sin(theta.rad),
        )

    @staticmethod
    def from_json(s: str) -> 'LatLng':
        lat, lng = json.loads(s)
        return LatLng(lat, lng)

    @staticmethod
    def url_google_maps_directions(latlng_list: list['LatLng']) -> str:
        saddr = latlng_list[0]
        daddr = latlng_list[1]
        waypoints = ','.join(
            [('+to:' + str(latlng)) for latlng in latlng_list[2:]]
        )
        return (
            'https://maps.google.com?'
            + f'saddr={saddr}&daddr={daddr}{waypoints}'
            + f'&dirflg={LatLng.DIRECTION_MODE}'
        )

    @staticmethod
    def route_distance(latlng_list: list['LatLng']) -> float:
        distance = 0
        for i in range(len(latlng_list) - 1):
            distance += latlng_list[i].distance(latlng_list[i + 1])
        return distance
