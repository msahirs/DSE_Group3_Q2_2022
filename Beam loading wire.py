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
    material_dict["steel"]["e-mod"] = 196 * 10 ** 9  # Pa
    material_dict["steel"]["density"] = 7.86 * 10 ** 3  # kg/m^3
    material_dict["steel"]["tensile_ult"] = 860 * 10 ** 6  # Pa
    material_dict["steel"]["tensile_yield"] = 690 * 10 ** 6  # Pa

    # add aluminium
    material_dict["allum"] = dict()
    material_dict["allum"]["e-mod"] = 70 * 10 ** 9  # Pa
    material_dict["allum"]["density"] = 2.8 * 10 ** 3  # kg/m^3
    material_dict["allum"]["tensile_ult"] = 350 * 10 ** 6  # Pa
    material_dict["allum"]["tensile_yield"] = 300 * 10 ** 6  # Pa

    # add Titanium
    material_dict["titan"] = dict()
    material_dict["titan"]["e-mod"] = 110 * 10 ** 9  # Pa
    material_dict["titan"]["density"] = 4.43 * 10 ** 3  # kg/m^3
    material_dict["titan"]["tensile_ult"] = 900 * 10 ** 6  # Pa
    material_dict["titan"]["tensile_yield"] = 830 * 10 ** 6  # Pa

    # add UHMPE
    material_dict["uhmpe"] = dict()
    material_dict["uhmpe"]["e-mod"] = 700 * 10 ** 9  # Pa
    material_dict["uhmpe"]["density"] = 0.93 * 10 ** 3  # kg/m^3
    material_dict["uhmpe"]["tensile_ult"] = 1100 * 10 ** 6  # Pa
    material_dict["titan"]["tensile_yield"] = 0
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
        self.wind_area_balloon = 50
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


# s_b - characteristic area of the balloon, phi-angle between wind direction and x-axis
def balloon_tension(phi, density_hydrogen, h, s_b):
    Balloon = balloon(1, 2, 3, 4)  ##placeholder values
    q_b = Balloon.q_balloon
    lift_balloon_force = q_b * s_b * Balloon.lift_coeff
    drag_balloon_force = q_b * s_b * Balloon.drag_coeff
    buoyancy_force = (density_at_altitude(h) - density_hydrogen) * Balloon.volume

    D_bl = np.array([0, 0, lift_balloon_force])
    D_bd = np.array([drag_balloon_force * cos(phi), drag_balloon_force * sin(phi), 0])
    B = np.array([0, 0, buoyancy_force(h)])
    W_b = np.array(Balloon.weight)
    F = D_bl + D_bd + B - W_b

    # CHANGING COORDINATE SYSTEM from 3d to 2d
    fx = np.take(F, 0)  # towards right
    fy = np.take(F, 2)  # upwards
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
    """
    Create the rotation matrix of one 2D line element
    :param coords1: coordinates of first endpoint
    :param coords2: coordinates of second endpoint
    :return: 4x4 transformation matrix for the line element
    """

    theta = atan2(coords2[1] - coords1[1], coords2[0] - coords1[0])  # returns angle in radians
    # print("angle is", degrees(theta))
    labda = cos(theta)  # round otherwise get 10^-32 and such small values
    mu = sin(theta)
    trans_matrix = np.matrix([[labda, mu, 0, 0], [-mu, labda, 0, 0], [0, 0, labda, mu], [0, 0, -mu, labda]])
    return trans_matrix


def split_eq_equation(K, U, R, P, DOF=3):
    """
    Split the parameters in the equilibrium equation in reduced and constrained versions.
    :param K: global stiffness matrix
    :param U: displacement vector (unknown, zero for now)
    :param R: reaction forces vector (unknown, zero for now)
    :param P: applied forces vector (known)
    :param DOF: number of degrees of freedom
    :return: Dictionary containing the split variables
    """

    bc = np.zeros(U.shape[0])
    bc[0:DOF] = 1  # Only constrain the first point
    constr_DOF = np.nonzero(bc)[0]  # indices of constrained degrees of freedom

    non_bc = np.ones(U.shape[0])
    non_bc[constr_DOF] = 0  # non-constrain all points except the constrained points
    free_DOF = np.nonzero(non_bc)[0]  # indices of non-constrained degrees of freedom

    split = {}
    # print(K)
    print(free_DOF)
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


# def gen_stiffness_matrix_element(begin_coords, end_coords, E=1e+9, A=0.0001):
#     """
#     :param E: E-mod
#     :param A: cross Area
#     :return: global stiffness_matrix element of truss
#     """
#     transformation_matrix = get_trans_matrix(begin_coords, end_coords)
#     L = np.sqrt((end_coords[0] - begin_coords[0]) ** 2 + (end_coords[1] - begin_coords[1]) ** 2)
#     stiffness_matrix_element = ((E * A) / L) * np.array([[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]])
#     global_matrix_element = transformation_matrix.transpose() @ stiffness_matrix_element @ transformation_matrix
#     return global_matrix_element


def gen_stiffness_matrix_beam_element(begin_coords, end_coords):
    """
    :param begin_coords: list x, y
    :param end_coords: list x, y
    :return: stiffness matrix of a beam element based on given coordinates
    """
    transformation_matrix = get_trans_matrix_beam(begin_coords, end_coords)
    L = np.sqrt((end_coords[0] - begin_coords[0]) ** 2 + (end_coords[1] - begin_coords[1]) ** 2)
    row1 = np.array([1, 0, 0, -1, 0, 0])
    row2 = np.array([0, 12, -6, 0, -12, -6])
    row3 = np.array([0, -6, 4, 0, 6, 2])
    row4 = np.array([-1, 0, 0, 1, 0, 0])
    row5 = np.array([0, -12, 6, 0, 12, 6])
    row6 = np.array([0, -6, 2, 0, 6, 4])
    stiffness_matrix_element = np.array([row1, row2, row3, row4, row5, row6])  # local
    global_matrix_element = transformation_matrix.transpose() @ stiffness_matrix_element @ transformation_matrix
    return global_matrix_element


def get_trans_matrix_beam(coords1, coords2):
    """
    Create the rotation matrix of one 2D line element
    :param coords1: coordinates of first endpoint
    :param coords2: coordinates of second endpoint
    :return: 6x6 transformation matrix for the line element
    """

    theta = atan2(coords2[1] - coords1[1], coords2[0] - coords1[0])  # returns angle in radians
    labda = cos(theta)  # consider rounding otherwise get 10^-32 and such small values
    mu = sin(theta)
    row1 = np.array([labda, mu, 0, 0, 0, 0])
    row2 = np.array([-mu, labda, 0, 0, 0, 0])
    row3 = np.array([0, 0, 1, 0, 0, 0])
    row4 = np.array([0, 0, 0, labda, mu, 0])
    row5 = np.array([0, 0, 0, -mu, labda, 0])
    row6 = np.array([0, 0, 0, 0, 0, 1])
    trans_matrix = np.array([row1, row2, row3, row4, row5, row6])
    return trans_matrix


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
    :param mesh: numpy array of shape [2, n]
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
    load_vector[1] = -0.5 * material_force  # half of material force at bottom
    for numb, item in enumerate(load_vector):
        if numb % 2 == 1 and numb > 1:
            load_vector[numb] = -material_force  # downwards
        if numb % 2 == 0:
            load_vector[numb] = wind_force  # to the right
    load_vector[-2] += balloon_forces[0]  # x force
    load_vector[-1] += balloon_forces[1] + 0.5 * material_force  # y force balloon + half of material force at top
    return load_vector


def sequential_element_matrices(coords):
    """
    Connect the nodes of a tether, one long sequence from top to bottom
    :param coords: array with shape (# of dimensions, # of nodes)
    :return: list of stiffness matrices of all tether elements
    """
    element_matrices = []
    for i in range(coords.shape[1] - 1):
        matrix = gen_stiffness_matrix_beam_element(coords[:, i], coords[:, i + 1])
        element_matrices.append(matrix)
    return element_matrices


def calc_stress_and_strain(mesh, displacement):
    final_points = [mesh[0] + displacement[0], mesh[1] + displacement[1]]
    strain_list = []
    stress_list = []
    for element_numb in range(len(mesh[0]) - 1):
        initial_length = np.sqrt((mesh[0][element_numb] - mesh[0][element_numb + 1]) ** 2 + (
                mesh[1][element_numb] - mesh[1][element_numb + 1]) ** 2)
        final_length = np.sqrt((final_points[0][element_numb] - final_points[0][element_numb + 1]) ** 2 + (
                final_points[1][element_numb] - final_points[1][element_numb + 1]) ** 2)
        elongation = final_length - initial_length
        strain = elongation / initial_length
        stress = strain * material_dict["uhmpe"]["e-mod"]
        strain_list.append(strain)
        stress_list.append(stress)
    return strain_list, stress_list


def plot_displacements(mesh, displacements):
    "x points, y points"
    plt.plot(mesh[0], mesh[1], label="initial state", c="gray", marker=".", markersize=10)
    plt.plot(mesh[0] + displacements[0], mesh[1] + displacements[1], label="final state", c="black", marker=".",
             markersize=10)
    plt.xlabel("horizontal distance [meter]")
    plt.ylabel("vertical distance [meter]")
    plt.legend()
    plt.show()


dof = 3
nodes = 3

U = np.zeros(dof * nodes)
P = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0])  # [x, y, moment]    repeat
R = np.zeros(dof * nodes)
mesh = np.array([[0, 0, 0], [0, 1, 2]])

stiffness_matrix = make_global_stiffness_matrix(
    [gen_stiffness_matrix_beam_element([0, 0], [0, 1]), gen_stiffness_matrix_beam_element([0, 1], [0, 2])])

print(stiffness_matrix)
split_vars = split_eq_equation(stiffness_matrix, U, R, P, dof)
print("\n")
print(split_vars['Kr'])
split_vars['Ur'] = np.linalg.inv(split_vars['Kr']).dot(split_vars['Pr'])
split_vars['Rs'] = split_vars['Ksr'].dot(split_vars['Ur']) - split_vars['Ps']

print("movement of elements:\n", split_vars['Ur'])
print("reaction forces:\n", split_vars['Rs'])
plot_displacements(mesh, split_vars['Ur'])

# print(calc_stress_and_strain(mesh, displacements))
# plot_displacements(mesh, displacements)
# mesh = np.array([[0,2,4], [0,0,0]])
# print(sequential_element_matrices(mesh))
# stiffness_matrix = make_global_stiffness_matrix(sequential_element_matrices(mesh))
# print(stiffness_matrix)


# nodes = 2
# dof = 2
#
# coordlst = create_mesh(nodes, altitude_balloon=6)
# coordlst = np.array([[0, 1], [0, 1]])
# el_matrices = sequential_element_matrices(coordlst)
# # print(el_matrices)
# stiff_matrix = make_global_stiffness_matrix(el_matrices)
# # print(stiff_matrix)
#
# # print(el_matrices)
# U = np.zeros(dof * nodes)
# P = np.array([0, 0, 1, 1])
# R = np.zeros(dof * nodes)
#
# split_vars = split_eq_equation(stiff_matrix, U, R, P, dof)
# print(stiff_matrix)
# print("\n")
# print(split_vars['Kr'])
# split_vars['Ur'] = np.linalg.inv(split_vars['Kr']).dot(split_vars['Pr'])
# split_vars['Rs'] = split_vars['Ksr'].dot(split_vars['Ur']) - split_vars['Ps']
#
# print(split_vars['Ur'], split_vars['Rs'])