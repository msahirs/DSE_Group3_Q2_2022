import numpy as np
import matplotlib.pyplot as plt
import ISA_general

# atmosphere = isa.get_atmosphere()

# Values
L_charac = 1
h = 20000.0
v_wind = 5
Cp = 1000
k = 2 * 10 ** (-3)  # thermal conductivity
g = 9.81
sigma = 5.67 * 10 ** (-8)
I = 1353
Cp_module = 2900
a = 295.070

# Calcues
T_air, P, rho, mu = ISA_general.ISA(h)
nu = mu / rho  # kinematic viscocity
Pr = mu * Cp / k
alpha = k / rho / Cp
beta = 1 / T_air  # approx

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
    epsilon = 0.9  # Ge substrate
    q_emission = sigma * epsilon * (T ** 4 - T_air ** 4) * L_charac ** 2

    # direct absorption
    alpha_ab = 0.4  # TBD
    refl_top = 0.02
    I_ab = I * (1 - refl_top)
    q_abs = I_ab * alpha_ab * L_charac ** 2

    # CFRP conductivity
    epsilon_back = 0.13  # ?
    Cp_cfrp = 1040
    d_cfrp = 100 * 10 ** (-6)  # m
    conductivity_hor = 250  # W/m/K
    conductivity_ver = 3  # W/m/K
    q_abs_cfrp = epsilon_back * q_abs  # J/s
    q_conduct_cfrp = conductivity_hor * (T - T_cfrp) / d_cfrp
    if q_conduct_cfrp < q_abs_cfrp:
        print("HEAT OVERLOAD", t)

    # CFRP emission
    epsilon_cfrp = 0.88
    q_emission_cfrp = sigma * epsilon_cfrp * (T_cfrp ** 4 - T ** 4) * L_charac ** 2

    # CFRP forced convection
    Pr_cfrp = Pr
    Re_cfrp = Re
    Nu_cfrp_forced = 0.664 * Re_cfrp ** (1 / 2) * Pr_cfrp ** (1 / 3)
    h_cfrp_forced = Nu_cfrp_forced * k / L_charac
    q_cfrp_forced_conv = h_cfrp_forced * L_charac ** 2 * (T_cfrp - T_air)

    # CFRP free convection
    Ra_cfrp = g * beta / nu / alpha * (T_cfrp - T_air) * L_charac ** 3
    Nu_cfrp_free = 0.15 * Ra_cfrp ** (1 / 3)
    h_cfrp_free = Nu_cfrp_free * k / L_charac
    q_cfrp_free_conv = h_cfrp_free * L_charac ** 2 * (T_cfrp - T_air)

    # Time step
    dT_cfrp = (q_abs_cfrp - q_cfrp_forced_conv - q_cfrp_free_conv - q_emission_cfrp) / Cp_cfrp * dt
    T_cfrp = T_cfrp + dT_cfrp
    print(q_cfrp_forced_conv + q_cfrp_free_conv + q_emission_cfrp, "cfrp emissions")

    dT = (q_abs - q_forced_conv - q_free_conv - q_emission - q_abs_cfrp) / Cp_module * dt
    T = T + dT
    print(q_forced_conv, q_free_conv, q_emission, "cell emissions")
    print(q_abs, "total heat")

plt.plot(t_list, T_list)
#plt.plot(t_list, temp)
plt.show()
