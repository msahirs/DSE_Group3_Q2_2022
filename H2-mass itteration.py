import numpy as np
import matplotlib.pyplot as plt


def calc_mass_balloon(hydrongen_volume):
    return 80000


def h2_mass_iter(begin_mass, hydrogen_volume):
    """
    :param begin_mass: begin mass without balloon
    :param hydrogen_volume: nessecry to lift begin mass
    :return: final_mass: begin_mass + balloon mass
    """
    difference = 50
    i = 0
    inital_balloon_mass = 100

    while difference > 10 or i < 100:
        #calc end_mass
        end_mass = calc_mass_balloon(hydrogen_volume) + begin_mass
        #recalc H2 mass

        i += 1
    print(end_mass)
