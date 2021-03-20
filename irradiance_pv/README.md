# Irradiance PV

Irradiance is a simple implementation of solar position and irradiance models to calculate the incident in plane irradiance in PV Modules.

The package works its way from an horizontal global irradince, calculating solar positions, then transforming the components into a 
Plane-of-Array (POA) Irradiance, necessary for the modeling of photovoltaic energy yields.


## Installation
'''console
$pip install irradiance-pv
'''

## files

### irradiance.py

Contains the main classes to create and transform the irradiance components falling into a photovoltaic system, represented by a location and a surface.

### spa_sb.py

Contains an implementation of the solar positions algorithm developped by the Astronomical Applications Department of the US Naval Observatory.
