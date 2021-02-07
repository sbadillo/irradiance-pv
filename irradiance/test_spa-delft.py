### Run pytest in terminal to test_d_time

import pytest

from .spa_delft import julian_date
from .spa_delft import d_time_bis
from .spa_delft import d_time
from .spa_delft import sun_mean_anomaly
from .spa_delft import sun_mean_lon
from .spa_delft import sun_ecliptic_lon
from .spa_delft import lmst
from .spa_delft import sun_altitude
from .spa_delft import sun_zenith

from .spa_delft import solar_position


import pandas as pd


# Delft test data, a localised pd datetime index ...
time_lst = pd.to_datetime("14/04/2014 11:00:00")  # Local Standard time
tz = "Etc/GMT+0"
time = time_lst.tz_localize(tz)
lat = 52.010000
lon = 4.360000

# time = pd.to_datetime("19/06/1987 12:00:00")
# # tz = "Etc/GMT+7"
# # time = time.tz_localize(tz)
# lat = 39.742476
# lon = -105.1786


def test_d_time_bis():
    assert d_time_bis(time) == 5216.875
    D = d_time_bis(time)


def test_d_time():
    D = d_time(julian_date(time))
    # assert pytest.approx(D, 0.001) == time.to_julian_date() - 2451545
    assert D == 5216.875


def test_sun_ecliptic_lon():
    D = 5216.875

    a = sun_mean_lon(D)
    b = sun_mean_anomaly(D)
    assert sun_ecliptic_lon(a, b) == pytest.approx(24.34162696, 0.00001)


def test_lmst():
    D = 5216.875
    lon = 4.36
    assert lmst(D, lon) == pytest.approx(341.8197304, 0.00001)


def test_sun_altitude():
    lat = 52.01
    lmst = 341.8197303
    sun_ecliptic_lon = 24.34162696
    epsilon = 23.42712193
    assert sun_altitude(lat, lmst, sun_ecliptic_lon, epsilon) == pytest.approx(
        36.1, 0.01
    )


def test_sun_zenith():
    lat = 52.01
    lmst = 341.8197303
    sun_ecliptic_lon = 24.34162696
    epsilon = 23.42712193
    assert sun_zenith(lat, lmst, sun_ecliptic_lon, epsilon) == pytest.approx(
        127.2, 0.01
    )


def test_solar_position():

    print(time, lat, lon)

    r = solar_position(time, lat, lon)

    assert r[0] == 36.1
    assert r[1] == 127.2
