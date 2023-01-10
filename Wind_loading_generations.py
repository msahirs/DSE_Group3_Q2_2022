import numpy as np
import matplotlib.pyplot as plt
from ISA_general import ISA
import scipy as sc
from scipy import interpolate

# r = 0.01  # m
# cd = 1  # -


def wind_model(h):
    dataset = np.array([[0, 11],
                        [2500, 15],
                        [5000, 29],
                        [7500, 41],
                        [10000, 51],
                        [12000, 43],
                        [13500, 32],
                        [16000, 20],
                        [17000, 11],
                        [20000, 9],
                        [23000, 11],
                        [25500, 15]])

    y = dataset[:, 1]  # wind speed
    x = dataset[:, 0]  # altitude
    windspeed_from_alt = sc.interpolate.interp1d(x, y, kind='quadratic')
    return windspeed_from_alt(h)


def create_mesh(nodes, altitude_balloon=20000, altitude_ground=0):
    """
    create mesh for the wire if needed
    [[xlist], [ylist]
    """
    y_list = np.linspace(altitude_ground, altitude_balloon, nodes)  # using bottem as well
    x_list = np.zeros(y_list.shape)
    coords = np.array([x_list, y_list])
    return coords


def wind_profile(heights, select=1, plot=True):
    wind_speed_array = np.zeros(heights.shape)  # right is positive
    if select == 1:
        "uniform wind"
        for numb, item in enumerate(heights):
            wind_speed_array[numb] = 5  # m/s

    if select == 2:
        "linear wind, with start point b and slope a"
        a = 0.0005
        b = -a * heights[-1] / 2
        for numb, item in enumerate(heights):
            wind_speed_array[numb] = a * item + b  # m/s

    if select == 3:
        "parabolic wind"
        a, b, c = 10, 2, 0
        for numb, item in enumerate(heights):
            wind_speed_array[numb] = a * item * item + b * item + c  # m/s

    if select == 4:
        "quadratic spline interpolated wind profile"
        wind_speed_array = wind_model(heights)

    elif type(select) != int:
        degree = int(input("What degree is needed?\t\tAssume shape a*x^n + b*x^(n-1) + ....\n"))
        list_of_degree_values = []
        for numb in range(degree + 1):
            value = float(input(f"value for degree {degree - numb}\n"))
            list_of_degree_values.append(value)

        for numbi, height in enumerate(heights):
            wind_speed = 0
            for numbj, item in enumerate(list_of_degree_values):
                wind_speed += item * height ** (degree - numbj)
            wind_speed_array[numbi] = wind_speed  # m/s

    if plot:
        show_wind_profile(wind_speed_array, heights)

    return wind_speed_array


def show_wind_profile(x, y):
    plt.plot(x, y, label="Wind speed profile", c="black", marker=".", markersize=10)
    plt.plot(np.zeros(y.shape), y, label="Original position", c="gray", marker=".", markersize=10)
    for numb in range(len(y)):
        plt.arrow(0, y[numb], x[numb], 0, color="gray", length_includes_head=True,
                  linestyle="--")  # , head_length=10, head_width=4)
    plt.legend()
    plt.show()


def calc_drag_on_wire(x, y, wind_profile, length_of_element, r, Cd):
    drag_on_wire = []
    # for element_numb in range(len(mesh[0]) - 1):
    #     # calc angle between mesh point
    #     beta = atan2(x[element_numb] - x[element_numb - 1],
    #                  y[element_numb] - y[element_numb - 1])  # returns angle in radians
    #     velocity = wind_profile[element_numb]
    for node_numb in range(len(x)):
        velocity = wind_profile[node_numb]
        density = ISA(y[node_numb])[2]
        area = r * length_of_element  # should be times 2, but next equation should be halved, so it cancelled
        drag_on_segment = Cd * density * velocity * abs(velocity) * area
        drag_on_wire.append(drag_on_segment)
    return drag_on_wire

# mesh = create_mesh(500)
# x, y = mesh[0], mesh[1]
# config = 2
# drag_on_wire = calc_drag_on_wire(x, y, wind_profile(mesh[1], config), mesh[1][1])
# print(drag_on_wire)
# print(sum(drag_on_wire))
