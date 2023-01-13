from matplotlib import pyplot as plt
from matplotlib import dates
import datetime as dt
import pandas as pd
import os

curr_dir = os.getcwd()

INP_DATA_FILE = os.path.join(curr_dir,"data","merged_all.csv")
if not os.path.exists(INP_DATA_FILE):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

f_data = pd.read_csv(INP_DATA_FILE)
datelist = f_data.iloc[:,-1]
len_dates = datelist.shape[0]


converted_dates = list(map(dt.datetime.strptime, datelist, len_dates*['%Y-%m-%d %H:%M:%S']))
x_axis = converted_dates
formatter = dates.DateFormatter('%Y/%m/%d %H:%M:%S')

y_axis = f_data.iloc[:,-3]

plt.plot( x_axis, y_axis, 'o' )
ax = plt.gcf().axes[0] 
ax.xaxis.set_major_formatter(formatter)
plt.gcf().autofmt_xdate(rotation=25)
plt.show()
