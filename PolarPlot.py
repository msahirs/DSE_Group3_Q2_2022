import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve
import Corona_discharge_losses_calculator
import Wire_structure_calculations

A_wire_electric = Corona_discharge_losses_calculator.Area_wire #Single stand wire thickness necessary for power transmission [cm2]
A_wire_struc    = Wire_structure_calculations.Area_wire_cm  #wire thickness necessary to carry loads

x = symbols('x')

eq_r1 = np.pi*x**2-A_wire_electric
r1 = solve(eq_r1)[1]
print(r1)

eq_r2 = (np.pi*x**2)-(np.pi*r1**2) - A_wire_struc
r2 = solve(eq_r2)[1]
print(r2)

eq_r3 = (np.pi*x**2)-(np.pi*r2**2) - A_wire_electric
r3 = solve(eq_r3)[1]
print(r3)

ins_thickness = r2-r1

theta = np.arange(0, 360, 0.01)
r1_list = [r1]*len(theta)
r2_list = [r2]*len(theta)
r3_list = [r3]*len(theta)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta, r1_list)
ax.plot(theta, r2_list)
ax.plot(theta, r3_list)
ax.set_rmax(0.6)
ax.set_rticks([0.15, 0.3, 0.45, 0.6, 0.75])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
ax.grid(True)
#ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()