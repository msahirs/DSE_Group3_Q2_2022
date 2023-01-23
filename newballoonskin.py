import math as m

Areasolarpanels = 2665 # [m]
r_solarpanels = m.sqrt(Areasolarpanels/m.pi)
V_h = 50556.925890248676 # [m^3]
d_P_gas = 108.57619006743589 # [N/m^2]
Excesslift = 6000 # N
Lift = 56241.137749999994 # N
gasbags = 12
admissiblestress=250000000

r = m.sqrt(Areasolarpanels/m.pi)
#r = (1+(1/4.5)) * r_solarpanels

c = ((4*V_h)/(4.19))**(1/3)
a = (1/4) * c
e = m.sqrt(1-((a**2)/(c**2)))
A = 2 * m.pi * (c**2) + m.pi * (a**2) / e * m.log10((1+e)/(1-e))

thickness_skin = d_P_gas * c / (2*admissiblestress) * 1.2

h = (2*a)
width = (2*c)

print("Diameter solar panels", r*2)
print("Width",width)
print("Height",h)

V_skinfibre = thickness_skin *A

density_fibre = 970 # [kg /m3]

mass_skinfibre = V_skinfibre * density_fibre

#t_latex = 0.051 * (10**-3) / 60
t_latex = 1 * (10**-6)
print("Thickness PDVC", t_latex)
print("Thickness fibre", thickness_skin)
print("Total thickness", t_latex+thickness_skin)
v_skinlatex = A * t_latex

density_skinlatex = 1600 # https://omnexus.specialchem.com/polymer-properties/properties/density

mass_skin_latex = v_skinlatex * density_skinlatex

area_gasbags = gasbags * 0.5 * m.pi * c * a

mass_gasbags = area_gasbags * ((t_latex * density_skinlatex) + (thickness_skin*density_fibre))

mass_gasbags_latex = area_gasbags * t_latex * density_skinlatex
mass_gasbags_fibre = area_gasbags * thickness_skin * density_fibre

masslatex = mass_skin_latex + mass_gasbags_latex
massfibre = mass_gasbags_fibre + mass_skinfibre
total_mass = mass_gasbags + mass_skin_latex + mass_skinfibre

print("Mass PDVC", masslatex)
print("Mass fibre", massfibre)
print("Mass total", total_mass)