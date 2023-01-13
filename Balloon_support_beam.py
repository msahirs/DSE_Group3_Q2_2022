import numpy as np

L=[0.1, 0.075] #m, horizontal element, vertical element , h, v ...


p = 0 #Pa
w = [4000, 0] #N/m

E=1
#E = 70*10**9 #Pa

b = 0.05 #m, width
h = 0.05 #m, thickness
#I = b*h**3/12 #moment of inertia
I=1

n=2 #even number of connections

def uniform_deflections(w, L, E, I, n):
    theta=[]
    v=[]
    for i in range(n):
        theta_max=(w[i]*L[i]**3)/(6*E*I)
        theta.append(theta_max)
        v_max=(w[i]*L[i]**4)/(8*E*I)
        v.append(v_max)
    return theta, v

def bending_deflections(M, L, E, I, n): #due to beam before
    theta=[0]
    v=[0]
    for i in range(n-1):
        theta_max=(M[i]*L[i+1])/E*I
        theta.append(theta_max)
        v_max=(M[i]*L[i]*L[i+1])/(2*E*I)
        v.append(v_max)
    return theta, v

def endpoint_bendings(w, L, n, M_initial):

    M = [0]
    r=int(n/2)
    for i in range(r):
        M_v = L[i]**2 * w[i] * 0.5 + M_initial
        M.append(M_v)
        M_h = L[i+1]**2 * w[i] * 0.5 + M_v
        M_initial=M_h
        M.append(M_h)
    return M

M_initial = 0
M=endpoint_bendings(w, L, n, M_initial)

theta_ben, v_ben=bending_deflections(M, L, E, I, n)

theta_unif, v_unif = uniform_deflections(w, L, E, I, n)

print(endpoint_bendings(w, L, n, M_initial))

print(theta_ben, theta_unif)
print(v_ben, v_unif)

