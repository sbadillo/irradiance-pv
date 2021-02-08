import pandas as pd
import numpy as np
from spa_delft import solar_position, solar_position_vectorized
import time
import requests
from requests.exceptions import HTTPError


class PVSystem:
    """The class represents a pv system array and its general attributes.

    Args :
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
        name,
        latitude,
        longitude,
        elevation=0,
        surface_azimuth=180,
        surface_tilt=0,
    ):

        self.name = name
        self.lat = latitude
        self.lon = longitude
        self.elev = elevation
        self.surface_azimuth = surface_azimuth
        self.surface_tilt = surface_tilt

    def __repr__(self):

        attrs = [
            self.name,
            self.lat,
            self.lon,
            self.surface_azimuth,
            self.surface_tilt,
        ]
        return "PV System '{}' at Lat {} Lon {}. Array azimuth: {} tilt: {}".format(
            *attrs
        )


class Irradiance:
    """The irradiance Class represents the irradiance profiles and some
    of their conversion methods in order to obtain the POA Irradiance"""

    def __init__(
        self,
        pvsystem,
        times,
    ):
        # check if times arrays is datetimeindex
        if not isinstance(times, pd.DatetimeIndex):
            print("warning times is not datetime, ")
            try:
                times = pd.DatetimeIndex(times)
            except (TypeError, ValueError):
                times = pd.DatetimeIndex(
                    [
                        times,
                    ]
                )

        # if localized, convert to UTC. otherwise, assume UTC.
        try:
            print(times[0])
            times = times.tz_convert("UTC")
            print(times[0])
        except TypeError:
            times = times

        self.times = times
        self.lat = pvsystem.lat
        self.lon = pvsystem.lon
        self.elev = pvsystem.elev
        self.surface_azimuth = pvsystem.surface_azimuth
        self.surface_tilt = pvsystem.surface_tilt

        self.solar_pos = None
        self.aoi = None

    def read_TMY_file():
        """ "read the standard components GHI, DNI, DHI."""

    def get_TMY_file(self):
        """uses pvgis webservice to create a Typical Meteorological Year file
        for the location.

        Returns :
        - json object

        read more about TMY files
        https://ec.europa.eu/jrc/en/PVGIS/tools/tmy
        """

        url = "https://re.jrc.ec.europa.eu/api/tmy"
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "startyear": 2005,
            "endyear": 2015,
            "outputformat": "json",  # csv, json, epw
        }

        start = time.time()

        try:
            r = requests.get(url, params=params)

            # If the respons was successful, no Exception will be raised
            r.raise_for_status()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6
        except Exception as err:
            print(f"Other error occurred: {err}")  # Python 3.6
        else:
            print("get_TMY_file: succes")
            print("done in {:.2f} seconds.".format(time.time() - start))

            return r.json()

    def get_solar_pos_v(self):
        """
        Calculates the position of the sun relative to an observer on the surface of the Earth.
        The convention used to describe solar positions includes the parameters :
        - Zenith Angle : measured from observer's zenith (observers plane normal).
        - Azimuth Angle : measured in relation to North.
        - Solar Elevation Angle : measured up from the horizon and equal to 90deg - Zenith Angle.

        """

        start = time.time()
        print("calculating sun positions")
        self.solar_pos = solar_position_vectorized(self.times, self.lat, self.lon)
        print(self.solar_pos)
        print("done in", time.time() - start)

    def get_aoi(self):
        """Calculates the angle of incidence between
        the Sun's rays and the surface of the PV Array.

        Args :
        sun_azimuth
        sun_zenith

        Return :

        """

        sun_zenith = np.radians(self.solar_pos["solar_zenith"])
        sun_azimuth = np.radians(self.solar_pos["solar_azimuth"])
        surface_tilt = np.radians(self.surface_tilt)
        surface_azimuth = np.radians(self.surface_azimuth)

        c_zenith_cos = np.cos(sun_zenith) * np.cos(surface_tilt)
        c_zenith_sin = np.sin(sun_zenith) * np.sin(surface_tilt)
        c_azimuth = np.cos(sun_azimuth - surface_azimuth)

        self.aoi = np.degrees(np.arccos(c_zenith_cos + c_zenith_sin * c_azimuth))
        print(self.aoi)

        # ! alert, output is not accurate, rewrite formula above or check conventions 👆
        # TODO :  check outputs, All math trig functions return radians ! transform accordingly
        pass

    def get_poa_irradiance():
        """Calculates plane-of-array irradiance"""

        E_poa_beam = None  # depends on AOI
        E_poa_ground = None  # depends on Albedo coefficient
        E_poa_diffuse = None  # depends on surface tilt, and sun zenith https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/plane-of-array-poa-irradiance/calculating-poa-irradiance/poa-sky-diffuse/simple-sandia-sky-diffuse-model/

        E_poa = E_poa_beam + E_poa_ground + E_poa_diffuse

        return E_poa


# Albedo coeff.
# Albedo is the fraction of the Global Horizontal Irradiance that is reflected.
# The PVsyst modeling software provides the following guidance for estimating an appropriate value for albedo:

# Urban environment 0.14 – 0.22
# Grass 0.15 – 0.25 / Fresh grass 0.26
# Fresh snow 0.82
# Wet snow 0.55-0.75
# Dry asphalt 0.09-0.15
# Wet Asphalt 0.18
# Concrete 0.25-0.35
# Red tiles 0.33
# Aluminum 0.85
# Copper 0.74
# New galvanized steel 0.35
# Very dirty galvanized steel 0.08