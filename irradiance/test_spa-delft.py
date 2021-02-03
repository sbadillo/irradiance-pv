### Run pytest in terminal to test_d_time

import pytest

from .spa_delft import julian_date
from .spa_delft import d_time
from .spa_delft import sun_mean_anomaly
from .spa_delft import sun_mean_lon
from .spa_delft import sun_ecliptic_lon
from .spa_delft import lmst
from .spa_delft import sun_altitude
from .spa_delft import sun_zenith
from .spa_delft import solar_position


import pandas as pd

lat = 52.010000
lon = 4.360000

time_lst = pd.to_datetime("14/04/2014 11:00:00")  # Local Standard time
tz = "Etc/GMT+2"
time = time_lst.tz_localize(tz)

def test_d_time():
    assert d_time(julian_date(time)) == time.to_julian_date() - 2451545

def test_sun_ecliptic_lon():
    D = 5216.875
    a = sun_mean_lon(D)
    b = sun_mean_anomaly(D)
    assert sun_ecliptic_lon(a,b) == pytest.approx(24.34162696, 0.00001)

def test_lmst():
    D = 5216.875
    lon = 4.36
    assert lmst(D, lon) == pytest.approx(341.8197304, 0.00001)

def test_sun_altitude():
    lat = 52.01
    lmst = 341.8197303
    sun_ecliptic_lon = 24.34162696
    epsilon = 23.42712193
    assert sun_altitude(lat, lmst, sun_ecliptic_lon, epsilon) == pytest.approx(36.1, 0.01)

def test_sun_zenith():
    lat = 52.01
    lmst = 341.8197303
    sun_ecliptic_lon = 24.34162696
    epsilon = 23.42712193
    assert sun_zenith(lat, lmst, sun_ecliptic_lon, epsilon) == pytest.approx(127.2, 0.01)

def test_solar_position():
    lat = 52.010000
    lon = 4.360000

    time_lst = pd.to_datetime("14/04/2014 11:00:00")  # Local Standard time
    tz = "Etc/GMT+2"
    time = time_lst.tz_localize(tz)

    r = solar_position(time, lat, lon)
    
    assert r[0] == 36.1
    assert r[1] == 127.2
    

