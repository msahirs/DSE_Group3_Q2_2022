import matplotlib.pyplot as plt
import numpy as np

from pymsis import msis


lons = np.arange(-180, 185, 2.5).tolist()
print(lons)
lats = np.arange(-90, 95, 2.5).tolist()
alt = 1
f107 = 150
f107a = 150
ap = 7
# One years worth of data at the 12th hour every day
date = np.datetime64("2003-01-01T00:00")
aps = [[ap] * 7]

output = msis.run(date, lons, lats, alt, f107, f107a, aps)
#  output is now of the shape (1, nlons, nlats, 1, 11)
# Get rid of the single dimensions
output = np.squeeze(output)

i = 0  # O2

_, ax = plt.subplots()
xx, yy = np.meshgrid(lons, lats)
mesh = ax.pcolormesh(xx, yy, output[:, :, i].T, shading="auto", cmap = "plasma")
plt.colorbar(mesh, label="Number density (/m$^3$)")

ax.set_title(f"O$_2$ number density at {alt} km")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
# ax.set_da

plt.show()

for i in range(10):
    pass