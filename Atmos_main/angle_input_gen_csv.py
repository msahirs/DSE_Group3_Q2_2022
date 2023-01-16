import numpy as np
import os
from SunFlux import isa

curr_dir = os.getcwd()

REF_ANGLE_HEADERS = ["YEAR","MONTH","DAY","HOUR","MINUTE",
                    "SECOND","TIMEZONE","DELTA_UT1", "DELTA_T",
                    "LONGITUDE","LATITUDE","ELEVATION","PRESSURE",
                    "TEMPERATURE","SLOPE","AZM_ROTATION","ATMOS_REFRACT",
                    "FUNCTION"]


ref_angle_inp = "2022 7 15 13 30 0 0 0 69.184 120 30 0 1013.25 15 0 0 0.65 1".split(" ")
ref_angle_inp = [float(x) for x in ref_angle_inp]
ref_angle_inp = np.array(ref_angle_inp)

second_sweep = np.arange(start = 0, stop = 60, step= 30)
minute_sweep = np.arange(start = 0, stop = 60, step= 1)
hour_sweep = np.arange(0,24,1)
# day_sweep = np.arange(1,29,1)
# month_sweep = np.arange(1,13,1)
elevation_sweep = np.arange(12000,21000,500)
# longitude_sweep = np.arange(-180,181,20)
# latitude_sweep = np.arange(-90,91,10)

longitude_sweep = [3.84898]

latitude_sweep = [52.37079]

# slope_sweep = np.arange(-175,180,5)

# sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep,day_sweep,month_sweep,longitude_sweep,latitude_sweep,copy=False)).T.reshape(-1,6)
# sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep,day_sweep,month_sweep,elevation_sweep)).T.reshape(-1,5)
sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep,second_sweep,elevation_sweep)).T.reshape(-1,4)
# sweep_params = np.array(np.meshgrid(slope_sweep)).T.reshape(-1,1)

main_data = np.tile(ref_angle_inp, (sweep_params.shape[0],1))

pressures = [isa.getVals(h)[0]/100 for h in sweep_params[:,3]]
temperatures = [isa.getVals(h)[1]/100 for h in sweep_params[:,3]]

# print(sweep_params)
# print(main_data.shape)

# main_data[:,11] = sweep_params[:,4]
main_data[:,3] = sweep_params[:,0]
main_data[:,4] = sweep_params[:,1]
main_data[:,5] = sweep_params[:,2]
main_data[:,11] = sweep_params[:,3]
main_data[:,12] = pressures
main_data[:,13] = temperatures


# main_data[:,9] = sweep_params[:,4]
# main_data[:,10] = sweep_params[:,5]

# main_data[:,14] = sweep_params[:,0]


if not os.path.exists(os.path.join(curr_dir,"data")):
    os.mkdir("data")

np.savetxt("./data/input_archive/elevation_gain/sweep_parameters.csv", main_data, fmt = "%.2f", delimiter= ","
            , header=','.join(REF_ANGLE_HEADERS))

print("Written Input sweep data")



