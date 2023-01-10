r=2
t=0.015
E=68*10**9
v=0.33
rho=2712
p=(83+12+25+220+127+1200+32)*9.81/(3.14*r**2)
#Flexural rigidity
D=E*t**3/(12*(1-v**2))

#Displacement
w_max=p*r**4/(64*D)

#Stress at the centre
sigma_max=3*(1+v)*p*r**2/(8*t**2)

#Mass
M=rho*(3.14*r**2*t)

print("max deflection:", w_max,"max stress:", sigma_max, "mass", M)
#design yield stress for aluminium
