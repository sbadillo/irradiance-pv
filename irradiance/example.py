from pvsystem import PVSystem
from pvsystem import Irradiance
import pandas as pd

import pvlib


naive_times = pd.date_range(start="2015", end="2016", freq="1h")
localized_times = naive_times.tz_localize("MST")


# Instanciate a PV System
pv_Sonora = PVSystem(
    name="Sonora", latitude=30, longitude=-110, surface_azimuth=180, surface_tilt=0
)
print("created", pv_Sonora)


irradiance = Irradiance(times=naive_times, pvsystem=pv_Sonora)

# irradiance.get_TMY_file()

irradiance.get_solar_pos_v()
irradiance.get_aoi()


print(aoi)
