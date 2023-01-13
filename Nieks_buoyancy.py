from ISA import ISA as I
import matplotlib.pyplot as plt


h = 0 # height [m]


g0 = 9.80665 # gravity constant [kg/m**2]

mass_extra = 4344/g0
mass_original = 4000
mass = mass_original + mass_extra

W = mass * g0



R_gas = 4116 # specific gas constant [J/(kg*K)

def Volume_calc(h, temp):
    ISA = I(h)
    rho_a_h = ISA[2]  # density [kg/m**3]
    p_gas_h = ISA[1]  # pressure at altitude of h2
    Pd = 0.5 * rho_a_h * 50 ** 2  # dynamic pressure
    d_p_gas = 2 * Pd  # pressure diff ( twice dynamic press) [N/m**2]
    d_T_gas = temp # temp diff [K]
    T_a = ISA[0]  # ambient temp [K]

    V_h = W / (g0 * (rho_a_h - ((p_gas_h + d_p_gas) / (R_gas * (T_a + d_T_gas)))))
    if h == 20000:
        print(V_h)
        print(d_p_gas)
    return V_h

def Lift_calc(h, V, temp):
    ISA = I(h)
    rho_a_h = ISA[2]  # density [kg/m**3]
    p_gas_h = ISA[1]  # pressure at altitude of h2
    Pd = 0.5 * rho_a_h * 50 ** 2  # dynamic pressure
    d_p_gas = 2 * Pd  # pressure diff ( twice dynamic press) [kg/m**2]
    d_T_gas = temp  # temp diff [K]
    T_a = ISA[0]  # ambient temp [K]

    lift = (g0 * (rho_a_h - ((p_gas_h + d_p_gas) / (R_gas * (T_a + d_T_gas))))) * V

    return lift




h1 = []
h2 = []
Vp = []
L = []


for j in range(101):
    h = j * 200
    V_p = Volume_calc(h, 30)
    h1.append(h)
    Vp.append(V_p)

for i in range(101):
    h = i *200 +10000
    up = Lift_calc(h, 60000, 0)/ g0
    L.append(up)
    h2.append(h)

# plt.plot(h1, Vp)
plt.plot(h2, L)
plt.show()
