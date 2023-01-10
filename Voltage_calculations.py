import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve
import Corona_discharge_losses_calculator
import Wire_structure_calculations
import PolarPlot

r1 = PolarPlot.r1
r2 = PolarPlot.r2
r3 = PolarPlot.r3

thick_core = r1
thick_insu = r2-r1
thick_outer = r3-r2

V_breakdown = 900 #[KV / cm]
f_safety = 2
V_allowed = (thick_insu*(V_breakdown/f_safety))

print(V_allowed)
