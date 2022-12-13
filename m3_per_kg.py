from Functions import ISA
import numpy as np
from math import sqrt, pi
import matplotlib.pyplot as plt

# Constants:
R = 8.31446261815324 # J/K/mol
g0 = 9.8

# Hydrogen:
MH2 = 2 * 1.00784 # u = g/mol
RH2 = R/MH2 # J/K/mol / [g/mol] = J*mol/K/mol/g = J/K/g = kJ/K.kg


# Inputs:
h = range(15000,30100,100) # m
m = 1 # kg
A = 4000 # m2
panelmass = 0.48 # kg/m2

def hydrogenvolume(h,m):
    # Hydrogen volume calculations:
    T, p, rho = ISA(h)
    rhoH = p/RH2/T # [J/m3] / [kJ/kg.K] / [K] = [J/m3].[kg] / [kJ] = [kg/m3]/[J/kJ] = [g/m3]
    rhoH = rhoH/1000
    # print(rhoH)

    rhodif = rho-rhoH # [kg/m3], Difference in weight between air and hydrogen at altitude h
    #L_over_V = rhodif * g0 # [N/m3], lift force per m3 of hydrogen
    V_per_kg = 1/rhodif # [m3/kg]
    print(V_per_kg)

    V_required = V_per_kg * m
    # print(V_required)
    mH_required = V_required * rhoH
    # print(mH_required)
    return rhoH, V_required, mH_required

def torus(V_required, Amin):
    # Torus calculations:
    Ri = sqrt(Amin/pi) # m
    r = sqrt(V_required/(2*pi**2*Ri))
    R = Ri + r
    V = 2*pi**2*r**2*(R)
    while not abs(V-V_required)/V_required < 0.000000001:
        R = R * V/V_required
        r = sqrt(V_required/(2*pi**2*R))
        V = 2*pi**2*r**2*(Ri+r)
    return Ri, r, V

def torus_on_top(V_required, Amin):
    R = sqrt(Amin/pi) # m
    r = sqrt(V_required/(2*pi**2*R))
    return R, r

# htest = 20000 # [m]
# mtest = 6700 # [kg]
# Atest = 4000 # [m2]

# rhotest, Vtest, mHtest = hydrogenvolume(htest,mtest)
# print(Vtest, mHtest)
# Ritest, rtest, Vcheck = torus(Vtest, Atest)
# print(Ritest, rtest, 2*(Ritest+2*rtest))
# Afront_test = pi*4*rtest**2 + (Ritest + rtest)*4*rtest
# print(Afront_test)

# # Square
# print('square')
# L = sqrt(Atest)
# hsqr = Vtest/Atest
# print(L, hsqr, L*hsqr)

# # Torus with panels on top
# print('top')
# Rtop, rtop = torus_on_top(Vtest, Atest)
# print(Rtop, rtop, 2*Rtop+2*rtop)
# print(pi*4*rtop**2 + (Rtop + rtop)*4*rtop)

# rad = (3*Vtest/4*pi)**(1/3)
# print(rad)
# print(rad**2)
# oppervlak = (3*Vtest/4*pi)#**(2/3)#*pi
# print("Area = {}".format(oppervlak))


# Solar panel mass
# panelm = panelmass*A
# print(panelm)

# # Flying wing wet thumb calculations
# # Assumptions:
# CL = 0.5
# # Assume S equal to the area of the solar panels
# S = A
# hc = 20000
# T20, p20, rho20 = ISA(hc)
# Vc = np.arange(0,100,5)
# L = CL*0.5*rho20*Vc**2*S

rhoHlst = []
rlst = []
Vlst = []

for alt in h:
    rhoH, V_torus, mH_torus = hydrogenvolume(alt,m)
    Ri, r, V = torus(V_torus, A)
    rhoHlst.append(rhoH)
    rlst.append(r)
    Vlst.append(V)

print(h[-1])
print(mH_torus)
print(Vlst[0], Vlst[-1], Vlst[-1]/Vlst[0])
print(rhoHlst[0],rhoHlst[-1])

plt.subplot(221)
plt.plot(h,rlst)
plt.title("Torus radius required for a balloon of {} kg versus altitude".format(m))

plt.subplot(222)
plt.plot(h,rhoHlst)
plt.title("Density of hydrogen at ISA pressure and temperature versus altitude")

plt.subplot(223)
plt.plot(h,Vlst)
plt.yscale('log')
plt.title("Required Volume of hydrogen [m3] versus altitude [m]")

# plt.subplot(224)
# plt.plot(Vc, L)
# plt.title("Generated lift force [N] by a flying with with a lift coefficient of {}\n and surface area of {} m2 at an altitude of {} m".format(CL,S,hc))
plt.show()