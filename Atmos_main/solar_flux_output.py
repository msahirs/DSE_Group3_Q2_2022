import os
# import numpy as np
import SunFlux as sf
import pandas as pd
import datetime as dt

curr_dir = os.getcwd()

INP_DATA_FILE = os.path.join(curr_dir,"data","input_archive","slope_valid","merged_noLines.csv")
OUTPUT_DATA_FILE = "merged_Final.csv"
REF_DAY = dt.datetime(1970,1,1)

# REF_DAY = np.datetime64('1970-01-01')

if not os.path.exists(INP_DATA_FILE):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

def LeapYearsBetween(end, start):

    return LeapYearsBefore(end) - LeapYearsBefore(start + 1)

def LeapYearsBefore(year):

    year-=1
    return (year // 4) - (year // 100) + (year // 400)

def DayOfYear(date):
    day_of_year = date.timetuple().tm_yday

    return day_of_year

def main():

    csv2np = pd.read_csv(INP_DATA_FILE)

    times = [None]*(csv2np.shape[0])
    year_day = [0]*(csv2np.shape[0])
    
    for i in range(csv2np.shape[0]):
        time_string = f"{int(csv2np.iloc[i,0]):04d}/{int(csv2np.iloc[i,1]):02d}/{int(csv2np.iloc[i,2]):02d} {int(csv2np.iloc[i,3]):02d}:{int(csv2np.iloc[i,4]):02d}:{int(csv2np.iloc[i,5]):02d}"
        
        times[i] = dt.datetime.strptime(time_string, "%Y/%m/%d %H:%M:%S")
        
        year_day[i] = DayOfYear(times[i])
        
    fluxes = []


    for i in range(csv2np.shape[0]):
        # [i,26] has zenith, [i,28] has incidences, [i,14] has slopes
        flux = sf.get_flux(csv2np.iloc[i,26],csv2np.iloc[i,28],csv2np.iloc[i,14],csv2np.iloc[i,12]/1013.25, year_day[i])

        fluxes.append(flux)

    add_var = {"FLUXES": fluxes,"YEAR_DAY": year_day ,"DATE/TIME": times,}
    add_var = pd.DataFrame.from_dict(add_var)

    merged_fluxes = pd.concat([csv2np,add_var], axis = 1)

    with open(os.path.join(curr_dir,"data","input_archive","slope_valid",OUTPUT_DATA_FILE), 'w',) as f:\
        merged_fluxes.to_csv(f, index = False)


if __name__ == '__main__':

    main()

