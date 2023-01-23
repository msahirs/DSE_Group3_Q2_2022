import math
import numpy as np
from Payload import distribution1

def rod_load (F_tension, W_payload, safety_f, tensile_str, density):
    tensile_str_all=(1-safety_f)*tensile_str

    #Initial values
    sigma = 0
    W_rod = 0 #should be around 664
    A = 0.1  # cross sectional area

    while sigma <= tensile_str_all:
        P = (F_tension + W_payload + W_rod) / A
        sigma = P / A
        m_rod = density * L_rod * A
        W_rod = m_rod * g
        A = A - 0.000001

    radius = math.sqrt(A / 3.14)

    return m_rod, radius, A

# Constants
g=9.81
yield_str = 276 * 10 ** 6  # Pa, when is the same for tension and compression
tensile_str=yield_str
compress_str=yield_str
density=2700
L_rod = 3 # m

# Input
F_tension = 24000 # 24000 # N
W_payload = 1500 # N
safety_f = 0.25

m_rod, radius, A = rod_load(F_tension, W_payload, safety_f, tensile_str, density)
#A=3.14*(ro^2-ri^2)
ri=0.03
r0=math.sqrt(A/3.14+ri**2)
print(r0)
print("Aluminium rod: mass ", m_rod,"kg, radius ", radius,"m, cross-sectional area ", A, "m^3")

#Carbon fiber composite
tensile_str=945*10**6 #Pa
density=1500 #only fibre, assume polymer to be similar

m_rod, radius, A = rod_load(F_tension, W_payload, safety_f, tensile_str, density)
#A=3.14*(ro^2-ri^2)
ri=0.03
r0=math.sqrt(A/3.14+ri**2)
print(r0)
print("Carbon composite rod: mass ", m_rod,"kg, radius ", radius,"m, cross-sectional area ", A, "m^3")
"""

# I-Beam calculations
sigma_max = (1-safety_f) * yield_str
tau_max = (1-safety_f) * (yield_str / 2)

length = 29.3
x_down, F_down, F_tot, w = distribution1(4.5, 1000, length, 24)

F_0 = 0.01* F_down
M_0 = F_down * length - 1.4* F_down * x_down

print("Downwards force is:", F_down)
print("Force and moment at hinge are:", F_0, M_0)

tau_lim, sigma_lim, d = 0, 0, 0
t = 0.1

while tau_lim <= tau_max and sigma_lim <= sigma_max:
    d = 100 * t
    tau_lim = 9/16 * F_0 / (t*d)
    sigma_lim = 3/8 * M_0 / (t*d*d)
    t = t - 0.0000001


A = 4 * d * t
W_I = A * length * 2700

print(t, d, A, W_I)
print(tau_lim, sigma_lim)
"""