import numpy as np
import matplotlib.pyplot as plt

# Values (based on V1.0)
V_oc = 2700  # mV
I_sc = 2132  # mA
V_mp = 2411  # mV
I_mp = 1938  # mA

d_V_oc = -6.2  # mV/K
d_I_sc = 1.387  # mA/K
d_V_mp = -6.7  # mV/K
d_I_mp = 0.924  # mA/K

# Higher T curves
def iv(T):
    # Standard curves
    C2 = (V_mp / V_oc - 1) / (np.log(1 - I_mp / I_sc))
    C1 = (1 - I_mp / I_sc) * np.exp(- V_mp / C2 / V_oc)

    I_list = []
    V_list = []
    P_list = []
    for V in range(0, V_oc + 50, 1):
        I_list.append(I_sc * (1 - C1 * (np.exp(V / C2 / V_oc) - 1)))
        V_list.append(V)
        P_list.append(V * I_list[V] / 1000)

    D_V_oc = d_V_oc * (T - 28)
    D_I_sc = d_I_sc * (T - 28)
    D_V_mp = d_V_mp * (T - 28)
    D_I_mp = d_I_mp * (T - 28)

    V_oc1 = V_oc + D_V_oc
    I_sc1 = I_sc + D_I_sc
    V_mp1 = V_mp + D_V_mp
    I_mp1 = I_mp + D_I_mp

    C2 = (V_mp1 / V_oc1 - 1) / (np.log(1 - I_mp1 / I_sc1))
    C1 = (1 - I_mp1 / I_sc1) * np.exp(- V_mp1 / C2 / V_oc1)

    I1_list = []
    V1_list = []
    P1_list = []
    for V1 in range(0, V_oc + 50, 1):
        I1_list.append(I_sc1 * (1 - C1 * (np.exp(V1 / C2 / V_oc1) - 1)))
        V1_list.append(V1)
        P1_list.append(V1 * I1_list[V1] / 1000)

    eff_loss = (np.amax(P1_list) - np.amax(P_list)) / np.amax(P_list) *100
    return eff_loss, V_list, I_list, P_list, V1_list, I1_list, P1_list


# Single input
T_new = 42.84  # Celcius

eff_loss, V_list, I_list, P_list, a, b, c = iv(T_new)

# Plot IV

plt.figure(1)
plt.ylabel('mA')
plt.xlabel('mV')
plt.title('I-V Curve')
plt.ylim(0, I_sc * 1.05)
plt.xlim(0, V_oc * 1.05)
plt.plot(V_list, I_list, color='b', label='28 °C')
plt.plot(a, b, color='r', label=str(T_new) + ' °C')
plt.legend()

# Plot PV
plt.figure(2)
plt.ylabel('mW')
plt.xlabel('mV')
plt.yticks([500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500])
plt.title('P-V Curve')
plt.ylim(0, np.amax(P_list) * 1.05)
plt.xlim(0, V_oc * 1.05)
plt.plot(V_list, P_list, color='b', label='28 °C')
#plt.plot(a, c, color='r', label=str(T_new) + ' °C')
plt.legend()

print((np.amax(c) - np.amax(P_list)) / np.amax(P_list) *100, '% loss')
print(np.amax(P_list),  'mw/cell')
print(np.amax(c), 'mw/cell')
plt.show()
