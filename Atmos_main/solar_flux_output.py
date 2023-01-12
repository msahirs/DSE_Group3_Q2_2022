import os
# import numpy as np
import SunFlux as sf
import pandas as pd
import numpy as np
import calendar

curr_dir = os.getcwd()

INP_DATA_FILE = os.path.join(curr_dir,"data","merged.csv")
OUTPUT_DATA_FILE = "merged_fluxes.csv"
REF_DAY = np.datetime64('1970-01-01')

if not os.path.exists(INP_DATA_FILE):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

def LeapYearsBetween(end, start):

    return LeapYearsBefore(end) - LeapYearsBefore(start + 1)

def LeapYearsBefore(year):

    year-=1
    return (year // 4) - (year // 100) + (year // 400)

def DayOfYear(date):
    
    leap_days = LeapYearsBetween(date.astype('datetime64[Y]').astype(int) + 1970,
                REF_DAY.astype('datetime64[Y]').astype(int) + 1970)
    
    shift = 0

    if calendar.isleap(date.astype('datetime64[Y]').astype(int) + 1970) and date.astype('datetime64[M]').astype(int) % 12 + 1 == 12:
        shift = 1

    raw_days = ((np.datetime64(date,'D') - REF_DAY).astype(int) - leap_days - shift) % 365
    
    return raw_days + 1

def main():

    csv2np = pd.read_csv(INP_DATA_FILE)

    datetime = np.zeros((csv2np.shape[0],1),dtype='datetime64[s]')
    year_day = np.zeros((csv2np.shape[0],1),dtype=int)
    
    for i in range(csv2np.shape[0]):
        time_string = f"{int(csv2np.iloc[i,0]):04d}-{int(csv2np.iloc[i,1]):02d}-{int(csv2np.iloc[i,2]):02d}T{int(csv2np.iloc[i,3]):02d}:{int(csv2np.iloc[i,4]):02d}:{int(csv2np.iloc[i,5]):02d}"

        datetime[i,0] = np.datetime64(time_string)
        year_day[i,0] = DayOfYear(datetime[i,0])
    
    fluxes = []

    for i in range(csv2np.shape[0]):
        # [i,26] has zenith, [i,28] has incidences, [i,14] has slopes
        flux = sf.get_flux(csv2np.iloc[i,26],csv2np.iloc[i,28],csv2np.iloc[i,14],0.054,year_day[i,0])

        fluxes.append(flux)

    add_var = {"FLUXES": fluxes,}
    add_var = pd.DataFrame.from_dict(add_var)

    merged_fluxes = pd.concat([csv2np,add_var], axis = 1)

    with open(os.path.join(curr_dir,"data",OUTPUT_DATA_FILE), 'w',) as f:\
        merged_fluxes.to_csv(f,index = False)


if __name__ == '__main__':

    main()

