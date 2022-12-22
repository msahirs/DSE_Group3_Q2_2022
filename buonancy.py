import ISA



h = 10000 # height [m]
ISA = ISA.ISA(h)
V_h = 80000 # volume balloon at altitude [m**3]
g0 = 9.80665 # gravity constant [kg/m**2]
rho_a_h = ISA[2] # density [kg/m**3]
p_gas_h = ISA[1] # pressure at altitude of h2
d_p_gas = 400 # pressure diff [kg/m**2]
d_T_gas = 0
T_a = ISA[0]


R_gas = 4124.2


Lift = g0 * V_h * (rho_a_h - ((p_gas_h + d_p_gas)/(R_gas * (T_a + d_T_gas)))) # N

lift_kg = Lift /g0
print(lift_kg)