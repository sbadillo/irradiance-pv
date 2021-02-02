"""
Calculate the solar position using
Astronomical Applications Department of the US Naval Observatory

The approximations presented are accurate within arcminutes for 200
centuries of the year 2000. 

Astronomical Applications Department of the U.S. Naval Observatory, (2015),
reproduced from The Astronomical Almanac Online and produced by the U.S.
Naval Observatory and H.M. Nautical Almanac Office.
http://aa.usno.navy.mil/faq/docs/SunApprox.php.
"""

# Created by Sergio Badillo. 2020

import math
import datetime

import numpy as np
import pandas as pd

# todo : get rid of test here
# test datapoint
lat = 52.010000
lon = 4.360000

time_lst = pd.to_datetime("14/04/2014 11:00:00")  # Local Standard time
tz = "Etc/GMT+2"
time = time_lst.tz_localize(tz)
# time_unix = to_unixtime(time)
print(time)

# fastforward - pandas one liner
# print(naive_times.to_julian_date())


def to_unixtime(time):
    """Transforms a pandas datetime index into unix time"""

    if not isinstance(time, pd.DatetimeIndex):
        try:
            time = pd.DatetimeIndex(time)
        except (TypeError, ValueError):
            time = pd.DatetimeIndex(
                [
                    time,
                ]
            )

    return np.array(time.astype(np.int64) / 10 ** 9)


def julian_date(unixtime):
    """Calculates the julian day. It is much faster to calculate
    from unix/epoch time.

    Args:
      Unixtime : Number of seconds since January 1, 1970.
    Return :
      Julian Day: Count of days since the beginning of the Julian period.
    """
    return unixtime * 1.0 / 86400 + 2440587.5


def d_time(julian_day):
    """
    Calculates time elapsed since 2000 noon UTC
    """
    J2000 = 2451545  # Refering to the instant of 12 noon on January 1, 2000
    d_time = julian_day - J2000
    print("d_time", d_time)

    return d_time


def sun_mean_lon(d_time):
    """Calculates Mean longitude of the sun corrected to the aberration of the light
    Output is normalized to [0,360)
    """

    sun_mean_lon = 280.459 + 0.98564736 * d_time
    sun_mean_lon = sun_mean_lon % 360

    return sun_mean_lon % 360


def sun_mean_anomaly(d_time):
    """Correcting to the elliptic orbit of the sun and
    the varying speed throughout the year.
    Output is normalized to [0,360).
    """

    sun_mean_anomaly = 357.529 + 0.98560028 * d_time

    return sun_mean_anomaly % 360


def sun_ecliptic_lon(sun_mean_anomaly, sun_mean_lon):
    """Ecliptic longitude of the Sun in degrees"""

    sun_ecliptic_lon = sun_mean_lon
    +(1.915 * math.sin(math.radians(sun_mean_anomaly)))
    +(0.020 * math.sin(math.radians(2) * math.radians(sun_mean_anomaly)))

    print(sun_ecliptic_lon)

    return sun_ecliptic_lon


# ecliptic latitude of the Sun
# sun_ecliptic_lat = 0


def earth_axial_tilt(d_time):
    """Calculates earth axial tilt in degrees.

    Args:
      d_time : time elapsed since Greenwich noon, terrestrial time,
      on january 2000, in days.
    """

    return 23.429 - 0.00000036 * D_time


def LMST(d_time, lon):
    """Calculates Local Mean Sideral Time (LMST) based on D_time

    Args:
      d_time : time elapsed since Greenwich noon, terrestrial time,
      on january 2000, in days.
      lon : longitude of the observer

    Return:
      Local mean sideral time in degrees
    """

    # Julian Ephemeris Century (JCE), the number of centuries past since
    # Greenwich noorm terrestrial time, on january 2000.
    JCE_time = D_time / 36525

    # Greenwich mean sideral time (GMST) in hours
    # and normalised to [0h to 24h)
    GMST = 18.697374558 + (24.06570982441908 * d_time) + (0.000026 * (JCE_time ** 2))
    GMST = GMST % 24

    # Local Mean sideral time
    LMST = GMST * 15 + lon

    print("LMST", LMST)

    return LMST


def sun_altitude():

    pass


D_time = 5216.875  # force for test, fix later

# calculate solar position

# zeta ζ
# nu ν
# xi ξ

sun_ecliptic_lon = math.radians(sun_ecliptic_lon)
earth_axial_tilt = math.radians(earth_axial_tilt)
lat = math.radians(lat)
LMST = math.radians(LMST)

# # Azimuth
nu = -(math.sin(LMST) * math.cos(sun_ecliptic_lon)) + (
    math.cos(LMST) * math.cos(earth_axial_tilt) * math.sin(sun_ecliptic_lon)
)

xi = -(math.sin(lat) * math.cos(LMST) * math.cos(sun_ecliptic_lon)) - (
    (math.sin(lat) * math.sin(LMST) * math.cos(earth_axial_tilt))
    - (math.cos(lat) * math.sin(earth_axial_tilt))
) * math.sin(sun_ecliptic_lon)

print("nu", nu, "xi", xi)
print("tanAs", nu / xi)
print("##Azimuth")
if xi < 0:
    print(math.degrees(math.atan(nu / xi)) + 180)
elif (xi > 0) & (nu < 0):
    print(math.degrees(math.atan(nu / xi)) + 360)
else:
    print(math.degrees(math.atan(nu / xi)))


# solar_azimuth = math.degrees(math.atan(nu/xi))
# print('solar_azimuth', solar_azimuth)

# Altitude
zeta = math.cos(lat) * math.cos(LMST) * math.cos(sun_ecliptic_lon) + (
    math.cos(lat) * math.sin(LMST) * math.cos(earth_axial_tilt)
    + math.sin(lat) * math.sin(earth_axial_tilt)
) * math.sin(sun_ecliptic_lon)

print("## Altitude")
print("sinas", zeta)
solar_altitude = math.degrees(math.asin(zeta))
print("solar_altitude", solar_altitude)
