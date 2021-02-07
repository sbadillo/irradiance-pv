import math
import pandas as pd
import numpy as np
from spa_delft import solar_position
import time


class PVSystem:
    """The class represents a pv system array and its general attributes.

    Args :
    - times : a pandas timeseries
    - latitude, longitude : decimal coordinates of system's location
    - elevation : distance aboves sea level

    - surface_azimuth
    - surface_tilt

    A surface facing south has an array azimuth of 180 deg.
    Surface tilt is defined as the angle from horizontal.
    Azimuth angle convention is defined as degrees east of north (e.g. North = 0, East = 90, West = 270).
    Array azimuth is defined as the horizontal normal vector from the array surface.

    """

    def __init__(
        self,
        times,
        latitude,
        longitude,
        elevation=0,
        surface_azimuth=180,
        surface_tilt=0,
    ):

        self.times = times
        self.lat = latitude
        self.lon = longitude
        self.elev = elevation
        self.surface_azimuth = surface_azimuth
        self.surface_tilt = surface_tilt
        self.sun_pos = []

    def __repr__(self):

        attrs = [
            self.lat,
            self.lon,
            self.surface_azimuth,
            self.surface_tilt,
        ]
        return "PV System at Lat {} Lon {}. Array azimuth: {} tilt: {}".format(*attrs)

    def get_solar_pos(self):

        df = pd.DataFrame(self.times, columns=["time"])

        start = time.time()
        print("calculating sun positions")

        df[["elevation", "azimuth"]] = df.apply(
            lambda x: solar_position(x, self.lat, self.lon),
            axis=1,
            result_type="expand",
        )

        end = time.time()

        print("done in", end - start)

        print(df)

    # def get_solar_pos(
    #     self, pressure=101325, temperature=12, delta_t=67.0, atmos_refract=None
    # ):
    #     """
    #     Calculates the position of the sun relative to an observer on the surface of the Earth.
    #     The convention used to describe solar positions includes the parameters :
    #     - Zenith Angle : measured from observer's zenith (observers plane normal).
    #     - Azimuth Angle : measured in relation to North.
    #     - Solar Elevation Angle : measured up from the horizon and equal to 90deg - Zenith Angle.

    #     pressure : int or float, optional, default 101325
    #         avg. yearly air pressure in Pascals.
    #     temperature : int or float, optional, default 12
    #         avg. yearly air temperature in degrees C.
    #     delta_t : float, optional, default 67.0
    #         If delta_t is None, uses spa.calculate_deltat
    #         using time.year and time.month from pandas.DatetimeIndex.
    #         For most simulations specifing delta_t is sufficient.
    #         Difference between terrestrial time and UT1.
    #         *Note: delta_t = None will break code using nrel_numba,
    #         this will be fixed in a future version.*
    #         The USNO has historical and forecasted delta_t [3].
    #     atmos_refrac : None or float, optional, default None
    #         The approximate atmospheric refraction (in degrees)
    #         at sunrise and sunset.

    #     Args:

    #     Returns:

    #     """

    #     pressure = pressure / 100  # pressure must be in millibars for calculation
    #     atmos_refract = atmos_refract or 0.5667

    #     lat = self.lat
    #     lon = self.lon
    #     elev = self.elev

    #     solar_pos = []
    #     for t in self.times:
    #         print(t)

    #     pass

    def get_aoi(self, solar_azimuth, solar_zenith):
        """Calculates the angle of incidence between
        the Sun's rays and the surface of the PV Array.

        Args :
        sun_azimuth
        sun_zenith

        Return :

        """

        c_zenith_cos = math.cos(sun_zenith) * math.cos(self.surface_tilt)
        c_zenith_sin = math.sin(sun_senith) * math.sin(self.surface_tilt)
        c_azimuth = math.cos(sun_azimuth - self.surface_azimuth)
        AOI = math.acos(c_zenith_cos + c_zenith_sin * c_azimuth)

        # TODO :  check outputs, All math trig functions return radians ! transform accordingly
        pass
