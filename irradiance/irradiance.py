"""
The main classes to create and transform the irradiance components
falling into a photovoltaic system, represented by a location and a 
surface.
"""
# Created by Sergio Badillo. 2020

import pandas as pd
import numpy as np
import time
import requests

from spa_sb import solar_position_vect
from requests.exceptions import HTTPError


class PVSystem:
    """The class represents a pv system array and its general attributes.

    Parameters
    ----------
    name : string
        Name or ID to identify the system
    latitude, longitude : float
        Decimal coordinates of system's location.
    elevation : float
        Distance aboves sea level, defaults to 0.
    surface_azimuth : float
        Orientation of the surface in respect to north.
        Azimuth angle convention is defined as degrees east of north
        (e.g. North = 0, East = 90, West = 270).
        A surface facing south has an array azimuth of 180 deg.
    surface_tilt : float
        Surface tilt is defined as the angle from horizontal.
    """

    def __init__(
        self,
        name,
        latitude,
        longitude,
        surface_azimuth,
        surface_tilt,
        elevation=0,
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
    """Represents the irradiance profiles and includes the conversion
    methods in order to obtain the Plane-of-Array (POA) Irradiance.
    Irradiance reauires a PVSystem objects to be passed, along with a
    times DateTimeIndex (assumed UTC) object to specify the simulation period.
    """

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

        # if index (times) is not closed to left then drop last value.

        if len(times) == 8761:
            times = times[:8760]

        self.times = times
        self.lat = pvsystem.lat
        self.lon = pvsystem.lon
        self.elev = pvsystem.elev
        self.surface_azimuth = pvsystem.surface_azimuth
        self.surface_tilt = pvsystem.surface_tilt
        self.pvsystem = pvsystem

        self.solar_pos = None
        self.aoi = None
        self.tmy = None

    def read_TMY_file():
        """ "read the standard components GHI, DNI, DHI."""
        # work in progress

    def get_TMY_file(self):
        """Uses PVGIS webservice to create a Typical Meteorological Year (TMY)
         file using the PVSystem coordinates.

        more about TMY files
        https://ec.europa.eu/jrc/en/PVGIS/tools/tmy

        Return
        ------
        A dataframe instance consisting of 1 year (or several years) of hourly
        data,  with the following columns:

            "time_pvgis" : UTC for normal CSV, local timezone time
            "GHI" : Global horizontal irradiance G(h) in [W/m2].
            "DNI" : Direct (beam) irradiance Gb(n) in [W/m2].
            "DHI" : Diffuse horizontal irradiance Gd(h) in [W/m2].
        """

        url = "https://re.jrc.ec.europa.eu/api/tmy"

        params = {
            "lat": self.lat,
            "lon": self.lon,
            "startyear": 2006,
            "endyear": 2015,
            "outputformat": "json",  # csv, json, epw
        }

        start = time.time()

        try:
            r = requests.get(url, params=params)

            # If the respons was successful, no Exception will be raised
            r.raise_for_status()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")

        except Exception as err:
            print(f"Other error occurred: {err}")

        else:
            print("get_TMY_file: done in {:.2f} seconds.".format(time.time() - start))

            tmy_json = r.json()
            df_r = pd.DataFrame.from_dict(data=tmy_json["outputs"]["tmy_hourly"])
            df_tmy = df_r[["time(UTC)", "G(h)", "Gb(n)", "Gd(h)"]].copy()
            df_tmy.set_index(self.times, inplace=True)
            df_tmy.columns = ["time_pvgis", "GHI", "DNI", "DHI"]
            self.tmy = df_tmy

            return df_tmy

    def get_solar_pos_v(self):
        """
        Calculate the position of the sun relative to an observer on
         the surface of the Earth.
         spa_sb.solar_position_vect() is an implementation of the
         Astronomical Applications Department of the US Naval Observatory method.

        Returns
        -------
        Time-indexed dataframe consisting of columns :
        - Zenith Angle : measured from observer's zenith (observers plane normal).
        - Azimuth Angle : measured in relation to North.
        - Solar Elevation Angle : measured up from the horizon (90deg - Zenith Angle).

        """

        start = time.time()
        print("calculating sun positions")
        self.solar_pos = solar_position_vect(self.times, self.lat, self.lon)
        print("get_solar_pos_v : done in", time.time() - start)

        return self.solar_pos

    def get_aoi(self):
        """Calculates the Angle of Incidence (AOI) between
        the Sun's rays and the surface of the PV Array.

        Returns
        -------
        Time-indexed dataframe consisting of columns :
        - AOI : angle of incidence between the sun's rays and the PV Surface.
                in degrees.

        """

        df_aoi = pd.DataFrame(index=self.solar_pos.index, columns=["aoi"])

        theta_A = np.radians(self.solar_pos["solar_azimuth"])  # azimuth
        theta_Z = np.radians(self.solar_pos["solar_zenith"])  # zenith
        theta_T = np.radians(self.surface_tilt)  # surface tilt
        theta_A_array = np.radians(self.surface_azimuth)  # surface azimuth

        c_zenith_cos = np.cos(theta_Z) * np.cos(theta_T)
        c_zenith_sin = (
            np.sin(theta_Z) * np.sin(theta_T) * np.cos(theta_A - theta_A_array)
        )

        df_aoi["aoi"] = np.degrees(np.arccos(c_zenith_cos + c_zenith_sin))
        self.aoi = df_aoi

        return df_aoi

    def get_poa_irradiance(self):
        """Calculates plane-of-array irradiance and its components.

        Return
        ------
        Time-indexed dataframe consisting of columns :
            "POA" : Total Plane of array irradiance.
            "E_b_poa" : Beam component of poa irradiance.
            "E_g_poa" : Ground reflected component of poa irradiance.
            "E_d_poa" : Diffue component of poa irradiance.


        """

        df_poa = pd.DataFrame(
            index=self.times, columns=["POA", "E_b_poa", "E_g_poa", "E_d_poa"]
        )

        # The plane of array (POA) beam component of irradiance is calculated
        # by adjusting the direct normal irradiance by the angle of incidence.

        aoi = self.aoi["aoi"]
        ghi = self.tmy["GHI"]
        dni = self.tmy["DNI"]
        dhi = self.tmy["DHI"]
        albedo = 0.16  # Urban environement is 0.14 - 0.22

        # POA Beam component
        df_poa["E_b_poa"] = dni * np.cos(np.radians(aoi))

        # POA Ground component
        df_poa["E_g_poa"] = (
            ghi * albedo * ((1 - np.cos(np.radians(self.surface_tilt))) / 2)
        )

        # POA Sky Diffuse component
        E_d_iso = dhi * ((1 + np.cos(np.radians(self.surface_tilt))) / 2)
        E_d_correction = ghi * (
            (
                0.012
                * self.solar_pos["solar_zenith"]
                * (1 - np.cos(np.radians(self.surface_tilt)))
            )
            / 2
        )

        df_poa["E_d_poa"] = E_d_iso + E_d_correction

        # Total POA Irradiance

        # remove negative values
        df_poa = df_poa.where(df_poa > 0, other=0)
        df_poa["POA"] = df_poa["E_b_poa"] + df_poa["E_g_poa"] + df_poa["E_d_poa"]

        return df_poa
