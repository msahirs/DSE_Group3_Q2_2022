import numpy as np
import pandas as pd

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
