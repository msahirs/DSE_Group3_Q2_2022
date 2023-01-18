import numpy as np
import matplotlib.pyplot as plt
import math
#Assumptions: bending due to rod in front does not induce displacement of the secondary rod
#Axial deformations not taken into account
#TODO:include contributions of angles of small elements in the end result for deflection
#TODO: varrying thickness for bending stress condition (maybe look into root bending and uniformly reduce thickness towards the tip)

#Shape outline

def create_outline(points, xr):
    a=36.82
    b=2.387
    c=36.82

    x_coord=np.linspace(0, a, points)
    y_coord=[]

    L=[]
    dy=[]

    x=[]
    y=[]


    for i in range (len(x_coord)):
        y_coord.append(math.sqrt((c-x_coord[i]**2/a)*b))

    #x.append(x_coord[0])
    #y.append(y_coord[0])
    for i in range (len(x_coord)-1):
        dy = y_coord[i+1]-y_coord[i]
        dx = x_coord[1]
        L.append(abs(dx))
        L.append(abs(dy))
        if dx*i<xr:
            index=i



        #x.append(x_coord[i]+dx)
        #y.append(y_coord[i]+dy)

    #print("x_coord: ", x_coord, "y_coord: ", y_coord)
    #print("L", L)
    return x_coord, y_coord, L, index

def uniform_deflections(w_tot, L, E, I, F, index):
    theta=[]
    v=[]
    theta.append(0)
    v.append(0)
    #print(w_tot, L)
    for i in range(len(L)):
        if i != (index*2+1):
            theta_max=(w_tot[i]*L[i]**3)/(6*E*I[i])
            theta.append(theta_max)
            v_max=(w_tot[i]*L[i]**4)/(8*E*I[i])
            v.append(v_max)
        #if i == (index*2+1):
        #    theta_max = ((w - (F/L[i]))* L[i] ** 3) / (6 * E * I[i])
        #    theta.append(theta_max)
        #    v_max = ((w - (F/L[i])) * L[i] ** 4) / (8 * E * I[i])
        #    v.append(v_max)
    return theta, v

def bending_deflections(M, L, E, I): #due to attachment beam twist
    theta=[]
    v=[]
    theta.append(0)
    v.append(0)
    v.append(0)
    for i in range(1, len(L)):
        theta_max=(M[i]*L[i-1])/(E*I[i-1])
        theta.append(theta_max)
        v_max=theta_max*L[i]
        v.append(v_max)
    theta.append(0)
    #theta.append((M[len(L)]*L[len(L)-1])/(E*I[len(L)-1]))

    return theta, v

def endpoint_bendings(L, w_lin, index, F):
    M=[]
    #print(L, w_lin, index, F)
    for i in range (len(L)):

        M_lin=sum(L[i::2])**2*(w_lin[len(L)-1]-w_lin[i])/2*(2/3)+sum(L[i+1::2])**2*(w_lin[len(L)-1]-w_lin[i])/2*(2/3)
        if i<index:
            M_F=sum(L[i:index])/2*F
        else:
            M_F=0
        M.append(M_lin-M_F)

        #M.append(sum(L[i::2])**2*w*0.5+sum(L[i+1::2])**2*w*0.5)


        #print(i, L[i::2], sum(L[i::2]))
        #print(i, L[i+1::2], sum(L[i+1::2]))
    M.append(0)
    return M

def load_vector(index, w_final, F, L):
    w_tot=[]
    w_lin=[]
    for i in range (len(L)):
        load=w_final*sum(L[0:i])/sum(L)
        w_lin.append(load)
        if i == (index*2)+1:
            load=load-F/L[index*2+1]
        w_tot.append(load)
    return w_tot, w_lin

def create_beam(L):
    h1=0.02
    h2=0.005

    b1=0.01
    b2=0.005
    I = []
    for i in range(len(L)):
        h = h1 - h2*i/(len(L)) #m, thickness
        b = b1 - b2*i/(len(L))  # m, width
        Inertia = b * h ** 3 / 12  # moment of inertia
        I.append(Inertia)
    I=I[::-1]

    # Weight
    a = h1 * b1
    b = (h1 - h2) * (b1 - b2)
    l = sum(L)
    V = (a + b) * l / 2
    rho = 2700  # Aluminium
    mass = rho * V
    print("MASS:", mass)
    return I

points=500
while points==500:
    E = 70*10**9 #Pa


    #points=10 #no of points dividing the curve, NOT TOTAL POINTS
    xr=60 #x location of compression rod
    x_coord, y_coord, L, index = create_outline(points, xr)
    I=create_beam(L)
    F=2700
    w_final=100

    w_tot, w_lin = load_vector(index, w_final, F, L)

    M=endpoint_bendings(L, w_lin, index, F)

    theta_ben, v_ben = bending_deflections(M, L, E, I)

    theta_unif, v_unif = uniform_deflections(w_tot, L, E, I, F, index)

    #print("Endpoint bendings, from fixed to loose end:",M)
    #print("Bending and uniform loading twising angles: ", theta_ben, theta_unif)
    #print("Bending loading deflections: ", v_ben)
    #print("Uniform loading deflections: ", v_unif)

    #point deflections:
    v_ben_x=v_ben[0::2]
    v_ben_y=v_ben[1::2]

    v_unif_x=v_unif[0::2]
    v_unif_y=v_unif[1::2]

    defl_x=[]
    defl_y=[]

    for i in range (int(len(L)/2)):
        deflection_total_x=sum(v_ben_x[i:len(v_ben_x)])+sum(v_unif_x[i:len(v_unif_x)])
        #print(i, sum(v_ben_x[i:len(v_ben_x)]), sum(v_unif_x[i:len(v_unif_x)]))
        defl_x.append(deflection_total_x)
        deflection_total_x = deflection_total_x - v_unif_x[i] - v_ben_x[i]
        defl_x.append(deflection_total_x)
    defl_x.append(0)

    for i in range(int(len(L) / 2)):
        deflection_total_y=sum(v_ben_y[i:len(v_ben_y)])+sum(v_unif_y[i:len(v_ben_y)])
        defl_y.append(deflection_total_y)
        #deflection_total_y = deflection_total_y - sum(v_ben_y[0:i])
        defl_y.append(deflection_total_y)
    defl_y.append(0)

    defl_x=defl_x[::-1]
    defl_y=defl_y[::-1]

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


    plt.plot(x_coord, y_coord, label="initial shape")

    plt.plot(np.add(np.array(x), np.array(defl_x)), np.add(np.array(y), np.array(defl_y)), label="final shape")
    plt.plot(x, y)
    #plt.xlim([-1, 70])
    #plt.ylim(min(y_coord)-1, max(y_coord)+1)
    plt.legend(loc="upper left")
    plt.xlabel("x-axis, [m]")
    plt.ylabel("y-axis, [m]")
    #plt.show()
    plt.savefig('plot1' + str(points) +'png')
    plt.show()

    points=points*2