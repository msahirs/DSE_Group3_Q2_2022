import solcore.light_source as ls
import numpy as np
import matplotlib.pyplot as plt

bandgap_top = 1.86
bandgap_middle = 1.4
bandgap_bottom = 0.65
#uv_cap = 300
#if_cap = 1239.8 / bandgap_bottom

ls.get_default_spectral2_object()
ls.get_default_smarts_object()

am0 = ls.light_source.reference_spectra()
am0 = np.delete(am0, [2, 3], 1)
plt.plot(am0[:, 0], am0[:, 1])
plt.xlabel('nanometers')
plt.ylabel('W/m2.nm')
plt.vlines([1239.8 / bandgap_top, 1239.8 / bandgap_middle, 1239.8 / bandgap_bottom], 0, 2, linestyles='dashed')

index_top = np.where(am0[:, 0] < 1239.8 / bandgap_top)
index_middle = np.where((am0[:, 0] > 1239.8 / bandgap_top) & (am0[:, 0] < 1239.8 / bandgap_middle))
index_bottom = np.where((am0[:, 0] > 1239.8 / bandgap_middle) & (am0[:, 0] < 1239.8 / bandgap_bottom))
am0_top = np.copy(am0[index_top])
am0_middle = np.copy(am0[index_middle])
am0_bottom = np.copy(am0[index_bottom])

am0_top_ev = np.copy(am0_top)
am0_top_ev[:, 0] = bandgap_top / (1239.8 / am0_top_ev[:, 0])
am0_top_ev[:, 0] = 1 - am0_top_ev[:, 0]
am0_top_ev[:, 1] = am0_top_ev[:, 0] * am0_top[:, 1]
am0_middle_ev = np.copy(am0_middle)
am0_middle_ev[:, 0] = bandgap_middle / (1239.8 / am0_middle_ev[:, 0])
am0_middle_ev[:, 0] = 1 - am0_middle_ev[:, 0]
am0_middle_ev[:, 1] = am0_middle_ev[:, 0] * am0_middle[:, 1]
am0_bottom_ev = np.copy(am0_bottom)
am0_bottom_ev[:, 0] = bandgap_bottom / (1239.8 / am0_bottom_ev[:, 0])
am0_bottom_ev[:, 0] = 1 - am0_bottom_ev[:, 0]
am0_bottom_ev[:, 1] = am0_bottom_ev[:, 0] * am0_bottom[:, 1]

a = np.trapz(am0_top_ev[:, 1], am0_top[:, 0])
b = np.trapz(am0_middle_ev[:, 1], am0_middle[:, 0])
c = np.trapz(am0_bottom_ev[:, 1], am0_bottom[:, 0])
print(a, b, c, a + b + c, (a + b + c) / 1353 * 100, '%')
plt.plot(am0_top[:, 0], am0_top_ev[:, 1])
plt.plot(am0_middle[:, 0], am0_middle_ev[:, 1])
plt.plot(am0_bottom[:, 0], am0_bottom_ev[:, 1])

plt.show()
