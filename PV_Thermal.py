import matplotlib.pyplot as plt
import numpy as np
import math
import ISA_general
import datetime
import PVIV

# Input Variables
A = 2665  # Area of solar cell configuration [m^2]
dh = 1  # Distance between pv array and balloon [m]
h = 16820.0  # Height [m]
v_wind = 5  # Wind speed [m/s]

# Constants
Cp = 1005  # Specific heat capacity of air [J/kg/K]
k = 2 * 10 ** (-3)  # Thermal conductivity of air [W/m/K]
g = 9.81  # Gravitational acceleration [m/s^2]
sigma = 5.67 * 10 ** (-8)  # Boltzmann constant [W/m^2/K^4]
I_earth = 237  # Earth's infrared emission [W/m^2]

# Solar cell constants and calculations (Germanium)
epsilon = 0.9  # Ge substrate emission coefficient [-]
refl_top = 0.02  # Reflectivity of solar cell cap [-]
Rho_Ge = 5323  # Ge substrate density [kg/m^3]
Cp_Ge = 3200  # Specific heat capacity of  Ge [J/kg/K]
d_Ge = 75 * 10 ** (-6)  # Approx thickness Ge substrate [m]
Cp_module = Rho_Ge * Cp_Ge * d_Ge * A  # Heat capacity of PV [J/K]
power_pc = np.amax(PVIV.iv(28)[2])

# Backplane constants and calculations (CFRP)
Cp_cfrp = 1040  # Specific heat capacity of CFRP [J/kg/K]
epsilon_cfrp = 0.88  # CFRP emission coefficient [-]

# Air Calculations
T_air, P, rho, mu = ISA_general.ISA(h)
nu = mu / rho  # Kinematic viscosity [m^2/s]
Pr = mu * Cp / k  # Prantl number [-]
alpha = k / rho / Cp  # Thermal diffusivity of air [m^2/s]
beta = 1 / T_air  # Thermal expansion coefficient [1/K] (approx)
Cp_bottom = Cp * A * dh * rho
L_charac = 2 * np.sqrt(A / np.pi)  # Characteristic length [m]
R_charac = L_charac / 2

# Initializing
t_max = 86400
dt = 1
t_list = np.linspace(0, t_max, int(t_max / dt) + 1)

A_segment_ps = 0.5 * R_charac * 2 * np.degrees(np.arccos((R_charac - (v_wind * dt)) / R_charac))
New_air_ps = A_segment_ps / A

'''
solar_irr = np.genfromtxt('data/input_archive/relev_locs_zero/merged_all_PA.csv', delimiter=',')
flux = solar_irr[:, 30]
flux_max = np.amax(flux)
index_max = np.where(flux == flux_max)
print(index_max)
print(solar_irr[index_max, 1], 'month', solar_irr[index_max, 2], 'day')
time_step = (solar_irr[1, 4] - solar_irr[0, 4]) * 60  # seconds
indices_in_day = 86400 / time_step
flux_curve = flux[int(index_max - indices_in_day / 2): int(index_max + indices_in_day / 2)]
time_flux = []
for ii in range(0, len(flux_curve)):
    time_flux.append(ii * time_step)
#t_list = np.linspace(0, time_flux[len(time_flux)-1], int(time_flux[len(time_flux)-1] / dt) + 1)
flux_interp = np.interp(t_list, time_flux, flux_curve)
#flux_interp = np.interp(t_list, time_flux, flux)
'''
'''
solar_irr = np.genfromtxt('data/input_archive/elevation_gain/merged_all.csv',  delimiter=',')
flux_all = solar_irr[:, 30]
altitudes = solar_irr[:, 11]
flux = [] # 1440
q = 0
for i in range(1000+1440*q, 1440+1440*q):
    flux.append(flux_all[i])
for j in range(0+1440*q, 1000+1440*q):
    flux.append(flux_all[j])

time_step = (solar_irr[1, 4] - solar_irr[0, 4]) * 60  # seconds
time_flux = np.linspace(0, 86400, int(86400 / time_step))
flux_interp = np.interp(t_list, time_flux, flux)

solar_irr = np.genfromtxt('data/merged_fluxes.csv', delimiter=',')
flux = solar_irr[:, 30]
time_step = (solar_irr[1, 4] - solar_irr[0, 4]) * 60  # seconds
time_flux = np.linspace(0, 86400, int(86400 / time_step))
flux_interp = np.interp(t_list, time_flux, flux)
'''

solar_irr = np.genfromtxt('data/input_archive/PA_16200/merged_Final.csv', delimiter=',')
flux = solar_irr[:, 30]
time_step = 10
time_flux = np.linspace(0, 86400, int(86400 / time_step))
flux_max = np.amax(flux)
index_max = np.where(flux == flux_max)
print(index_max)
flux_curve1 = flux[6000:8639]
flux_curve2 = flux[0:6001]
flux_curve = res = [j for i in [flux_curve1, flux_curve2] for j in i]
flux_interp = np.interp(t_list, time_flux, flux_curve)
plt.plot(t_list, flux_interp)
plt.show()

T = T_air
T_list = []
T_bottom = T_air
T_bottom_list = []
q = [[], [], [], [], [], [], [], []]  # abs, emis, free, forced, emis, free, forced, gen

for t in range(len(t_list)):
    T_list.append(T - 273.15)
    T_bottom_list.append(T_bottom - 273.15)
    I_sun = flux_interp[t]

    if T - 273.15 < 28:
        eff = 0.35
    else:
        eff = np.amax(PVIV.iv(T - 273.15)[2]) / power_pc * 0.35

    # direct absorption
    alpha_ab = 1 - eff
    I_inc = I_sun * (1 - refl_top)
    q_gen = I_inc * eff * A
    q[7].append(q_gen*dt)  # Joule per timestep
    q_abs = I_inc * alpha_ab * A
    q[0].append(q_abs*dt)

    # emission radiation
    q_emission = sigma * epsilon * (T ** 4 - T_air ** 4) * A
    q[1].append(q_emission*dt)

    # free convection
    Ra = g * beta / nu / alpha * (T - T_air) * L_charac ** 3
    Nu_free = 0.15 * Ra ** (1 / 3)
    h_free = Nu_free * k / L_charac
    q_free_conv = h_free * A * (T - T_air)
    q[2].append(q_free_conv*dt)

    # forced convection (turbulent flow)
    Re = v_wind * rho * L_charac / mu
    Nu_forced = 0.037 * Re ** (4 / 5) * Pr ** (1 / 3)
    h_forced = Nu_forced * k / L_charac
    q_forced_conv = h_forced * A * (T - T_air)
    q[3].append(q_forced_conv*dt)

    # CFRP emission
    q_emission_cfrp = sigma * epsilon_cfrp * (T ** 4 - T_bottom ** 4) * (A * 0.9)
    q[4].append(q_emission_cfrp*dt)

    # CFRP free convection air layer
    Ra_cfrp = g * beta / nu / alpha * (T - T_bottom) * L_charac ** 3
    Nu_cfrp_free = 0.15 * Ra_cfrp ** (1 / 3)
    h_cfrp_free = Nu_cfrp_free * k / L_charac
    q_cfrp_free_conv = h_cfrp_free * (A * 0.9) * (T - T_bottom)
    q[5].append(q_cfrp_free_conv*dt)

    # CFRP forced convection air layer (turbulent flow)
    Pr_cfrp = Pr
    Re_cfrp = Re
    Nu_cfrp_forced = 0.037 * Re_cfrp ** (4 / 5) * Pr_cfrp ** (1 / 3)
    h_cfrp_forced = Nu_cfrp_forced * k / L_charac
    q_cfrp_forced_conv = h_cfrp_forced * (A * 0.9) * (T - T_bottom)
    q[6].append(q_cfrp_forced_conv*dt)

    # Time step

    dT = (
                 q_abs - q_forced_conv - q_free_conv - q_emission - q_emission_cfrp - q_cfrp_free_conv - q_cfrp_forced_conv) / Cp_module * dt
    T = T + dT
    dT_bottom = (q_emission_cfrp + q_cfrp_free_conv + q_cfrp_forced_conv) / Cp_bottom * dt
    T_bottom = (T_bottom + dT_bottom) * (1 - New_air_ps) + T_air * New_air_ps
    '''
    dT = (q_abs - q_forced_conv - q_free_conv - q_emission) / Cp_module * dt
    T = T + dT
    T_bottom = 0
    '''

# Finding maxima and printing
max_index = np.argmax(T_list)
print("\nMax temperature: ", T_list[max_index])
print("Total:")
print(sum(q[0]), "Joule absorbed")
print(sum(q[1]), "J released through top radiation", sum(q[1]) / sum(q[0]) * 100, "%")
print(sum(q[2]), "J released trough top free conv", sum(q[2]) / sum(q[0]) * 100, "%")
print(sum(q[3]), "J released trough top forced conv", sum(q[3]) / sum(q[0]) * 100, "%")
print(sum(q[4]), "J released through bottom radiation", sum(q[4]) / sum(q[0]) * 100, "%")
print(sum(q[5]), "J released trough bottom free conv", sum(q[5]) / sum(q[0]) * 100, "%")
print(sum(q[6]), "J released trough bottom free conv", sum(q[6]) / sum(q[0]) * 100, "%")

print('============================')
print(sum(q[7]) / 10 ** 9, 'Power generated (GJ)')
print(sum(q[7]) / 3600000, 'Power generated (kWh)')
print(np.amax(flux_interp), 'Max Flux (W/m2)')
print(np.where(flux_interp == np.amax(flux_interp)), 'Max Flux Time (s)')
print(np.amax(T_list), 'Max Temperature')
print(np.amax(PVIV.iv(np.amax(T_list))[2]), 'Power per cell at max temp (mW/m2)')
print((np.amax(PVIV.iv(np.amax(T_list))[2]) - np.amax(PVIV.iv(28)[2])) / np.amax(PVIV.iv(28)[2]) * 100,
      'Percent eff loss')
print(np.amax(PVIV.iv(np.amax(T_list))[2]) / power_pc * 35, 'Eff at max temp')
print(301.5 * 402 * 10 ** -6, 'Panel area (m2) at 12 cells')
print(np.amax(PVIV.iv(np.amax(T_list))[2]) / 1000 * 12, 'W per panel')
print(np.amax(PVIV.iv(np.amax(T_list))[2]) / 1000 / (301.5 * 402 * 10 ** -6) * 12, 'W/m2 of a panel')
print(1074762 / (np.amax(PVIV.iv(np.amax(T_list))[2]) / 1000 / (301.5 * 402 * 10 ** -6) * 12), 'm2 for 1074762 W')


power_gen = np.divide(q[7], 1000)

# Plotting
fig, ax1 = plt.subplots()

# First graph
color = 'tab:red'
ax1.set_xlabel('Time of day [hh:mm] UTC')
ax1.set_ylabel('Solar Irradiance [W/m^2]', color=color)
ax1.plot(t_list, flux_interp, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Second graph
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
plt.grid(axis='both')
color = 'tab:blue'
ax2.set_ylabel('Temperature [C]', color=color)
ax2.plot(t_list, T_list, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.yticks([-60, -50, -40,-30, -20, -10, 0, 10, 20, 30, 40])
'''
# Second graph
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
plt.grid(axis='both')
color = 'tab:blue'
ax2.set_ylabel('Effective Power Output [kW]', color=color)
ax2.plot(t_list, power_gen, color=color)
ax2.tick_params(axis='y', labelcolor=color)
'''

'''
# Set x-axis labels
div = 4
initial_time = 0
labels = []
zero = datetime.datetime.min
for i in range(math.floor(len(t_list) / (div * 3600))):
    timestep = datetime.timedelta(hours=initial_time + 16, minutes=20, seconds=i * div * 3600)
    labels.append((zero + timestep).time())

# labels = np.array([datetime.time(initial_time + div * i, 0) for i in range(math.floor(len(t_list) / div))])
for i in range(len(labels)):
    labels[i] = labels[i].strftime("%H:%M")
plt.xticks(np.arange(initial_time * 3600, t_max, t_max / (24 / div)), labels)
fig.tight_layout()
'''
# Set x-axis labels
div = 4
initial_time = 0
labels = []
zero = datetime.datetime.min
for i in range(math.floor(len(t_list) / (div * 3600))):
    timestep = datetime.timedelta(hours=initial_time + 16, minutes=20, seconds=i * div * 3600)
    labels.append((zero + timestep).time())

# labels = np.array([datetime.time(initial_time + div * i, 0) for i in range(math.floor(len(t_list) / div))])
for i in range(len(labels)):
    labels[i] = labels[i].strftime("%H:%M")
plt.xticks(np.arange(initial_time * 3600, t_max, t_max / (24 / div)), labels)
fig.tight_layout()

plt.show()
