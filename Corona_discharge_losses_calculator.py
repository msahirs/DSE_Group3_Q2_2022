#Corona losses calculation file
#Source: http://large.stanford.edu/courses/2010/ph240/harting1/
import math
import numpy as np
import matplotlib.pyplot as plt

#Variables
P_design =  1000000  #[W] Power to be transmitted
k0 = 241    #fixed constant
g0 = 21.1   #[KV/cm] Disruptive Gradient in Air
kd = 0.2      #air density factor
a  = 1    #[cm] effective(?) radius of conductor
d  = 5000   #[cm] Conductor Spacing
f  = 0    #50000        #[Hz] Frequency
ki = 0.95   #Wire irregularity factor
#V0 = 442     #[KV] Line voltage to neutral
DCV = g0*ki*a*kd*np.log(d/a) #KV
print("The DCV is: ", DCV)

#V_design = np.arange(10, 200, 0.5)
V_design = 130 #DCV   #FOR CALCULATING LOSSES AT DIFFERENT VOLTAGES, Change value

P_loss = (k0/kd)*(f+25)*math.sqrt(a/d)*(V_design-g0*ki*a*kd*np.log(d/a))**2*10**-5
Amp_wire = P_design / (1000*V_design) #A

#************* Ohmic Resistance / conventional resistance losses ************

#Variables
R_al = 2.65*10**-6 #[Ohm/cm] Resistance
#Area_wire = 0.4         #[cm^2] Surface area of wire
Rho = 0.0027       #{kg/cm^3} Density
L_wire = 2100000#[cm] Length of the wire
Amp_load = 4      #amps per mm2 of wire

Area_wire = (Amp_wire / (Amp_load))/100 #cm^2
V_wire = L_wire * (Area_wire)
M_wire = V_wire * Rho #kg
M_wire_total = M_wire * 2
P_loss_corona = P_loss * L_wire/100000

# ******** Inductive losses **********

#Some variables
d_wire = 0.15          #[cm] diameter of wire
L_wire = L_wire     #[cm] length of wire
mu = 1              #permeability, 1 for non magnetic materials

#Inductance calculation
x = math.sqrt(1+(d_wire/(2*L_wire))**2) #substitute x in de inductance formula for readability
inductance = 2*L_wire*(np.log(((2*L_wire)/d_wire)*(1+x))-x+mu/4+d_wire/(2*L_wire)) #Calculates inductance in nanohenry

#print(inductance) #print inductance in nanohenries
R_wire_inductance = 2*math.pi*f*(inductance*10**-9) #Calculates impedance due to inductance in ohms

R_wire_ohmic = (R_al/Area_wire) * L_wire

P_loss_ohmic = (R_wire_ohmic*Amp_wire**2)/1000
P_loss_inductance = (R_wire_inductance*Amp_wire**2)/1000
P_loss_total = P_loss_corona + P_loss_ohmic + P_loss_inductance
Loss_percent = (P_loss_total / (P_design/1000)) * 100

#print(min(P_loss_total))

#Plots the Voltage vs Power loss curve


fig, ax = plt.subplots()
ax.plot(f, (P_loss_inductance))
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Loss [KW]')
#ax.set_title('Line Graph')
#plt.show()
#print(Area_wire)




#print("With a design voltage of ", round(V_design, 2), "kilovolts:")
#print("The corona inception voltage is ", np.round(DCV, 2), "kilovolts.")
#print("Your power loss due to corona is: ", np.round(P_loss, 2), "kilowatts per kilometer.")
print("Your power loss due to ohmic losses is: ", np.round(P_loss_ohmic, 2), "kilowatts.")
#print("Your power loss due to inductive losses is: ", np.round(P_loss_inductance, 2), "kilowatts.")
#print("Total loss is ", np.round(Loss_percent, 3), "percent of the total power to be transmitted.")
print("The wire cross section is: ", np.round(Area_wire, 4), "square centimeters with a weight of ", np.round(M_wire_total, 2), "kilograms.")

