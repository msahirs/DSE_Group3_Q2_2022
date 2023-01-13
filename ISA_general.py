'''ISA temperature, pressure and density calculating function'''
import numpy as np


def ISA(h):
    g0 = 9.80665
    R = 287.
    T0 = 288.15
    p0 = 101325.
    h0 = 0.
    e = 2.718281828459045

    if h > 86000:
        print("I can only do altitudes up to 86000 m")

    h1 = min(h, 11000.0)
    a1 = -0.0065
    T1 = T0 + a1 * (h1 - h0)
    p1 = p0 * (T1 / T0) ** (-g0 / (a1 * R))
    rho1 = p1 / (R * T1)
    if h <= 11000:
        Temp = T1
        p = p1
        rho = rho1
    else:
        h2 = min(h, 20000.0)
        p2 = p1 * e ** (-g0 / (R * T1) * (h2 - h1))
        rho2 = p2 / (R * T1)
        if h <= 20000:
            Temp = T1
            p = p2
            rho = rho2
        else:
            h3 = min(h, 32000.0)
            a3 = 0.001
            T3 = T1 + a3 * (h3 - h2)
            p3 = p2 * (T3 / T1) ** (-g0 / (a3 * R))
            rho3 = p3 / (R * T3)
            if h <= 32000:
                Temp = T3
                p = p3
                rho = rho3
            else:
                h4 = min(h, 47000.0)
                a4 = 0.0028
                T4 = T3 + a4 * (h4 - h3)
                p4 = p3 * (T4 / T3) ** (-g0 / (a4 * R))
                rho4 = p4 / (R * T4)
                if h <= 47000:
                    Temp = T4
                    p = p4
                    rho = rho4
                else:
                    h5 = min(h, 51000.0)
                    p5 = p4 * e ** (-g0 / (R * T4) * (h5 - h4))
                    rho5 = p5 / (R * T4)
                    if h <= 51000:
                        p = p5
                        rho = rho5
                    else:
                        h6 = min(h, 71000.0)
                        a6 = -0.0028
                        T6 = T4 + a6 * (h6 - h5)
                        p6 = p5 * (T6 / T4) ** (-g0 / (a6 * R))
                        rho6 = p6 / (R * T6)
                        if h <= 71000:
                            Temp = T6
                            p = p6
                            rho = rho6
                        else:
                            h7 = min(h, 86000.0)
                            a7 = -0.002
                            T7 = T6 + a7 * (h7 - h6)
                            p7 = p6 * (T7 / T6) ** (-g0 / (a7 * R))
                            rho7 = p7 / (R * T7)
                            if h <= 86000:
                                Temp = T7
                                p = p7
                                rho = rho7
    return Temp, p, rho


def ISA_from_everything(altitude):
    # Function to get a list or array to run in the ISA function
    # Returns either floats or lists
    if altitude.__class__ == int or altitude.__class__ == float:
        T, p, rho = ISA(altitude)
        return T, p, rho
    else:
        altitude = list(altitude)
        Tlst = []
        plst = []
        rholst = []
        for alt in altitude:
            T, p, rho = ISA(alt)
            Tlst.append(T)
            plst.append(p)
            rholst.append(rho)
        return Tlst, plst, rholst
