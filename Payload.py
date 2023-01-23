import math as m
import matplotlib.pyplot as plt
import numpy as np

# angleused = 2*m.pi / beams

def distribution1(dis_force, n, length, beams):
    w = []
    w_i = 0
    circum = 2*np.pi*length
    max_width = circum / beams
    x_eq = 2/3 * length
    F_eq = 1/2 * length * max_width * dis_force
    F_tot = dis_force * np.pi * length**2

    for i in range(n):
        w_i = w_i + (dis_force * max_width)/n
        w.append(w_i)

    return x_eq, F_eq, F_tot, w

def distribution2(dis_force, n, length, beams):
    w = []
    w_i = 0
    circum = 2*np.pi*length
    max_width = circum / beams
    x_eq = 0.55 * length
    F_eq = 1/2 * length * max_width * dis_force
    F_tot = dis_force * np.pi * length**2

    for i in range(n):
        w_i = w_i + (dis_force * max_width)/n
        w.append(w_i)

    return x_eq, F_eq, F_tot, w

# print(distribution1(9.75,1000,40,24))

"""
Length = 29.
Fullarea = np.pi * Length**2

density_solarpanels = 0.45
r = m.sqrt(Fullarea/m.pi)\

a = m.sqrt(r**2 + r**2 - (2*r*r*m.cos(angleused)))

b = m.sqrt(r**2 - (a/2)**2 )

d = r-b

percentage = (d+b)/100
b_per = b/percentage / 100
d_per = d/percentage / 100

x1 = np.linspace(0,b_per*r,92)
x2 = np.linspace(b_per*r,r,8)

densitynewtons = 4.5 * 9.81 * (r/100) * 2


m1 = x1 * (a/2/b)
m2 = np.sqrt(r**2-x2**2)

w1 = m1 * densitynewtons

w2 = m2 * densitynewtons

xmax = b
mmax = xmax * (a/2/b)
wmax = mmax * densitynewtons
EqF1mag = wmax*xmax*0.5
print("Equivalent load of the distributed load w1:", EqF1mag)

EqF1loc = (2/3) * b
print("Location of equivalent load of the distributed load w1:", EqF1loc)


r = 29.316150714175198
x21 = 0
x22 = d

int21w2 = densitynewtons * 0.5 * ((x21 * np.sqrt(r**2-x21**2) + (r**2 * m.atan(np.sqrt(r**2-x21**2)))))
int22w2 = densitynewtons * 0.5 * (x22 * np.sqrt(r**2-x22**2) + (r**2 * m.atan(np.sqrt(r**2-x22**2))))
intw2 = (int22w2 - int21w2)


print("Equivalent load of the distributed load w2:", intw2)


loc21w2 = -1/3 * ((r**2-x21**2)**(3/2))
loc22w2 = -1/3 * ((r**2-x22**2)**(3/2))

loc = (loc22w2 - loc21w2) / intw2



locexact =  b +loc
print("Location of equivalent load of the distributed load w2:", locexact)

magnituderesultantforce = intw2 + EqF1mag
print("Magnitude resulting force:", magnituderesultantforce)

locationresultantforce = ((locexact * intw2) + (EqF1loc* EqF1mag))/magnituderesultantforce
print("Location resulting force:", locationresultantforce)

plt.plot(x1, w1, 'r')
plt.plot(x2, w2, 'b')
plt.show()
"""
