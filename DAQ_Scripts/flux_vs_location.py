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

    plt.plot( x_axis, y_axis, 'o',markersize = 3, label = filename[-6:-4], alpha = 0.8)

    break

# vert_csv = pd.concat(list_csvs)

ax = plt.gcf().axes[0] 
ax.xaxis.set_major_formatter(formatter)
plt.legend()
plt.gcf().autofmt_xdate(rotation=25)
plt.xlabel("Time")
plt.ylabel("Solar Irradiance")
plt.show()

plt.bar(codes,net_fluxes)
# plt.xlabel("Time")
plt.ylabel("Average Solar Irradiance at computed times [W/m^2]")

plt.show()
