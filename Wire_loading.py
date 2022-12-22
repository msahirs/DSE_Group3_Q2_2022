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
radius_wire = 0.005  # m
total_wire_length = design_altitude  # meters
balloon_altitude = design_altitude  # meters
density_internal_balloon = 0.2  # kg/m^3
volume_balloon = 80000  # m^3
wire_drag_coeff = 0.5

material_dict = make_material_dict()
g = 9.80665  # m/s^2

# side-quest calculations
area_of_segment = np.pi * radius_wire ** 2  # mm^2


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


def balloon_tension(phi, balloon_altitude, q_b, s_b, C_bl, C_bd, density_hydrogen, volume):

    Balloon=balloon(0,0,0,0) #TODO: placeholder values
    lift_balloon_force=q_b*s_b*C_bl
    drag_balloon_force=q_b*s_b*C_bd
    buoyancy_force=(density_at_altitude(0)-density_hydrogen)*volume

    D_bl=np.array([0, 0, lift_balloon_force])
    D_bd=np.array([drag_balloon_force*cos(phi), drag_balloon_force*sin(phi), 0])
    B=np.array([0, 0, buoyancy_force(balloon_altitude)])
    W_b=np.array(5)
    F=D_bl+D_bd+B-W_b

    #CHANGING COORDINATE SYSTEM from 3d to 2d
    fx=np.take(F, 0) #towards right
    fy=np.take(F, 2) #upwards
    return fx, fy

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
    '''
    Create the rotation matrix of one 2D line element
    :param coords1: coordinates of first endpoint
    :param coords2: coordinates of second endpoint
    :return: 4x4 transformation matrix for the line element
    '''

    theta = atan2(coords2[1] - coords1[1], coords2[0] - coords1[0])
    labda = cos(theta)
    mu = sin(theta)
    trans_matrix = np.matrix([[labda, mu, 0, 0], [-mu, labda, 0, 0], [0, 0, labda, mu], [0, 0, -mu, labda]])
    return trans_matrix


def split_eq_equation(K, U, R, P, DOF=2):
    '''
    Split the parameters in the equilibrium equation in reduced and constrained versions.
    :param K: global stiffness matrix
    :param U: displacement vector (unknown, zero for now)
    :param R: reaction forces vector (unknown, zero for now)
    :param P: applied forces vector (known)
    :param DOF: number of degrees of freedom
    :return: Dictionary containing the split variables
    '''

    bc = np.zeros(U.shape[0])
    bc[0:DOF] = 1  # Only constrain the first point
    constr_DOF = np.nonzero(bc)[0]  # indices of constrained degrees of freedom

    non_bc = np.ones(U.shape[0])
    non_bc[constr_DOF] = 0  # non-constrain all points except the constrained points
    free_DOF = np.nonzero(non_bc)[0]  # indices of non-constrained degrees of freedom

    split = {}
    split['Kr'] = K[np.ix_(free_DOF, free_DOF)]
    split['Ks'] = K[np.ix_(constr_DOF, constr_DOF)]
    split['Krs'] = K[np.ix_(free_DOF, constr_DOF)]
    split['Ksr'] = K[np.ix_(constr_DOF, free_DOF)]

    split['Pr'] = P[free_DOF]
    split['Ps'] = P[constr_DOF]

    split['Rr'] = R[free_DOF]
    split['Rs'] = R[constr_DOF]

    split['Ur'] = U[free_DOF]
    split['Us'] = U[constr_DOF]

    return split


def gen_stiffness_matrix_element(E, A, begin_coords, end_coords):
    """
    :param E: E-mod
    :param A: cross Area
    :return: global stiffness_matrix element
    """
    transformation_matrix = get_trans_matrix(begin_coords, end_coords)
    L = np.sqrt((end_coords[0] - begin_coords[0]) ** 2 + (end_coords[1] - begin_coords[1]) ** 2)
    stiffness_matrix_element = ((E * A) / L) * np.array([[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]])
    global_matrix_element = transformation_matrix.transpose() @ stiffness_matrix_element @ transformation_matrix
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


def get_wind_force():
    return 60  # N


def make_load_vector(coords, material="uhmpe", balloon_forces=(4000, 1500 * 9.81)):
    """
    generate load vector, not assuming tandum balloons, just a top balloon
    :param mesh: numpu array of shape [2, n]
    :param material: string, material name from dictionary
    :param balloon_forces: Tuple, (x force, y force)
    :return: load vector of shape [n, 1]
    """

    # generate shape of load vector
    # [Fx1, F1y, Fx2, Fy2 ...]
    load_vector = np.zeros([2 * len(coords[0]), 1])

    wind_force = get_wind_force()

    density = material_dict[material]["density"]
    length_of_element = coords[1, 1]
    area = np.pi * radius_wire ** 2
    print("mass of wire in [kg] =", int(area * length_of_element * density * (len(coords[0]) - 1)))

    material_force = float(density * length_of_element * area * g)  # N

    # construct actual load vector
    load_vector[1] = -0.5 * material_force
    for numb, item in enumerate(load_vector):
        if numb % 2 == 1 and numb > 1:
            load_vector[numb] = -material_force  # downwards
        if numb % 2 == 0:
            load_vector[numb] = wind_force  # to the right
    load_vector[-2] += balloon_forces[0]  # x force
    load_vector[-1] += balloon_forces[1] + 0.5 * material_force  # y force

    return load_vector


mesh = create_mesh(5)
print(mesh)
load_vector = make_load_vector(mesh)
print(load_vector, load_vector.shape)
coordlst = create_mesh(3)

# print(create_mesh(3))
#
# print(gen_stiffness_matrix_element(100, 10 ** -2, 1, [0, 0], [np.cos(np.radians(60)), np.sin(np.radians(60))]))
# print(gen_stiffness_matrix_element(100, 10 ** -2, 1, [0, 0], [1, 1]))
# array = np.array([[[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]]])
# print(make_global_stiffness_matrix(array))

## set up dataframe for use ##

# mass
# length_of_segment = total_wire_length / wire_segments
# volume_of_segment = area_of_segment * length_of_segment
# mass_of_segment = volume_of_segment * density_of_material
# mass_list = mass_of_segment * np.ones(wire_segments)
#
# # wind/gust
# wind_profile_list = np.zeros(wire_segments)
#
# # initial tension
# initial_tension_list = np.zeros(wire_segments)
#
# # orientation
# angle_of_orientation_list = np.zeros(wire_segments)
#
# # positioning
# top_position_list = (np.ones(wire_segments), np.ones(wire_segments))  # tuple -> x,y
# bottom_position_list = (np.ones(wire_segments), np.ones(wire_segments))  # tuple -> x,y
