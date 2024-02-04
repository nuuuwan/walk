import os
import webbrowser

from utils import Log

from utils_future import Angle, LatLng

log = Log('Walk')


class Walk:
    STEPS = 3
    RADIUS = 0.005

    @staticmethod
    def generate(theta_deg: int):
        log.debug(f'{theta_deg=}')
        latlng_home = LatLng.from_json(os.environ['LATLNG_HOME_JSON'])
        theta = Angle(theta_deg)
        log.debug(f'{theta=}')
        latlng_center = LatLng.from_center(latlng_home, Walk.RADIUS, theta)
        log.debug(f'{latlng_center=}')

        latlng_list = []
        for i in range(0, Walk.STEPS + 1):
            theta_i = theta - Angle(180) + Angle(360 * i / Walk.STEPS)
            log.debug(f'{theta_i=}, {i=}')
            latlng1 = LatLng.from_center(latlng_center, Walk.RADIUS, theta_i)
            latlng_list.append(latlng1)
            if i > 0 and i < Walk.STEPS:
                webbrowser.open(latlng1.url_google_maps_street_view)

        webbrowser.open(LatLng.url_google_maps_directions(latlng_list))
        crow_distance = LatLng.route_distance(latlng_list)
        log.info(f'{crow_distance=:.1f}km')
