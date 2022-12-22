import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv

from pymsis import msis


lon = 0
lat = -90
alt = 15
f107 = 150
f107a = 150
ap = 7
# One years worth of data at the 12th hour every day
dates = np.arange("2017-01-01", "2018-01-01", dtype="datetime64[D]")
ndates = len(dates)
print(ndates)
# (F107, F107a, ap) all need to be specified at the same length as dates
f107s = [f107] * ndates
f107as = [f107a] * ndates
aps = [[ap] * 7] * ndates

output = msis.run(dates, lon, lat, alt, f107s, f107as, aps)
#  output is now of the shape (ndates, 1, 1, 1, 11)
# Get rid of the single dimensions
output = np.squeeze(output)


# print(output)

# Lets get the percent variation from the annual mean for each variable
# variation = 100 * (output / output.mean(axis=0) - 1)
variation = output
print(dates.shape)
variables = [
    "Total mass density",
    "N2",
    "O2",
    "O",
    "He",
    "H",
    "Ar",
    "N",
    "Anomalous O",
    "NO",
    "Temperature",
]

np.savetxt("data_output.csv", output, delimiter=",", header = "".join(x+',' for x in variables))

plt.ion()

_, ax = plt.subplots()

# for i, label in enumerate(variables):
#     if label == "NO":
#         # There is currently no NO data
#         continue
#     ax.plot(dates, variation[:, i], label=label)

for i, label in enumerate(variables):
    if label == "Temperature":
        # There is currently no NO data
        lines = ax.plot(dates, variation[:, i], label=label)

ax.legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True, ncol=5
)
ax.set_xlabel(f"Longitude: {lon}, Latitude: {lat}, Altitude: {alt} km")
ax.set_ylabel(r"Total Atmospheric Density ($kg/m^3$)")
ax.set_xlim(dates[0], dates[-1])

# ax.set_ylim(0,1.5)
# ax.set_yscale("log")
# ax.set_ylim(0,0.3)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=50))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))

plt.show()

ascending = True
while True:
    if ascending:
        lat += 1
    else:
        lat -=1
    if lat > 90:
        ascending = False
    if lat <-90:
        ascending = True

    output = msis.run(dates, lon, lat, alt, f107s, f107as, aps)
    output = np.squeeze(output)
    variation = output
    # print(alt)
    for i, label in enumerate(variables):
        if label == "Temperature":
            # print(lat)
        # There is currently no NO data
            lines[0].set_data(dates, variation[:, i])

            ax.set_xlabel(f"Longitude: {lon}, Latitude: {lat}, Altitude: {alt:3.1f} km")
            plt.draw()
    
        plt.pause(1/240)
