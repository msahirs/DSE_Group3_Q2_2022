import numpy as np
import os

curr_dir = os.getcwd()

REF_ANGLE_HEADERS = ["YEAR","MONTH","DAY","HOUR","MINUTE",
                    "SECOND","TIMEZONE","DELTA_UT1", "DELTA_T",
                    "LONGITUDE","LATITUDE","ELEVATION","PRESSURE",
                    "TEMPERATURE","SLOPE","AZM_ROTATION","ATMOS_REFRACT",
                    "FUNCTION"]


ref_angle_inp = '2022 1 1 12 30 30 2.0 0 67 4.3 51.98 1000 1015.3 25 0 0 0.5667 1'.split(" ")
ref_angle_inp = [float(x) for x in ref_angle_inp]
ref_angle_inp = np.array(ref_angle_inp)

month_sweep = np.arange(start = 1, stop = 12+1, step= 1)
lat_sweep = np.arange(-80,80+10,10)

sweep_params = np.array(np.meshgrid(month_sweep,lat_sweep)).T.reshape(-1,2)

main_data = np.tile(ref_angle_inp, (sweep_params.shape[0],1))

# print(sweep_params)
# print(main_data.shape)

main_data[:,1] = sweep_params[:,0]
main_data[:,10] = sweep_params[:,1]


if not os.path.exists(os.path.join(curr_dir,"data")):
    os.mkdir("data")

np.savetxt("./data/sweep_parameters.csv", main_data, fmt = "%.2f", delimiter= ","
            , header=','.join(REF_ANGLE_HEADERS))



