import math
import matplotlib.pyplot as plt
from Functions import ISA

mass = 1000
dt = 0.1



# print(ISA(10))

def relative_density(rho_ref,T_ref,T2,P_ref=1,P2=1):

    return rho_ref * (T2/T_ref) * (P2/P_ref)


def calc_DlDv(rho_gas,rho_atm):
    DlDv = rho_atm * (1-(rho_gas/rho_atm))

    return -DlDv


h_range = [h for h in range(0,45000,100)]

DlDv_list = list()

for h in h_range:
    pass
    atm_params = ISA(h)
    hydrogen_density = relative_density(0.0841,288.15,
                                        atm_params[0])
    # print(hydrogen_density)
    # raise "Biem"
    DlDv_list.append(calc_DlDv(atm_params[2], hydrogen_density))




plt.plot(h_range,DlDv_list)
plt.xlabel("Height [m]")
plt.ylabel("Lifted mass per volume of gas [kg/m^3]")
plt.show()