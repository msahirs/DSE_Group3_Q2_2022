from matplotlib import pyplot as plt
from matplotlib import dates
import datetime as dt
import pandas as pd
import os

curr_dir = os.getcwd()

INP_DATA_FILE = os.path.join(curr_dir,"data/input_archive/North_18","merged_Final.csv")
if not os.path.exists(INP_DATA_FILE):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

f_data_net = pd.read_csv(INP_DATA_FILE)

fig1, ax1= plt.subplots()
fig2, ax2= plt.subplots()
ids = []
avgs = []

for i in range(6):
    
    # f_data = f_data_net[f_data_net['LATITUDE'] >= 60]
    f_data = f_data_net.iloc[16128*i : 16128*(i+1):1,:]
    print(f_data.shape)
    # print(f_data.iloc[:,9])

    datelist = f_data.iloc[:,-1]
    len_dates = datelist.shape[0]
        

    flux_avg = f_data.iloc[:,-3].sum() / len_dates
    avgs.append(flux_avg)
    id_num = f"Long = {f_data.iloc[0,9]}, \n Lat = {f_data.iloc[0,10]}"
    ids.append(id_num)

    converted_dates = list(map(dt.datetime.strptime, datelist, len_dates*['%Y-%m-%d %H:%M:%S']))
    x_axis = converted_dates
    formatter = dates.DateFormatter('%Y/%m/%d %H:%M:%S')

    y_axis = f_data.iloc[:,-3]

    ax1.plot( x_axis, y_axis, 'o', markersize= 2,label =f"Long = {f_data.iloc[0,9]}, Lat = {f_data.iloc[0,10]}")

ax1.xaxis.set_major_formatter(formatter)
ax1.legend()
fig1.autofmt_xdate(rotation=20)
ax1.set_xlabel("Time")
ax1.tick_params(axis='x', labelsize = 9)
ax1.set_ylabel("Solar Irradiance [W/m^2]")
ax1.set_title("Flux over time at 18 km for Northern Latitudes")
fig1.savefig("data/input_archive/North_18/Irr_vs_time.png")
fig1.savefig("Bob1.png")

ax2.bar(ids,avgs)
# plt.xlabel("Time")
ax2.set_ylabel("Solar Irradiance [W/m^2]")
ax2.set_xlabel("Geographic locations")
ax2.set_title("Average solar irradiance throughout 2022 at 18 km for Northern Latitudes")
fig2.set_figheight(7)
fig2.set_figwidth(13)
fig2.savefig("data/input_archive/North_18/avg_vs_locs.png")
