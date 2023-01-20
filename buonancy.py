from ISA import ISA as I
import matplotlib.pyplot as plt

g0 = 9.80665 # gravity constant [kg/m**2]
mass = 5653
W = mass * g0
R_gas =  4124 # specific gas constant [J/(kg*K)

h1 = []
h2 = []
Vp = []
L = []
Temps1 = []
rho = []
def Volume_calc(h, temp):
    ISA = I(h)
    rho_a_h = ISA[2]  # density [kg/m**3]
    p_gas_h = ISA[1]  # pressure at altitude of h2
    Pd = 0.5 * rho_a_h * 30 ** 2  # dynamic pressure [where 30 is the max wind speed]
    d_p_gas = 2 * Pd  # pressure diff ( twice dynamic press) [kg/m**2]
    d_T_gas = temp  # temp diff [K]
    T_a = ISA[0]  # ambient temp [K]

    rho_gas = ((p_gas_h + d_p_gas) / (R_gas * (T_a + d_T_gas)))

    V_h = W / (g0 * (rho_a_h - rho_gas))

    return V_h, rho_a_h, rho_gas, p_gas_h

def Lift_calc(h, V, temp):
    ISA = I(h)
    rho_a_h = ISA[2]  # density [kg/m**3]
    p_gas_h = ISA[1]  # pressure at altitude of h2
    Pd = 0.5 * rho_a_h * 30 ** 2  # dynamic pressure
    d_p_gas = 2 * Pd  # pressure diff ( twice dynamic press) [kg/m**2]
    d_T_gas = temp  # temp diff [K]
    T_a = ISA[0]  # ambient temp [K]

    lift = (g0 * (rho_a_h - ((p_gas_h + d_p_gas) / (R_gas * (T_a + d_T_gas))))) * V

    return lift

for j in range(241):
    h = j * 100
    V_p, rho_a, rho_gas, p_gas = Volume_calc(h, 0)
    h1.append(h/1000)
    Vp.append(V_p)
    V_p0, rho_a0, rho_gas0, p_gas0 = Volume_calc(0, 0)
    rho.append(100 - (rho_gas/rho_gas0)* 100)



for i in range(101):
    temps = i
    up = Lift_calc(18000, 49827.91610806447, temps)
    L.append(up/1000)
    Temps1.append(temps)

print('Volume', Volume_calc(18000, 40))
#####   sizing ballonet    ####

plt.xlabel('Altitude (km)')
plt.ylabel('Percentage of size ballonet over total volume (-)')
plt.xlim(0, 22)
plt.ylim(0,100)
plt.plot(h1, rho)
plt.grid()
plt.show()

######  Changing lift for varying diff temp   ####

plt.plot(Temps1, L)
plt.xlim(0, 100)
plt.title('Volume of 49828 m^3 at 18 km altitude')
plt.xlabel('Differential temperature (K)')
plt.ylabel('Lift (kN)')
plt.grid()
plt.show()

######  Changing Volume for varying height  #####

plt.xlabel('Altitude (km)')
plt.ylabel('Volume (m^3)')
plt.xlim(10, 23)
plt.ylim(0, 135000)
plt.plot(h1, Vp)
plt.grid()
plt.show()
