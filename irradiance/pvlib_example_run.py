import pvlib
import pandas as pd


naive_times = pd.date_range(start='2015', end='2016', freq='1h')

# Site : Latitude, Longitude, Name
# System : surface azimuth (180 = South)
coordinates = [(30, -110, 'Tucson')]
system = {
    'surface_azimuth': 180, 
    'surface_tilt': 30 
}

for latitude, longitude, name in coordinates:
    times = naive_times
    
    solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
    print(len(times))
    

    aoi = pvlib.irradiance.aoi(system['surface_tilt'], system['surface_azimuth'],
                              solpos['apparent_zenith'], solpos['azimuth'])
    
    print(aoi)
    print(solpos)

    
