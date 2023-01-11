import matplotlib.pyplot as plt
import numpy as np
import math
import ISA_general
import datetime
import PVIV


# Input Values
L_charac = 52  # Characteristic length [m]
A = 2700  # Area of solar cell configuration [m^2]
h = 20000.0  # Height [m]
v_wind = 5  # Wind speed [m/s]
albedo = 0.1  # Earth's albedo [-]

# Constants
Cp = 1005  # Specific heat capacity of air [J/kg/K]
k = 2 * 10 ** (-3)  # Thermal conductivity of air [W/m/K]
g = 9.81  # Gravitational acceleration [m/s^2]
sigma = 5.67 * 10 ** (-8)  # Boltzmann constant [W/m^2/K^4]
I_earth = 237  # Earth's infrared emission [W/m^2]

# Solar cell (Germanium)
epsilon = 0.9  # Ge substrate emission coefficient [-]
refl_top = 0.02  # Reflectivity of solar cell cap [-]
Rho_Ge = 5323  # Ge substrate density [kg/m^3]
Cp_Ge = 3200  # Specific heat capacity of  Ge [J/kg/K]
d_Ge = 160 * 10 ** (-6)  # Approx thickness Ge substrate [m]
Cp_module = Rho_Ge * Cp_Ge * d_Ge * A  # Heat capacity of PV [J/K]

# Backplane (CFRP)
Cp_cfrp = 1040  # Specific heat capacity of CFRP [J/kg/K]
k_cfrp_hor = 250  # Conductivity (hor) of CFRP [W/m/K]
k_cfrp_ver = 3  # Conductivity (ver) of CFRP [W/m/K]
epsilon_cfrp = 0.88  # CFRP emission coefficient [-]

# General Calculations
T_air, P, rho, mu = ISA_general.ISA(h)
nu = mu / rho  # Kinematic viscosity [m^2/s]
Pr = mu * Cp / k  # Prantl number [-]
alpha = k / rho / Cp  # Thermal diffusivity of air [m^2/s]
beta = 1 / T_air  # Thermal expansion coefficient [1/K] (approx)

# Data initialization (temporary)


# Initializing
t_max = 86400
dt = 1
t_list = np.arange(0, t_max, dt)

solar_irr = np.genfromtxt('data/merged_fluxes.csv', delimiter=',')
flux = solar_irr[:, 30]
steps = flux.size
time_step = (solar_irr[1, 4] - solar_irr[0, 4]) * 60  # seconds
time_flux = np.arange(0, 86400, time_step)
flux_interp = np.interp(t_list, time_flux, flux)

T = T_air
T_cfrp = T_air
T_list = []
q = [[], [], [], [], [], [], []]  # list of all heat flows: absorption, emission, free, forced, emission, free, forced

for t in t_list:
    T_list.append(T - 273.15)
    I_sun = flux_interp[t]

    # direct absorption (from sun & earth)
    alpha_ab = 0.65  # TBD
    #    I_ab = I_sun * (1 - refl_top)
    I_ab = I_sun * (1 - refl_top)
    # I_ab = (I_sun * (1+albedo) + I_earth) * (1 - refl_top)
    q_abs = I_ab * alpha_ab * A
    q[0].append(q_abs)

    # emission radiation
    q_emission = sigma * epsilon * (T ** 4 - T_air ** 4) * A
    q[1].append(q_emission)

    # free convection
    Ra = g * beta / nu / alpha * (T - T_air) * L_charac ** 3
    Nu_free = 0.15 * Ra ** (1 / 3)
    h_free = Nu_free * k / L_charac
    q_free_conv = h_free * A * (T - T_air)
    q[2].append(q_free_conv)

    # forced convection (turbulent flow)
    Re = v_wind * rho * L_charac / mu
    Nu_forced = 0.037 * Re ** (4 / 5) * Pr ** (1 / 3)
    h_forced = Nu_forced * k / L_charac
    q_forced_conv = h_forced * A * (T - T_air)
    q[3].append(q_forced_conv)

    # conduction to backplane
    T_bottom = T_air

    # CFRP emission
    q_emission_cfrp = sigma * epsilon_cfrp * (T ** 4 - T_bottom ** 4) * A
    q[4].append(q_emission_cfrp)

    # CFRP free convection air layer
    Ra_cfrp = g * beta / nu / alpha * (T - T_bottom) * L_charac ** 3
    Nu_cfrp_free = 0.15 * Ra_cfrp ** (1 / 3)
    h_cfrp_free = Nu_cfrp_free * k / L_charac
    q_cfrp_free_conv = h_cfrp_free * A * (T - T_bottom)
    q[5].append(q_cfrp_free_conv)

    # CFRP forced convection air layer (turbulent flow)
    Pr_cfrp = Pr
    Re_cfrp = Re
    Nu_cfrp_forced = 0.037 * Re_cfrp ** (4 / 5) * Pr_cfrp ** (1 / 3)
    h_cfrp_forced = Nu_cfrp_forced * k / L_charac
    q_cfrp_forced_conv = h_cfrp_forced * A * (T - T_bottom)
    q[6].append(q_cfrp_forced_conv)

    # Time step
    dT = (q_abs - q_forced_conv - q_free_conv - q_emission - q_emission_cfrp - q_cfrp_free_conv - q_cfrp_forced_conv) / Cp_module * dt
    T = T + dT


# Finding maxima and printing
max_index = np.argmax(T_list)
print("\nMax temperature: ", T_list[max_index])
print("At this point in time the heat balance consists of:")
print(round(q[0][max_index]), "Watts absorbed")
print(round(q[1][max_index]), "Watts released through top radiation", round(q[1][max_index] / q[0][max_index] * 100, 2),
      "%")
print(round(q[2][max_index]), "Watts released trough top free conv", round(q[2][max_index] / q[0][max_index] * 100, 2),
      "%")
print(round(q[3][max_index]), "Watts released trough top forced conv",
      round(q[3][max_index] / q[0][max_index] * 100, 2), "%")
print(round(q[4][max_index]), "Watts released through bottom radiation",
      round(q[4][max_index] / q[0][max_index] * 100, 2),
      "%")
print(round(q[5][max_index]), "Watts released trough bottom free conv",
      round(q[5][max_index] / q[0][max_index] * 100, 2),
      "%")
print(round(q[6][max_index]), "Watts released trough bottom forced conv",
      round(q[6][max_index] / q[0][max_index] * 100, 2),
      "%")

# Plotting
fig, ax1 = plt.subplots()

# First graph
color = 'tab:blue'
ax1.set_xlabel('time')
ax1.set_ylabel('temperature (C)', color=color)
ax1.plot(t_list, T_list, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Second graph
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:orange'
ax2.set_ylabel('solar irradiance (W/m^2)', color=color)  # we already handled the x-label with ax1
ax2.plot(t_list, flux_interp, color=color)
ax2.tick_params(axis='y', labelcolor=color)
'''
# Set x-axis labels
div = 4
initial_time = 2
labels = np.array([datetime.time(initial_time + div * i, 0) for i in range(math.floor(len(t_list) / div))])
for i in range(len(labels)):
    labels[i] = labels[i].strftime("%H:%M")
plt.xticks(t_list[initial_time::div], labels)
'''
fig.tight_layout()

print(PVIV.iv(np.amax(T_list))[0])
plt.show()

