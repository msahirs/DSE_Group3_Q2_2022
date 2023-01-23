import math
import numpy as np
from Payload import distribution1, distribution2

# Input
length_top = 29.1
length_bottom = 72.2/2 # Calculate
beams = 12
bottom_loading = 13.46 # Calculate
n = 1000
compression_factor = 2 # Edit
d_bottom = 2
d_top = 4

def moi(dim):
    I = 2*(1/3*dim[0]*dim[1] + dim[2]*dim[3])*dim[1]*dim[1]
    A = 2*dim[0]*dim[1] + 2*dim[2]*dim[3]
    return I,A

# Constants
safety_f = 0.2
top_loading = 6
yield_str = 276 * 10 ** 6  # Pa
density = 2700
g = 9.81

# Constraints
sigma_max = (1-safety_f) * yield_str
tau_max = (1-safety_f) * (yield_str / 2)


# Top Beam
x_solar, F_solar, F_tot, w_top = distribution1(top_loading, n, length_top, beams)
F_0 = abs(F_solar - compression_factor * F_solar)
M_0 = abs(F_solar * x_solar - compression_factor * F_solar * (1/2 * x_solar))
M_max = 0.25 * F_solar * x_solar

print("Downwards force is:", F_solar)
print("Force and moment at centre are:", F_0, M_0)

tau_lim, sigma_lim = 0, 0
d, t = 0.1, 0.1
dim = [t,d,t,d]

while tau_lim <= tau_max and sigma_lim <= sigma_max:
    d = 25 * t
    dim = [t, 2 * d, 2 * t, d]
    tau_lim = 9/16 * F_0 / (t*d)
    sigma_lim = dim[1] * M_max / moi(dim)[0]
    t = t - 0.0000001

W_top = moi(dim)[1] * length_top * 2700

print("Weight of top beam will be:", W_top)
print(moi(dim)[1])
print(tau_lim, sigma_lim)


# Bottom Beam
x_h, F_h, F_tot, w_top = distribution2(bottom_loading, n, length_bottom, beams)
F_0 = abs(F_h - compression_factor * F_solar)
M_0 = abs(F_h * x_h - compression_factor * F_solar * (length_top + d_bottom))

print("\nUpwards force is:", F_h, "acting at", x_h, "causing a moment of", x_h*F_h)
print("Force and moment at centre are:", F_0, M_0)

tau_lim, sigma_lim  = 0, 0
t, d = 0.1, 0.1
dim = [t,d,t,d]

while tau_lim <= tau_max and sigma_lim <= sigma_max:
    d = 25 * t
    dim = [t, 2 * d, 2 * t, d]
    tau_lim = 9/16 * F_0 / (t*d)
    sigma_lim = dim[1] * M_0 / moi(dim)[0]
    t = t - 0.0000001

W_bottom = moi(dim)[1] * length_top * 2700

print("Weight of bottom beam will be:", W_bottom)
print(tau_lim, sigma_lim)


print("\nTotal weight per rib:", W_bottom + W_top)
print("Total weight of top structure:", (W_bottom + W_top) * beams)

print(moi(dim)[0])