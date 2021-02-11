from pvsystem import PVSystem
from pvsystem import Irradiance
import pandas as pd
import time
import matplotlib.pyplot as plt

naive_times = pd.date_range(start="2015", end="2016", freq="1h", closed="left")

print(naive_times)

# utc_times = localized_times.tz_convert(tz=None)

# Instanciate a PV System
pv_Sonora = PVSystem(
    name="Sonora", latitude=30, longitude=-110, surface_azimuth=-90, surface_tilt=40
)
print("created", pv_Sonora)

irradiance = Irradiance(times=naive_times, pvsystem=pv_Sonora)

# start calculations
startMaster = time.time()

tmy = irradiance.get_TMY_file()
pos = irradiance.get_solar_pos_v()
aoi = irradiance.get_aoi()
poa = irradiance.get_poa_irradiance()

# join together to a final dataframe
df = pd.concat([tmy, pos, aoi, poa], axis=1)
df.name = irradiance.pvsystem.name

# localize and convert index to MST
df.index = df.index.tz_localize(tz="UTC")
df.index = df.index.tz_convert(tz="MST")

# export results to file
df.to_csv(r"df_test.csv")

print(df)

print("DONE in ", time.time() - startMaster)

# Get irradiance data for summer and winter solstice, assuming 25 degree tilt
# and a south facing array
summer_irradiance = df["2015-06-30"]
winter_irradiance = df["2015-12-24"]

# Convert Dataframe Indexes to Hour:Minute format to make plotting easier
summer_irradiance.index = summer_irradiance.index.strftime("%H:%M")
winter_irradiance.index = winter_irradiance.index.strftime("%H:%M")


# Plot GHI vs. POA for winter and summer
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
summer_irradiance["GHI"].plot(ax=ax1, label="GHI")
summer_irradiance["POA"].plot(ax=ax1, label="POA")
winter_irradiance["GHI"].plot(ax=ax2, label="GHI")
winter_irradiance["POA"].plot(ax=ax2, label="POA")
ax1.set_xlabel("Time of day (Summer)")
ax2.set_xlabel("Time of day (Winter)")
ax1.set_ylabel("Irradiance ($W/m^2$)")
ax1.legend()
ax2.legend()
plt.show()