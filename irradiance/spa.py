
# import os
# import threading
# import warnings
import pandas as pd
import numpy as np



naive_times = pd.date_range(start='2015', end='2016', freq='1h')
unixtimes = np.array(naive_times.astype(np.int64)/10**9)

def julian_date(unixtime):
    jd = unixtime * 1.0 / 86400 + 2440587.5
    return jd


def to_unixtime(time):
    """Transforms a pandas datetime index into unix time"""
    
    if not isinstance(time, pd.DatetimeIndex):
        try:
            time = pd.DatetimeIndex(time)
        except (TypeError, ValueError):
            time = pd.DatetimeIndex([time, ])
    return np.array(time.astype(np.int64)/10**9)

# test October 17, 2003
time_lst = pd.to_datetime("17/10/2003 12:30:30")    # Local Standard Time
timezone = 'MST'                                      # Mountain standard time GMT-7h
time1 = to_unixtime(time_lst.tz_localize('MST'))

print(julian_date(time1))


# fastforward - pandas one liner
# print(naive_times.to_julian_date())

