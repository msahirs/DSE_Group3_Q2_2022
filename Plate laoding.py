import math
import numpy as np

def comment_out ():
    r=2
    t=0.005
    E=70*10**9
    v=0.33

    # rho=2712 #aluminium
    rho=2700
    p=(83+12+25+220+127+1200+32+500)*9.81/(3.14*r**2)
    #Flexural rigidity
    D=E*t**3/(12*(1-v**2))

    #Displacement
    w_max=p*r**4/(64*D)

    #Stress at the centre
    sigma_max=3*(1+v)*p*r**2/(8*t**2)

    #Mass
    M=rho*(3.14*r**2*t)

    print("Circular and clamped: max deflection:", w_max,"max stress:", sigma_max, "mass", M)
    #design yield stress for aluminium

    #Supported on all corners, square
    b1=4
    b2 = 0
    a3 = b1
    b3 = b2
    b=b1+b2+b2

    p=(83+12+25+220+13.5+1200+32)*9.81/b**2

    #Displacement at the centre, PPPP
    w_max_2 = 0.0262 * p * b1**4 / D
    M_centre=0.0947 * p * b1**2
    #print ("Displacement of a square plate at the centre, PPPP:", w_max_2)


    #Displacement at the centre, SSSS

    w_max_2 = 0.142 * p * b1**4 / (E*t*(2.21+1)) #For square plate only
    M_centre=0.0363 * p * b1**2
    sigma=0.75 * p * b1**2 / (t**2*(1.61+1))
    print ("Displacement of a square plate at the centre, SSSS:", w_max_2, "stress:", sigma, sigma<=(276*10**6), "mass: ", rho*b1*b1*t)


    #Max moment corner segments, CCSS
    M_corner = 0.0269 * p * b2 * b2

    #Max moment at top segment, CSSS
    M_top = 0.0443 * p * a3 * b3
    print("b/a=", b3/a3)

    #print("Moments:", M_centre, M_top, M_corner)

    #print("Mass, square config.:", rho*b**2*t)


#Rod loading
def rod_load (W_panels, W_payload, W_wire, safety_f, tensile_str, compress_str, density):
    g=9.81
    compress_str_all=(1-safety_f)*compress_str
    tensile_str_all=(1-safety_f)*tensile_str
    #Initial values
    sigma_comp=0
    sigma_tens=0

    W_rod = 0 #should be around 664
    A = 1  # cross sectional area

    while sigma_comp <= compress_str_all and sigma_tens <= tensile_str_all:
        L_resultant = W_panels + W_payload + W_wire + W_rod
        w = W_rod / 20.5  # weight per m of rod

        # critical loads
        P1 = (W_panels + 0.5 * w) / A  # compression
        P2 = -(W_panels + 0.5 * w - L_resultant) / A  # tension

        # Critical stresses
        sigma_comp = P1 / A
        sigma_tens = P2 / A

        m_rod = density * 20.5 * A
        W_rod= m_rod * g
        A=A-0.0001

    radius=math.sqrt(A / 3.14)
    return m_rod, radius, A


#Design parameters
g=9.81
W_panels = 1000 * g
W_payload = 1300 * g
W_wire = 2300 * g
safety_f=0.2

#Aluminium parameters
yield_str = 276 * 10 ** 6  # Pa, when is the same for tension and compression
tensile_str=yield_str
compress_str=yield_str
density=2700

m_rod, radius, A = rod_load(W_panels, W_payload, W_wire, safety_f, tensile_str, compress_str, density)
#A=3.14*(ro^2-ri^2)
ri=0.06
r0=math.sqrt(A/3.14+ri**2)
print(r0)
print("Aluminium rod: mass ", m_rod,"kg, radius ", radius,"m, cross-sectional area ", A, "m^3")

#Carbon fiber composite
tensile_str=945*10**6 #Pa
compress_str= 686*10**6 #Pa
density=1900 #only fibre, assume polymer to be similar

m_rod, radius, A = rod_load(W_panels, W_payload, W_wire, safety_f, tensile_str, compress_str, density)
#A=3.14*(ro^2-ri^2)
ri=0.06
r0=math.sqrt(A/3.14+ri**2)
print(r0)
print("Carbon composite rod: mass ", m_rod,"kg, radius ", radius,"m, cross-sectional area ", A, "m^3")

def plate_load ():
    l=5 #m
    #position vector
    X=np.linspace(0, 3, 5)
    Y=np.linspace(0, 3, 5)
    elem_no_in = (len(X)-1)*(len(Y)-2)+(len(Y)-1)*(len(X)-2)
    elem_no_out = (len(X)-1)*(len(Y)-1)
    print(elem_no_in, elem_no_out)

    #loads
    F_payload=1000*9.81
    F_tension=1000*9.81 #will vary
    F_resultant=F_payload+F_tension

    F_element_in=F_payload/elem_no_in
    F_element_out=F_resultant/elem_no_out

    #load acting at nodes
    P_c=-F_element_out #corners, forces act up
    P_s=-F_element_out+F_element_in/2 #sides, forces act up
    P_m=2*F_element_in #middle, forces down

    print(P_c, P_s, P_m)

    #

    return

#plate_load()

comment_out()