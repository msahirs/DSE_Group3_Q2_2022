import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ISA_general import ISA, ISA_from_everything
from math import *

"""numbering of elements is increasing from earth to balloon"""


def make_material_dict():
    # make dict
    material_dict = dict()

    # add steel
    material_dict["steel"] = dict()
    material_dict["steel"]["e-mod"] = 196 * 10 ** 9
    material_dict["steel"]["density"] = 7.86 * 10 ** 3
    material_dict["steel"]["tensile_ult"] = 860 * 10 ** 6
    material_dict["steel"]["tensile_yield"] = 690 * 10 ** 6

    # add aluminium
    material_dict["allum"] = dict()
    material_dict["allum"]["e-mod"] = 70 * 10 ** 9
    material_dict["allum"]["density"] = 2.8 * 10 ** 3
    material_dict["allum"]["tensile_ult"] = 350 * 10 ** 6
    material_dict["allum"]["tensile_yield"] = 300 * 10 ** 6

    # add Titanium
    material_dict["titan"] = dict()
    material_dict["titan"]["e-mod"] = 110 * 10 ** 9
    material_dict["titan"]["density"] = 4.43 * 10 ** 3
    material_dict["titan"]["tensile_ult"] = 900 * 10 ** 6
    material_dict["titan"]["tensile_yield"] = 830 * 10 ** 6

    # add UHMPE
    material_dict["uhmpe"] = dict()
    material_dict["uhmpe"]["e-mod"] = 700 * 10 ** 9
    material_dict["uhmpe"]["density"] = 0.93 * 10 ** 3
    material_dict["uhmpe"]["tensile_ult"] = 1100 * 10 ** 6
    material_dict["titan"]["tensile_yield"] = 1
    return material_dict


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


def get_trans_matrix(coords1, coords2):
    theta = atan2(coords2[1] - coords1[1], coords2[0] - coords1[0])
    labda = cos(theta)
    mu = sin(theta)
    trans_matrix = np.matrix([[labda, mu, 0, 0], [-mu, labda, 0, 0], [0, 0, labda, mu], [0, 0, -mu, labda]])
    return trans_matrix


def gen_stifness_matrix_element(E, A, L, begin_coords, end_coords):
    """
    :param E: E-mod
    :param A: cross Area
    :param L: length
    :return: global stiffness_matrix element
    """
    transformation_matrix = get_trans_matrix(begin_coords, end_coords)

    stifness_matrix_element = ((E * A) / L) * np.array([[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]])
    global_matrix_element = transformation_matrix.transpose() @ stifness_matrix_element @ transformation_matrix
    return global_matrix_element


def make_global_stiffness_matrix(list_of_matrix_elements):
    """
    make global matrix with one diagonal
    :param list_of_matrix_elements:
    :return:
    """
    length_of_global_matrix = int(0.5 * len(list_of_matrix_elements[0]) * (1 + len(list_of_matrix_elements)))
    global_stiffness_matrix = np.zeros([length_of_global_matrix, length_of_global_matrix])
    for numb, matrix_element in enumerate(list_of_matrix_elements):
        # matrix_element = np.array(matrix_element)
        start_index = numb * len(matrix_element) / 2
        for i in range(len(matrix_element)):
            for j in range(len(matrix_element)):
                global_stiffness_matrix[int(start_index + i), int(start_index + j)] += matrix_element[i, j]
    return global_stiffness_matrix


print(create_mesh(3))

print(gen_stifness_matrix_element(100, 10 ** -2, 1, [0, 0], [np.cos(np.radians(60)), np.sin(np.radians(60))]))
print(gen_stifness_matrix_element(100, 10 ** -2, 1, [0, 0], [1, 1]))
array = np.array([[[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]]])
print(make_global_stiffness_matrix(array))

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
