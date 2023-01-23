import math as m

Areasolarpanels = 2726 # [m]
r_solarpanels = m.sqrt(Areasolarpanels/m.pi)
V_h = 49518.88738452703 # [m^3]
d_P_gas = 108.57619006743589 # [N/m^2]
Excesslift = 6000 # N
Lift = 55086.390589999995 # N
gasbags = 12
admissiblestress=250000000
print(gasbags)

r = (1+(1/4.5)) * r_solarpanels

thickness_skin = d_P_gas * r / (2*admissiblestress) * 1.2

b = r
c = V_h / (4/3 * m.pi * (b**2))
e = m.sqrt(1-((c**2)/(b**2)))
A = 2 * m.pi * (b**2) + m.pi * (c**2) / e * m.log10((1+e)/(1-e))

h = (2*c)
width = (2*b)

V_skinfibre = thickness_skin *A

density_fibre = 970 # [kg /m3]

mass_skinfibre = V_skinfibre * density_fibre

t_latex = 0.051 * (10**-3)
print(t_latex)
print(thickness_skin)
print(t_latex+thickness_skin)
v_skinlatex = A * t_latex

density_skinlatex = 68.886

mass_skin_latex = v_skinlatex * density_skinlatex
print(h)
print(width)
print(mass_skin_latex)
print(mass_skinfibre)

area_gasbags = gasbags * 0.5 * m.pi * c * b

mass_gasbags = area_gasbags * ((t_latex * density_skinlatex) + (thickness_skin*density_fibre))

mass_gasbags_latex = area_gasbags * t_latex * density_skinlatex
mass_gasbags_fibre = area_gasbags * thickness_skin * density_fibre

masslatex = mass_skin_latex + mass_gasbags_latex
massfibre = mass_gasbags_fibre + mass_skinfibre
print(mass_gasbags)
total_mass = mass_gasbags + mass_skin_latex + mass_skinfibre
print(total_mass)

print(masslatex)
print(massfibre)
