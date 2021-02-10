from pvsystem import PVSystem
from pvsystem import Irradiance
import pandas as pd
import time
import pytz

naive_times = pd.date_range(start="2015", end="2016", freq="1h", closed="left")

print(naive_times)

# utc_times = localized_times.tz_convert(tz=None)

# Instanciate a PV System
pv_Sonora = PVSystem(
    name="Sonora", latitude=30, longitude=-110, surface_azimuth=180, surface_tilt=0
)
print("created", pv_Sonora)


irradiance = Irradiance(times=naive_times, pvsystem=pv_Sonora)

# start calculations
startMaster = time.time()

tmy = irradiance.get_TMY_file()
irradiance.get_solar_pos_v()
aoi = irradiance.get_aoi()
poa = irradiance.get_poa_irradiance()

df = pd.concat([tmy, poa], axis=1)
df.name = irradiance.pvsystem.name

index_ = df.index.tz_localize(tz="MST")
df.index = index_

# Create the index

local_time = pytz.timezone("MST")
local_datetime = local_time.localize(naive_times, is_dst=None)
utc_datetime = local_datetime.astimezone(pytz.utc)

df.index = utc_datetime


print(df)
print("DONE in ", time.time() - startMaster)


# # Get irradiance data for summer and winter solstice, assuming 25 degree tilt
# # and a south facing array
# summer_irradiance =
# winter_irradiance =


# # Plot GHI vs. POA for winter and summer
# fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
# summer_irradiance["GHI"].plot(ax=ax1, label="GHI")
# summer_irradiance["POA"].plot(ax=ax1, label="POA")
# winter_irradiance["GHI"].plot(ax=ax2, label="GHI")
# winter_irradiance["POA"].plot(ax=ax2, label="POA")
# ax1.set_xlabel("Time of day (Summer)")
# ax2.set_xlabel("Time of day (Winter)")
# ax1.set_ylabel("Irradiance ($W/m^2$)")
# ax1.legend()
# ax2.legend()
# plt.show()