import numpy as np
import pandas as pd


def density_at_altitude(h):
    if h < 0:
        return 0
    elif h <= 11000:
        return 1.225*(1-0.0065*h/288.15)**4.256
    elif h <=20000:
        return 0.3672*np.exp(-1*(h-11000)/6341.62)
    elif h <= 32000:
        return 0.0889*(1+0.0010*(h-20000)/216.65)**-35.163

# inputs for program
amount_of_wires = 1
wire_segments = 100  # amount of segments
radius_wire = 1  # mm
total_wire_length = 20000  # meters

density_of_materials = [0.8, 0.9, 1, 1.1, 1.2]  # kg/L
density_of_material = density_of_materials[1]

# side-quest calculations
area_of_segment = np.pi * radius_wire ** 2  # mm^2

## set up dataframe for use ##

# mass
length_of_segment = total_wire_length / wire_segments
volume_of_segment = area_of_segment * length_of_segment
mass_of_segment = volume_of_segment * density_of_material
mass_list = mass_of_segment * np.ones(wire_segments)

# wind/gust
wind_profile_list = np.zeros(wire_segments)

# initial tension
initial_tension_list = np.zeros(wire_segments)

# orientation
angle_of_orientation_list = np.zeros(wire_segments)

# positioning
top_position_list = (np.ones(wire_segments), np.ones(wire_segments))  # tuple -> x,y
bottom_position_list = (np.ones(wire_segments), np.ones(wire_segments))  # tuple -> x,y
