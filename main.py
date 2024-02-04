import json
import math
import os
import random
import sys
import webbrowser
from dataclasses import dataclass
from functools import cached_property

from utils import Log

log = Log('walk')


@dataclass
class LatLng:
    lat: float
    lng: float

    @cached_property
    def tuple(self):
        return self.lat, self.lng

    def __str__(self) -> str:
        return f'{self.lat:.04f}N,{self.lng:.04f}E'
    
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
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c    
        return distance



    @cached_property
    def url_google_maps_place(self) -> str:
        return f'https://www.google.com/maps/place/{self}'

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
        return f'https://maps.google.com?saddr={saddr}&daddr={daddr}{waypoints}&dirflg={MODE}'

    @staticmethod
    def route_distance(latlng_list: list['LatLng']) -> float:
        distance = 0
        for i in range(len(latlng_list) - 1):
            distance += latlng_list[i].distance(latlng_list[i + 1])
        return distance

@dataclass
class Angle:
    angle_deg: float

    @cached_property
    def rad(self):
        return math.pi * self.angle_deg / 180

    def __str__(self) -> str:
        return f'{self.angle_deg:.1f}°'

    def __repr__(self) -> str:
        return f'{self.angle_deg:.1f}°'

    def __add__(self, other: 'Angle') -> 'Angle':
        assert isinstance(other, Angle)
        return Angle(self.angle_deg + other.angle_deg)

    def __sub__(self, other: 'Angle') -> 'Angle':
        assert isinstance(other, Angle)
        return Angle(self.angle_deg - other.angle_deg)

    def __neg__(self) -> 'Angle':
        return Angle(-self.angle_deg)

    @staticmethod
    def random():
        return Angle(random.uniform(0, 360))


MODE = 'w'  # walking
STEPS = 9
RADIUS = 0.004


def generate_path(seed: int):
    log.debug(f'{seed=}')
    random.seed(seed)
    latlng_home = LatLng.from_json(os.environ['LATLNG_HOME_JSON'])
    theta = Angle.random()
    log.debug(f'{theta=}')
    latlng_center = LatLng.from_center(latlng_home, RADIUS, theta)
    log.debug(f'{latlng_center=}')

    latlng_list = []
    for i in range(0, STEPS + 1):
        theta_i = theta - Angle(180) + Angle(360 * i / STEPS)
        log.debug(f'{theta_i=}, {i=}')
        latlng1 = LatLng.from_center(latlng_center, RADIUS, theta_i)
        latlng_list.append(latlng1)

    webbrowser.open(LatLng.url_google_maps_directions(latlng_list))
    crow_distance = LatLng.route_distance(latlng_list)
    log.info(f'{crow_distance=:.1f}km')

if __name__ == '__main__':
    seed = sys.argv[1]
    generate_path(seed)
