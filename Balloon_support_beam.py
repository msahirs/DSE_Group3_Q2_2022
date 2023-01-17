import numpy as np
import matplotlib.pyplot as plt
import math
#Assumptions: bending due to rod in front does not induce displacement of the secondary rod
#Axial deformations not taken into account
#TODO:include contributions of angles of small elements in the end result for deflection
#TODO: varrying thickness for bending stress condition (maybe look into root bending and uniformly reduce thickness towards the tip)

#Shape outline

def create_outline():
    a=39.3
    b=0.75
    c=39.3

    x_coord=np.linspace(0, 39.3, 100)
    y_coord=[]
    L=[]
    dy=[]

    for i in range (len(x_coord)):
        y_coord.append(math.sqrt((c-x_coord[i]**2/a)*b))

    for i in range (len(x_coord)-1):
        dy = y_coord[i+1]-y_coord[i]
        dx = x_coord[1]
        L.append(abs(dx))
        L.append(abs(dy))

    print("x_coord: ", x_coord, "y_coord: ", y_coord)
    print("L", L)
    return x_coord, y_coord, L




def uniform_deflections(w, L, E, I):
    theta=[]
    v=[]
    theta.append(0)
    v.append(0)
    for i in range(len(L)):
        theta_max=(w*L[i]**3)/(6*E*I[i])
        theta.append(theta_max)
        v_max=(w*L[i]**4)/(8*E*I[i])
        v.append(v_max)
    return theta, v

def bending_deflections(M, L, E, I): #due to attachment beam twist
    theta=[]
    v=[]
    theta.append(0)
    v.append(0)
    v.append(0)
    for i in range(1, len(L)):
        theta_max=(M[i]*L[i-1])/E*I[i-1]
        theta.append(theta_max)
        v_max=theta_max*L[i]
        v.append(v_max)
    theta.append(0)
    #theta.append((M[len(L)]*L[len(L)-1])/(E*I[len(L)-1]))

    return theta, v

def endpoint_bendings(w,L):
    M=[]
    for i in range (len(L)):
        M.append(sum(L[i::2])**2*w*0.5+sum(L[i+1::2])**2*w*0.5)
    return M

'''
def endpoint_bendings(w, L):

    M_0 = 0
    L=L[::-1]
    M = []
    M.append(0)
    for i in range(len(L)):
        M_end = L[i]**2 * w * 0.5 + M_0
        M.append(M_end)
        M_0 = M_end
    M=M[::-1]
    return M
'''

x_coord, y_coord, L = create_outline()

p = 0 #Pa
w = 127 #N/m, skin of meter thickness

nr=10

h1=0.01
h2=0.006

b1=0.006
b2=0.002
I = []
for i in range(len(L)):
    h = h1 - h2*i/(len(L)) #m, thickness
    b = b1 - b2*i/(len(L))  # m, width
    Inertia = b * h ** 3 / 12  # moment of inertia
    I.append(Inertia)

#print("I=", I)
#E=1
E = 70*10**9 #Pa

print(h, b)
#Weight
a=h1*b1
b=(h1-h2)*(b1-b2)
l=sum(L)
V=(a+b)*l/2
rho = 2700 #Aluminium
mass=rho*V

print("MASS:", mass)
#I=1


M=endpoint_bendings(w, L)

theta_ben, v_ben=bending_deflections(M, L, E, I)

theta_unif, v_unif = uniform_deflections(w, L, E, I)

print("Endpoint bendings, from fixed to loose end:",endpoint_bendings(w, L))
#print("Bending and uniform loading twising angles: ", theta_ben, theta_unif)
print("Bending and uniform loading deflections: ", v_ben, v_unif)

#point deflections:
v_ben_x=v_ben[0::2]
v_ben_y=v_ben[1::2]

v_unif_x=v_unif[0::2]
v_unif_y=v_unif[1::2]

defl_x=[]
defl_y=[]



#print("v_unif_x:", v_unif_x)
#print("v_unif_x[::-1]",v_unif_x[::-1])
v_unif_x=v_unif_x[::-1]
v_ben_x=v_ben_x[::-1]

for i in range (int(len(L)/2)):
    deflection_total_x=sum(v_ben_x[i:len(v_ben_x)])+sum(v_unif_x[i:len(v_unif_x)])
    defl_x.append(deflection_total_x)
    deflection_total_x = deflection_total_x - sum(v_ben_x[0:i])
    defl_x.append(deflection_total_x)
defl_x.append(0)

defl_y.append(sum(v_ben_y[0:len(L)])+sum(v_unif_y[0:len(L)]))
for i in range(int(len(L) / 2)-1):
    deflection_total_y=sum(v_ben_y[i:len(v_ben_y)])+sum(v_unif_y[i:len(v_ben_y)])
    defl_y.append(deflection_total_y)
    deflection_total_y = deflection_total_y - sum(v_ben_y[0:i])
    defl_y.append(deflection_total_y)

deflection_total_y = sum(v_ben_y[(len(v_ben_y)):len(v_ben_y)]) + sum(v_unif_y[(len(v_ben_y)):len(v_ben_y)])
defl_y.append(deflection_total_y)
defl_y.append(0)


#defl_y.append(0)


defl_x=defl_x[::-1]
defl_y=defl_y[::-1]

#print("defl_x:", defl_x)
#print("defl_y: ", defl_y)

L_x = L[0::2]
L_y = L[1::2]
x=[]
y=[]
for i in range (len(L_x)+1):
    x_sum=sum(L_x[0:i])
    y_sum=-sum(L_y[0:i])+y_coord[0]
    x.append(x_sum)
    y.append(y_sum)
    if i != 0:
        x.append(x_sum)
    if i != (len(L_x)):
        y.append(y_sum)


#print(x, y)


plt.plot(x_coord, y_coord)

plt.plot(np.add(np.array(x), np.array(defl_x)), np.add(np.array(y), np.array(defl_y)))
plt.plot(x, y)
#plt.xlim([-1, 70])
#plt.ylim(min(y_coord)-1, max(y_coord)+1)
plt.show()
#print("x", x)
#print(y, defl_x, defl_x[::-1], np.subtract(np.array(y), np.array(defl_x)))