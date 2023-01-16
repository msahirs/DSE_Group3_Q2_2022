import os
import glob
import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import dates


# OUTPUT_DATA_FILE = "merged_all_Final.csv"

curr_dir = os.getcwd()

list_csvs = []
codes = []
net_fluxes = []

mypath = "data/input_archive/relev_locs/merged_all_*.csv"

fig1, ax1= plt.subplots()
fig2, ax2= plt.subplots()

for filename in glob.glob(mypath):

    code = filename[-6:-4]
    codes.append(code)

    f_data = pd.read_csv(filename)
    f_data = f_data.iloc[::2]

    datelist = f_data.iloc[:,-1]
    len_dates = datelist.shape[0]

    flux_sum = f_data.iloc[:,-3].sum() / len_dates
    net_fluxes.append(flux_sum)
    print(f"flux at {code}: ", flux_sum)

    # f_data = f_data.assign(location = filename[-6:-4])
    
    # list_csvs.append(f_data)



    converted_dates = list(map(dt.datetime.strptime, datelist, len_dates*['%Y-%m-%d %H:%M:%S']))
    x_axis = converted_dates
    formatter = dates.DateFormatter('%Y/%m/%d %H:%M:%S')

    y_axis = f_data.iloc[:,-3]

    ax1.plot( x_axis, y_axis, 'o',markersize = 3, label = filename[-6:-4], alpha = 0.8)

    

# vert_csv = pd.concat(list_csvs)

ax1.xaxis.set_major_formatter(formatter)
ax1.legend()
fig1.autofmt_xdate(rotation=20)
ax1.set_xlabel("Time")
ax1.tick_params(axis='x', labelsize = 9)
ax1.set_ylabel("Solar Irradiance")
ax1.set_title("Variation of solar irradiance over 2022 at 18 km, for considered locations")
fig1.set_figheight(7)
fig1.set_figwidth(13)
fig1.savefig("data/input_archive/relev_locs/Irr_vs_time_locs.png")
# plt.savefig("data/input_archive/relev_locs/Irr_vs_time_locs.png")


ax2.bar(codes,net_fluxes)
# plt.xlabel("Time")
ax2.set_ylabel("Solar Irradiance[W/m^2]")
ax2.set_xlabel("Region Codes")
ax2.set_title("Average solar irradiance for 2022 at 18 km, for considered locations")
fig2.set_figheight(7)
fig2.set_figwidth(13)
fig2.savefig("data/input_archive/relev_locs/avg_Irr_vs_locs.png")

plt.show()
