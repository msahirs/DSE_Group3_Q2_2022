import numpy as np
import os
from SunFlux import isa

curr_dir = os.getcwd()

REF_ANGLE_HEADERS = ["YEAR","MONTH","DAY","HOUR","MINUTE",
                    "SECOND","TIMEZONE","DELTA_UT1", "DELTA_T",
                    "LONGITUDE","LATITUDE","ELEVATION","PRESSURE",
                    "TEMPERATURE","SLOPE","AZM_ROTATION","ATMOS_REFRACT",
                    "FUNCTION"]


ref_angle_inp = "2022 2 2 11 45 0 0 0 69.184 4.35 52.0 18000 75.0484 15 0 0 0.65 1".split(" ")
ref_angle_inp = [float(x) for x in ref_angle_inp]
ref_angle_inp = np.array(ref_angle_inp)

# second_sweep = np.arange(start = 0, stop = 60, step= 30)
minute_sweep = np.arange(start = 0, stop = 60, step= 30)
hour_sweep = np.arange(0,24,1)
day_sweep = np.arange(1,29,1)
month_sweep = np.arange(1,13,1)
# elevation_sweep = np.arange(0,21000,500)
longitude_sweep = np.arange(0,30,10)
latitude_sweep = np.arange(70,90,10)

# longitude_sweep = [21.17911]

# latitude_sweep = [37.36599]

# slope_sweep = np.arange(-175,180,5)

sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep,day_sweep,month_sweep,longitude_sweep,latitude_sweep,copy=False)).T.reshape(-1,6)
# sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep,day_sweep,month_sweep,elevation_sweep)).T.reshape(-1,5)
# sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep,elevation_sweep)).T.reshape(-1,3)
# sweep_params = np.array(np.meshgrid(slope_sweep)).T.reshape(-1,1)
# sweep_params = np.array(np.meshgrid(longitude_sweep,latitude_sweep)).T.reshape(-1,2)

main_data = np.tile(ref_angle_inp, (sweep_params.shape[0],1))

# pressures = [isa.getVals(h)[0]/100 for h in sweep_params[:,2]]
# temperatures = [isa.getVals(h)[1]/100 for h in sweep_params[:,2]]
# print(sweep_params)
# print(main_data.shape)

# main_data[:,11] = sweep_params[:,2]
main_data[:,3] = sweep_params[:,0]
# main_data[:,3] = sweep_params[:,0]
main_data[:,4] = sweep_params[:,1]
# main_data[:,4] = sweep_params[:,1]
main_data[:,2] = sweep_params[:,2]
main_data[:,1] = sweep_params[:,3]
# main_data[:,12] = pressures
# main_data[:,13] = temperatures
# print(sweep_params)

main_data[:,9] = sweep_params[:,4]
main_data[:,10] = sweep_params[:,5]

# main_data[:,14] = sweep_params[:,0]


if not os.path.exists(os.path.join(curr_dir,"data")):
    os.mkdir("data")

np.savetxt("./data/input_archive/North_0/sweep_parameters.csv", main_data, fmt = "%.2f", delimiter= ","
            , header=','.join(REF_ANGLE_HEADERS))

print("Written Input sweep data")



