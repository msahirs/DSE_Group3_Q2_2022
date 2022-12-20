import math
import matplotlib.pyplot as plt
from Functions import ISA
from scipy.interpolate import UnivariateSpline
import numpy as np

mass = 1000
dt = 0.1

plt.rcParams.update({'font.size': 15, 'xtick.labelsize' : 11, 'ytick.labelsize' : 11})

# print(ISA(10))

def relative_density(rho_ref,T_ref,T2,P_ref=1,P2=1):

    return rho_ref * (T2/T_ref) * (P2/P_ref)


def calc_DlDv(rho_gas,rho_atm):
    DlDv = rho_atm * (1-(rho_gas/rho_atm))

    return -DlDv


h_range = [h for h in range(45000,45100, 100)]

DlDv_list = list()

for h in h_range:
    
    atm_params = ISA(h)
    hydrogen_density = relative_density(0.0841,288.15,
                                        atm_params[0])
    # print(hydrogen_density)
    # raise "Biem"
    DlDv_list.append(calc_DlDv(atm_params[2], hydrogen_density))


# y_spl = UnivariateSpline(h_range,DlDv_list,s=0,k=4)
# x_range = np.linspace(h_range[0],h_range[-1],100)

plt.plot(h_range,DlDv_list,)
# plt.plot(x_range,y_spl(x_range), label = 'spline fit')
plt.xlabel("Height [m]")
plt.ylabel("Lifted mass per volume of gas [kg/m^3]")
# plt.legend()
plt.show()

print(DlDv_list)

# y_spl_2d = y_spl.derivative(n=2)
# print(y_spl_2d(x_range))

# plt.plot(x_range,y_spl_2d(x_range),label = '2nd Derivative')
# plt.legend()
# plt.show()