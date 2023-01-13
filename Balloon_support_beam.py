import numpy as np
import matplotlib.pyplot as plt
import math
#Assumptions: bending due to rod in front does not induce displacement of the secondary rod
#Axial deformations not taken into account
#TODO:include contributions of angles of small elements in the end result for deflection
#TODO: varrying thickness for bending stress condition (maybe look into root bending and uniformly reduce thickness towards the tip)

#Shape outline
a=63
b=3
c=63

n=100
#horizontal_step = 0.5
x_coord=np.linspace(0, 63, n)
y_coord=[]
L=[]
dy=[]
for i in range (len(x_coord)):
    y_coord.append(math.sqrt((c-x_coord[i]**2/a)*b))
for i in range (len(x_coord)-1):
    dy = y_coord[i+1]-y_coord[i]
    dx = x_coord[1]
    L.append(dx)
    L.append(dy)

print(x_coord, y_coord, L)


#L=[10, 1, 10, 1.5, 10, 2, 10, 4, 10, 3] #m, horizontal element, vertical element , h, v ..., from the loose end to the root


p = 0 #Pa
w = 220 #N/m, skin of meter thickness

#E=1
E = 70*10**9 #Pa

b = 0.05 #m, width
h = 0.02 #m, thickness
I = b*h**3/12 #moment of inertia
#I=1

n=len(L) #even number of connections

def uniform_deflections(w, L, E, I, n):
    theta=[]
    v=[]
    for i in range(n):
        theta_max=(w*L[i]**3)/(6*E*I)
        theta.append(theta_max)
        v_max=(w*L[i]**4)/(8*E*I)
        v.append(v_max)
    return theta, v

def bending_deflections(M, L, E, I, n): #due to attachment beam twist
    theta=[]
    v=[]
    for i in range(n-1):
        theta_max=(M[i]*L[i+1])/E*I
        theta.append(theta_max)
        v_max=theta_max*L[i]
        v.append(v_max)
    theta.append(0)
    v.append(0)
    return theta, v

def endpoint_bendings(w, L, n):

    M_0 = 0
    M = []
    for i in range(n):
        M_end = L[i]**2 * w * 0.5 + M_0
        M.append(M_end)
        M_0 = M_end
    return M


M=endpoint_bendings(w, L, n)

theta_ben, v_ben=bending_deflections(M, L, E, I, n)

theta_unif, v_unif = uniform_deflections(w, L, E, I, n)

print("Endpoint bendings, from loose to fixed end:",endpoint_bendings(w, L, n))
#print("Bending and uniform loading twising angles: ", theta_ben, theta_unif)
#print("Bending and uniform loading deflections: ", v_ben, v_unif)

#point deflections:
v_ben_x=v_ben[0::2]
v_ben_y=v_ben[1::2]

v_unif_x=v_unif[0::2]
v_unif_y=v_unif[1::2]

defl_x=[]
defl_y=[]
for i in range (int(n/2)):
    deflection_total_x=sum(v_ben_x[i:(n)])+sum(v_unif_x[i:(n)])
    defl_x.append(deflection_total_x)
    defl_x.append(0)

    defl_y.append(0)
    deflection_total_y=sum(v_ben_y[i:(n)])+sum(v_unif_y[i:(n)])
    defl_y.append(deflection_total_y)


defl_x.append(0)
defl_y.append(0)
print("defl_x[::-1]:", defl_x[::-1])
print("defl_y[::-1]: ", defl_y[::-1])

L_x = L[0::2]
L_y = L[1::2]
x=[]
y=[]
for i in range (len(L_x)+1):
    x_sum=sum(L_x[0:i])
    y_sum=sum(L_y[0:i])+y_coord[0]
    x.append(x_sum)
    y.append(y_sum)
    if i != 0:
        x.append(x_sum)
    if i != (len(L_x)):
        y.append(y_sum)


#print(x, y)


plt.plot(x_coord, y_coord)

plt.plot(np.add(np.array(x), np.array(defl_x[::-1])), np.add(np.array(y), np.array(defl_y[::-1])))
plt.plot(x, y)
plt.xlim([-1, 70])
plt.ylim(min(y_coord)-1, max(y_coord)+1)
plt.show()
print("x", x)
#print(y, defl_x, defl_x[::-1], np.subtract(np.array(y), np.array(defl_x)))