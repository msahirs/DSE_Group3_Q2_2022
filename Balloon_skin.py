
import math as m

# V_h and d_p_gas if h = 20000
V_h = 60681 # [m**3]
d_p_gas = 220 # [N/m**2]
atm = 101325
p_atm = d_p_gas / atm
A_s = 2700 # [m**2]

#considering oblate spheroid
#https://www.vcalc.com/wiki/vCalc/Oblate+Spheroid+-+volume
b = 0.5 * m.sqrt(A_s) * 1.5
c = V_h / (4/3 * m.pi * (b**2))
e = m.sqrt(1-((c**2)/(b**2)))
A = 2 * m.pi * (b**2) + m.pi * (c**2) / e * m.log10((1+e)/(1-e))


#considering spheriod
#A_low_cost_alternative_for_satellites-_tethered_ultra-high_altitude_balloons.pdf
r = (V_h/((4/3)*m.pi))**(1/3)
A = 4 * m.pi * r * r
s_a = 250000000 # admissible stress = 1/4 of umpf's yield strength
t = d_p_gas * r / (2*s_a)
v_skin_fibre= t*A

density_skin_fibre = 970 # [kg /m3]# 0.97g/cm3 https://www.sciencedirect.com/topics/chemistry/ultra-high-molecular-weight-polyethylene

m_skin_fibre = v_skin_fibre * density_skin_fibre

t_latex = 0.051 * (10**-3)

v_skin_latex = A * t_latex

density_skin_latex = 68.886

m_skin_latex = v_skin_latex * density_skin_latex


print(m_skin_latex)
print(m_skin_fibre)


#P = 5.5
#A_m = A * 10**4
#time = 24*60*60
#P_d = 101325
#V_g = 1000
#f = 10**(-8)
#thickness = (P*A_m*time*P_d)/(V_g*f)
#print(thickness)

P = 0.4
A_m = A * 10**4
time = 60
P_d = 220/101325
V_g = (1000/24/60)
f = 10**(6)
thickness = (P*A_m*time*P_d)/(V_g*f)
#print(thickness)