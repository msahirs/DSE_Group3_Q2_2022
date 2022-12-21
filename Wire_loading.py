import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ISA_general import ISA, ISA_from_everything

"""numbering of elements is increasing from earth to balloon"""


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
wire_drag_coeff = 0.5

density_of_materials = [0.8, 0.9, 1, 1.1, 1.2]  # kg/L
density_of_material = density_of_materials[1]

# side-quest calculations
area_of_segment = np.pi * radius_wire ** 2  # mm^2


def buoyancy_force(balloon_altitude):
    return (density_at_altitude(balloon_altitude) - density_internal_balloon) * volume_balloon


def drag_balloon_force():
    return q_balloon * s_balloon * drag_coeff


def lift_balloon_force():
    return q_balloon * s_balloon * lift_coeff


class balloon():
    def __init__(self, speed, altitude, volume_balloon, weight):
        self.drag_coeff = 0.53
        self.lift_coeff = 0.1
        self.s_balloon = 50
        self.volume = volume_balloon
        self.altitude = altitude
        self.speed = speed
        self.weight = weight
        self.q_balloon = 0.5 * density_at_altitude(altitude) * speed * speed

        # self.buoyancy_force = (density_at_altitude(balloon_altitude)-density_internal_balloon)*volume_balloon
        # self.drag_force


class tether():
    def __init__(self):
        self.length = total_wire_length / wire_segments
        self.nodes = dict()  # position, angle, etc...
        self.material = dict()  # density, E-mod, tensile strength, etc...
        self.radius = radius_wire
        self.drag_coeff = wire_drag_coeff


class atmosphere():
    """h = list of altitudes"""

    def __init__(self, h):
        self.ISA = self.ISA(h)
        self.wind = self.wind(h)

    class ISA():
        def __init__(self, h):
            ISA_properties = ISA_from_everything((h))
            self.temp = ISA_properties[0]
            self.pressure = ISA_properties[1]
            self.density = ISA_properties[2]

    class wind():
        def __init__(self, angle):
            self.angle = angle


def calc_force_matrix():
    """
    input:
    mass =
    drag =
    lift_gas =
    lift_wind =

    :return:
    """


def create_mesh(nodes, altitude_balloon=20000, altitude_ground=0):
    """
    create mesh for the wire
    [[xlist], [ylist]
    """
    y_list = np.linspace(altitude_ground, altitude_balloon, nodes)  # using bottem as well
    x_list = np.zeros(y_list.shape)
    coords = np.array([x_list, y_list])
    return coords

print(create_mesh(3))



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
