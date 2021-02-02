### Run pytest in terminal to test_d_time

from .spa_delft import julian_date
from .spa_delft import d_time

import pandas as pd

lat = 52.010000
lon = 4.360000

# D_time = 5216.875  # force for test, fix later

time_lst = pd.to_datetime("14/04/2014 11:00:00")  # Local Standard time
tz = "Etc/GMT+2"
time = time_lst.tz_localize(tz)


def test_d_time():
    assert d_time(julian_date(time)) == time.to_julian_date() - 2451545
