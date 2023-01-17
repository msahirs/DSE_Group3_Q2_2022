import math as m

Areasolarpanels = 2726 # [m]
r_solarpanels = m.sqrt(Areasolarpanels/m.pi)
V_h = 35448.8825891154 # [m^3]
d_P_gas = 127.12485479797665 # [N/m^2]
Excesslift = 2000 # N
Lift = 44965.13311704596 # N
gasbags = int(Lift/Excesslift) + 1
admissiblestress=250000000
print(gasbags)

r = (1+(1/3)) * r_solarpanels

thickness_skin = d_P_gas * r / (2*admissiblestress)

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

v_skinlatex = A * t_latex

density_skinlatex = 1.2 * 68.886

mass_skin_latex = v_skinlatex * density_skinlatex
print(h)
print(width)
print(mass_skin_latex)
print(mass_skinfibre)

area_gasbags = gasbags * 2 * m.pi * c * b

mass_gasbags = area_gasbags * ((t_latex * density_skinlatex) + (thickness_skin*density_fibre))

total_mass = mass_gasbags + mass_skin_latex
print(total_mass)