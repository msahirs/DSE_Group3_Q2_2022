
# set up dataframe for use ##

mass
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
