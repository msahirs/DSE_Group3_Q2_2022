import math
import matplotlib.pyplot as plt
import ISA_general

# Input Values
L_charac = 1               # Characteristic length [m]
h = 20000.0                 # Height [m]
v_wind = 5                  # Wind speed [m/s]

# Constants
Cp = 1000                   # Specific heat capacity of air [J/kg]
k = 2 * 10 ** (-3)          # Thermal conductivity of air [W/m/K]
g = 9.81                    # Gravitational acceleration [m/s2]
sigma = 5.67 * 10 ** (-8)   # Boltzmann constant
I = 1353                    # Incident solar intensity [W/m2]
Cp_module = 2900            # Specific heat capacity of PV [J/kg]

# Calculations
T_air, P, rho, mu = ISA_general.ISA(h)
nu = mu / rho               # Kinematic viscosity [m2/s]
Pr = mu * Cp / k            # Prantl number [-]
alpha = k / rho / Cp        # Thermal diffusivity of air [m2/s]
beta = 1 / T_air            # Thermal expansion coefficient [1/K] (approx)

# Solar cell
epsilon = 0.9               # Ge substrate emission coefficient [-]
refl_top = 0.02             # Reflectivity of solar cell cap [-]
d_contact = 5*10**-6        # Bottom metal contact thickness [m]
k_contact = 429  # Conductivity of metal contact (Ag) [W/m/K]

# Backplane
Cp_cfrp = 1040              # Specific heat capacity of CFRP [J/kg]
d_cfrp = 100 * 10 ** (-6)   # Thickness CFRP [m]
k_cfrp_hor = 250      # Conductivity (hor) of CFRP [W/m/K]
k_cfrp_ver = 3        # Conductivity (ver) of CFRP [W/m/K]
epsilon_cfrp = 0.88         # CFRP emission coefficient [-]



# Initializing
dt = 1
t_list = []
T = T_air
T_list = []
T_cfrp = T_air
temp = []

for t in range(0, 10000, dt):
    t_list.append(t)
    T_list.append(T - 273.15)

    # forced convection
    Re = v_wind * rho * L_charac / mu
    Nu_forced = 0.664 * Re ** (1 / 2) * Pr ** (1 / 3)
    h_forced = Nu_forced * k / L_charac
    q_forced_conv = h_forced * L_charac ** 2 * (T - T_air)

    # free convection
    Ra = g * beta / nu / alpha * (T - T_air) * L_charac ** 3
    Nu_free = 0.15 * Ra ** (1 / 3)
    h_free = Nu_free * k / L_charac
    q_free_conv = h_free * L_charac ** 2 * (T - T_air)

    # emission radiation
    q_emission = sigma * epsilon * (T ** 4 - T_air ** 4) * L_charac ** 2

    # direct absorption
    alpha_ab = 0.65  # TBD
    I_ab = I * (1 - refl_top)
    q_abs = I_ab * alpha_ab * L_charac ** 2

    # energy generation ~advection
    ff = (2.43 * 16.8) / (2.73 * 17.41)
    k1 = 10**6
    q_energygen = ff * I_ab * math.log(k1 * I_ab) / T


    # conduction to backplane
    T_cfrp = T

    # CFRP emission
    q_emission_cfrp = sigma * epsilon_cfrp * (T ** 4 - T_air ** 4) * L_charac ** 2

    # CFRP forced convection air layer
    Pr_cfrp = Pr
    Re_cfrp = Re
    Nu_cfrp_forced = 0.664 * Re_cfrp ** (1 / 2) * Pr_cfrp ** (1 / 3)
    h_cfrp_forced = Nu_cfrp_forced * k / L_charac
    q_cfrp_forced_conv = h_cfrp_forced * L_charac ** 2 * (T_cfrp - T_air)

    # CFRP free convection air layer
    Ra_cfrp = g * beta / nu / alpha * (T_cfrp - T_air) * L_charac ** 3
    Nu_cfrp_free = 0.15 * Ra_cfrp ** (1 / 3)
    h_cfrp_free = Nu_cfrp_free * k / L_charac
    q_cfrp_free_conv = h_cfrp_free * L_charac ** 2 * (T_cfrp - T_air)

    # Time step
    dT = (q_abs - q_forced_conv - q_free_conv - q_emission - q_emission_cfrp - q_cfrp_free_conv - q_cfrp_forced_conv - q_energygen) / Cp_module * dt
    T = T + dT

print(q_abs, "absorped")
print(q_forced_conv, "fo conv")
print(q_free_conv, "fr conv")
print(q_emission, "emission")
print(q_emission_cfrp, "cfrp emission")
print(q_cfrp_free_conv, "cfrp fr conv")
print(q_cfrp_forced_conv, "cfrp fo conv")
print(q_energygen, "advection")


plt.plot(t_list, T_list)
#plt.plot(t_list, temp)
plt.show()
