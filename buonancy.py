import ISA
import matplotlib.pyplot as plt


h = 20000 # height [m]
ISA = ISA.ISA(h)
#V_h = 80000 # volume balloon at altitude [m**3]
g0 = 9.80665 # gravity constant [kg/m**2]
rho_a_h = ISA[2] # density [kg/m**3]
p_gas_h = ISA[1] # pressure at altitude of h2
d_p_gas = 400 # pressure diff [kg/m**2]
d_T_gas = 0 # temp diff [K]
T_a = ISA[0] # ambient temp [K]
mass = 5000
W = mass * g0


R_gas = 4116 # specific gas constant [J/(kg*K)

V_h = W / (g0  * (rho_a_h - ((p_gas_h + d_p_gas)/(R_gas * (T_a + d_T_gas)))))
Lift = g0 * V_h * (rho_a_h - ((p_gas_h + d_p_gas)/(R_gas * (T_a + d_T_gas)))) # N

lift_kg = Lift /g0
print(p_gas_h)
print(rho_a_h)
print(round(V_h, 3), "m3")
print(V_h/2600)