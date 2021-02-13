"""
Calculate the solar position using the
Astronomical Applications Department of the US Naval Observatory method.

The approximations presented are accurate within arcminutes for 200
centuries of the year 2000. 

Astronomical Applications Department of the U.S. Naval Observatory, (2015),
reproduced from The Astronomical Almanac Online and produced by the U.S.
Naval Observatory and H.M. Nautical Almanac Office.
http://aa.usno.navy.mil/faq/docs/SunApprox.php.
"""

# Created by Sergio Badillo. 2020

import math

import numpy as np
import pandas as pd

# TDB Julian date of epoch J2000.0
EPOCHS_JULIAN_DATE = 2451545

SUNS_MEAN_LONGITUDE_AT_EPOCH = 280.459
SUNS_MEAN_LONGITUDE_AT_EPOCH = 280.459
SUNS_MEAN_ANOMALY_AT_EPOCH = 357.5291
EARTHS_MEAN_ANGULAR_ROTATION = 0.98560028
EARTHS_ECLIPTIC_OBLIQUITY_CHANGE_RATE = 0.00000036
EARTHS_ECLIPTIC_MEAN_OBLIQUITY = 23.429


def julian_date(time):
    """Calculates the julian day. Time must be passed and a DateTimeIndex
    object and asumed to be UTC.

    Args:
      time : Number of seconds since January 1, 1970.
    Return :
      Julian Day: Count of days since the beginning of the Julian period.
    """

    unixtime = np.array(time.astype(np.int64) / 10 ** 9)

    # jd = time.to_julian_date()[0]
    # return jd

    return unixtime * 1.0 / 86400 + 2440587.5


def d_time(julian_day):
    """
    Calculates time elapsed since 2000 noon UTC
    """
    d = julian_day - EPOCHS_JULIAN_DATE

    return d


def d_time_bis(time):
    # time is datetimeobject

    # if localized, convert to UTC. otherwise, assume UTC.
    try:
        time_utc = time.tz_convert("UTC")
    except TypeError:
        time_utc = time

    unixtime = time.timestamp()

    jd = unixtime * 1.0 / 86400 + 2440587.5

    d = jd - EPOCHS_JULIAN_DATE

    return d


def sun_mean_lon(d_time):
    """Calculates Mean longitude of the sun corrected to the aberration of the light
    Output is normalized to [0,360)
    """

    sun_mean_lon = SUNS_MEAN_LONGITUDE_AT_EPOCH + 0.98564736 * d_time
    sun_mean_lon = sun_mean_lon

    return sun_mean_lon % 360


def sun_mean_anomaly(d_time):
    """Correcting to the elliptic orbit of the sun and
    the varying speed throughout the year.
    Output is normalized to [0,360).

    d_time : time elapsed since Greenwich noon, terrestrial time,

    """

    sun_mean_anomaly = (
        SUNS_MEAN_ANOMALY_AT_EPOCH + EARTHS_MEAN_ANGULAR_ROTATION * d_time
    )

    return sun_mean_anomaly % 360


def sun_ecliptic_lon(sun_mean_lon, sun_mean_anomaly):
    """Calculates the geocentric apparent ecliptic longitude of the sun
    (adjusted for aberration).
    """

    sun_ecliptic_lon = (
        sun_mean_lon
        + 1.915 * math.sin(math.radians(sun_mean_anomaly))
        + 0.020 * math.sin(2 * math.radians(sun_mean_anomaly))
    )
    # print(type(sun_ecliptic_lon))
    return sun_ecliptic_lon


# ecliptic latitude of the Sun
# sun_ecliptic_lat = 0

# # The distance of the Sun from the Earth, R, in astronomical units (AU)
# R = 1.00014-0.01671*COS( sun_mean_anomaly )-0.00014*COS( 2.0* sun_mean_anomaly );


def earth_axial_tilt(d_time):
    """Calculates earth axial tilt in degrees.

    Args:
    d_time : Days elapsed since Greenwich noon, terrestrial time, on january 2000.
    """

    earth_axial_tilt = (
        EARTHS_ECLIPTIC_MEAN_OBLIQUITY - EARTHS_ECLIPTIC_OBLIQUITY_CHANGE_RATE * d_time
    )
    return earth_axial_tilt


def lmst(d_time, lon):
    """Calculates Local Mean Sideral Time (lmst) based on D_time

    Args:
      d_time : time elapsed since Greenwich noon, terrestrial time,
      on january 2000, in days.
      lon : longitude of the observer

    Return:
      Local mean sideral time in degrees
    """

    # Julian Ephemeris Century (JCE), the number of centuries past since
    # Greenwich noorm terrestrial time, on january 2000.
    JCE_time = d_time / 36525

    # Greenwich mean sideral time (gmst) in hours
    # and normalised to [0h to 24h)
    gmst = 18.697374558 + (24.06570982441908 * d_time) + (0.000026 * (JCE_time ** 2))
    gmst = gmst % 24
    lmst = (gmst * 15) + lon

    return lmst


def sun_altitude(lat, lmst, sun_ecliptic_lon, earth_axial_tilt):
    """Calculates the Solar Altitude in degrees."""

    # Convert inputs to radians
    sun_ecliptic_lon = math.radians(sun_ecliptic_lon)
    earth_axial_tilt = math.radians(earth_axial_tilt)
    lat = math.radians(lat)
    lmst = math.radians(lmst)

    # Altitude components zeta (ζ)

    zeta = math.cos(lat) * math.cos(lmst) * math.cos(sun_ecliptic_lon) + (
        math.cos(lat) * math.sin(lmst) * math.cos(earth_axial_tilt)
        + math.sin(lat) * math.sin(earth_axial_tilt)
    ) * math.sin(sun_ecliptic_lon)

    solar_altitude = math.degrees(math.asin(zeta))

    return solar_altitude


def sun_zenith(lat, lmst, sun_ecliptic_lon, earth_axial_tilt):
    """Calculates the Solar Zenith in degrees."""

    # Convert inputs to radians
    sun_ecliptic_lon = math.radians(sun_ecliptic_lon)
    earth_axial_tilt = math.radians(earth_axial_tilt)
    lat = math.radians(lat)
    lmst = math.radians(lmst)

    # Azimuth components # nu (ν) and xi (ξ)
    nu = -1 * (math.sin(lmst) * math.cos(sun_ecliptic_lon)) + (
        math.cos(lmst) * math.cos(earth_axial_tilt) * math.sin(sun_ecliptic_lon)
    )

    xi = -1 * (math.sin(lat) * math.cos(lmst) * math.cos(sun_ecliptic_lon)) - (
        (math.sin(lat) * math.sin(lmst) * math.cos(earth_axial_tilt))
        - (math.cos(lat) * math.sin(earth_axial_tilt))
    ) * math.sin(sun_ecliptic_lon)

    if xi < 0:
        solar_azimuth = math.degrees(math.atan(nu / xi)) + 180
    elif (xi > 0) & (nu < 0):
        solar_azimuth = math.degrees(math.atan(nu / xi)) + 360
    else:
        solar_azimuth = math.degrees(math.atan(nu / xi))

    return solar_azimuth


def solar_position(time, lat, lon):
    """Calculate the solar position using the
    Astronomical Applications Department of the US Naval Observatory method.

    Args :

    Returns :
    Array with elements
        elevation
        azimuth
    """

    D = d_time(julian_date(time))
    q = sun_mean_lon(D)
    g = sun_mean_anomaly(D)
    # print(D)
    # print("q, g", q, g)

    lambda_s = sun_ecliptic_lon(q, g)
    # print("lambda_s", lambda_s)
    epsilon = earth_axial_tilt(D)
    # print("epsilon", epsilon)
    theta_L = lmst(D, lon)
    # print("theta_L", theta_L)

    altitude = sun_altitude(lat, theta_L, lambda_s, epsilon)
    azimuth = sun_zenith(lat, theta_L, lambda_s, epsilon)

    return [altitude, azimuth]


def solar_position_vect(times, lat, lon):
    """
    Calculate the solar position using the Astronomical Applications
    Department of the US Naval Observatory method.
    This vectorized approach is 10x faster compared to the original
    solar_positions function.

    Args
    ----
    times : A DateTimeIndex object assumed to be in UTC.

    Returns
    -------
    A dataframe object indexed to times with the columns :
        solar_altitude
        solar_azimuth
        solar_zenith
    """

    df = pd.DataFrame(index=times)

    df["D"] = df.index.to_julian_date() - EPOCHS_JULIAN_DATE
    df["sun_mean_lon"] = (SUNS_MEAN_LONGITUDE_AT_EPOCH + 0.98564736 * df["D"]) % 360
    df["sun_mean_ano"] = (
        SUNS_MEAN_ANOMALY_AT_EPOCH + EARTHS_MEAN_ANGULAR_ROTATION * df["D"]
    ) % 360

    df["sun_ecliptic_lon"] = (
        df["sun_mean_lon"]
        + 1.915 * np.sin(np.radians(df["sun_mean_ano"]))
        + 0.020 * np.sin(2 * np.radians(df["sun_mean_ano"]))
    )

    df["earth_axial_tilt"] = (
        EARTHS_ECLIPTIC_MEAN_OBLIQUITY - EARTHS_ECLIPTIC_OBLIQUITY_CHANGE_RATE * df["D"]
    )

    df["gmst"] = (
        18.697374558
        + (24.06570982441908 * df["D"])
        + (0.000026 * ((df["D"] / 36525) ** 2))
    ) % 24

    df["lmst"] = (df["gmst"] * 15) + lon

    # Convert inputs to radians (being lazy to avoid enormous formulas here)

    sun_ecliptic_lon = np.radians(df["sun_ecliptic_lon"])
    earth_axial_tilt = np.radians(df["earth_axial_tilt"])
    lat = np.radians(lat)
    lmst = np.radians(df["lmst"])

    # Altitude components zeta (ζ)

    zeta = np.cos(lat) * np.cos(lmst) * np.cos(sun_ecliptic_lon) + (
        np.cos(lat) * np.sin(lmst) * np.cos(earth_axial_tilt)
        + np.sin(lat) * np.sin(earth_axial_tilt)
    ) * np.sin(sun_ecliptic_lon)

    df["solar_altitude"] = np.degrees(np.arcsin(zeta))

    df["solar_zenith"] = 90 - df["solar_altitude"]

    # Azimuth components # nu (ν) and xi (ξ)

    nu = -1 * (np.sin(lmst) * np.cos(sun_ecliptic_lon)) + (
        np.cos(lmst) * np.cos(earth_axial_tilt) * np.sin(sun_ecliptic_lon)
    )

    xi = -1 * (np.sin(lat) * np.cos(lmst) * np.cos(sun_ecliptic_lon)) - (
        (np.sin(lat) * np.sin(lmst) * np.cos(earth_axial_tilt))
        - (np.cos(lat) * np.sin(earth_axial_tilt))
    ) * np.sin(sun_ecliptic_lon)

    df["solar_azimuth"] = np.degrees(np.arctan(nu / xi))
    df["solar_azimuth"] = np.where(
        (xi < 0), df["solar_azimuth"] + 180, df["solar_azimuth"]
    )
    df["solar_azimuth"] = np.where(
        (xi > 0) & (nu < 0), df["solar_azimuth"] + 360, df["solar_azimuth"]
    )

    output_cols = ["solar_altitude", "solar_zenith", "solar_azimuth"]

    return df[output_cols]
