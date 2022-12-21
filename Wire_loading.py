import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def density_at_altitude(h):
    """
    constraints:
    only between 0 and 32000 meters
    :param h: altitude [m]
    :return: density at given altitude for air [kg/m^3]
    """
    if h < 0:
        return 0
    if h <= 11000:
        return 1.225 * (1 - 0.0065 * h / 288.15) ** 4.256
    if h <= 20000:
        return 0.3672 * np.exp(-1 * (h - 11000) / 6341.62)
    if h <= 32000:
        return 0.0889 * (1 + 0.0010 * (h - 20000) / 216.65) ** -35.163
    else:
        return 0


# inputs for program
design_altitude = 20000
amount_of_wires = 1
wire_segments = 100  # amount of segments
radius_wire = 1  # mm
total_wire_length = design_altitude  # meters
balloon_altitude = design_altitude  # meters
density_internal_balloon = 0.2  # kg/m^3
volume_balloon = 80000  # m^3

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


def boancy_force(balloon_altitude):
    return (density_at_altitude(balloon_altitude)-density_internal_balloon)*volume_balloon

def drag_balloon_force():
    return q_balloon*s_balloon*drag_coeff

def lift_balloon_force():
    return q_balloon*s_balloon*lift_coeff

# class balloon():
#     def __init__(self, speed, altitude):
#         self.q_balloon = speed*speed*0.5*density_at_altitude(altitude)
#         self.boancy_force = density_at_altitude(balloon_altitude)-density_internal_balloon)*volume_balloon

class atmosphere():
    """h = list of altitudes"""
    def __init__(self, h):
        self.ISA = self.ISA(h)
        self.wind = self.wind(h)


    class ISA():
        def __init__(self, h):
            self.temp = get_temp(h)
            self.pressure = get_pressure(self, h)
            self.density = get_density(h)

    def get_pressure(self, h):
        """"
        calc thing """
        pressure = h/10
        return pressure

    class wind():
        def __init__(self, angle):
            self.angle = angle

