import pandas as pd
import pvlib
import time

naive_times = pd.date_range(start="2015", end="2016", freq="1h")

# Site : Latitude, Longitude
# System : surface azimuth (180 = South)

surface_azimuth = 180
surface_tilt = 30

start = time.time()
print("calculating sun positions")

solpos = pvlib.solarposition.get_solarposition(naive_times, latitude=30, longitude=-110)
end = time.time()
print("done in", end - start)

print(solpos)

# print(len(times))

# aoi = pvlib.irradiance.aoi(
#     system["surface_tilt"],
#     system["surface_azimuth"],
#     solpos["apparent_zenith"],
#     solpos["azimuth"],
# )

# print(aoi)
