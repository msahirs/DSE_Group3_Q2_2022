#UHMWPE Structural Calculations

#Import stuff
import math
import numpy as np
import matplotlib.pyplot as plt



#Variables
stress_ult = 1100000000 #[Pa]
safety_factor = 4 #dimensionless
material_density = 980 #kg / m^3
gravitational_constant = 9.80665 #m/s^2
wire_length = 20000 #[m]
Fd = 10000 #[N], total drag working on the tether
wire_electric_weight = 500 #[kg]
i =1

#Simple calculations
F_mass_electric = wire_electric_weight * gravitational_constant
wire_stress_design =  stress_ult / safety_factor #Design stress of the tether
form_var_ww = gravitational_constant**2*wire_length**2*material_density**2 #For conciseness in the Area formula

#Calculations
Area_wire = (Fd)/(math.sqrt(wire_stress_design**2 - form_var_ww)) #m2
Area_wire_cm = Area_wire * 10000 #[cm^2]
Volume_wire =  Area_wire * wire_length #[m^3 ]
Mass_wire = Volume_wire * material_density #[kg]
F_mass_wire = Mass_wire*gravitational_constant

wire_stress_actual = math.sqrt((F_mass_electric+F_mass_wire)**2 + Fd**2) / Area_wire
wire_stress_wiremass = F_mass_wire / Area_wire
wire_stress_electricmass = F_mass_electric / Area_wire


while wire_stress_actual > wire_stress_design:
    Area_wire = Area_wire + 0.1*10**-6
    Volume_wire =  Area_wire * wire_length #[m^3 ]
    Mass_wire = Volume_wire * material_density #[kg]
    F_mass_wire = Mass_wire*gravitational_constant
    wire_stress_actual = math.sqrt((F_mass_electric+F_mass_wire)**2 + Fd**2) / Area_wire
    Area_wire_cm = Area_wire *10000
print("Wire cross section in mm2: ",round(Area_wire*10**6, 2)," The mass of the wire in kg is: ", round(Mass_wire, 2)) #prints the wire area in mm^2

