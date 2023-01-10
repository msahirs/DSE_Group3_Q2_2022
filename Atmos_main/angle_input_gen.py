import numpy as np
import os

curr_dir = os.getcwd()

REF_ANGLE_HEADERS = ["YEAR","MONTH","DAY","HOUR","MINUTE",
                    "SECOND","TIMEZONE","DELTA_UT1", "DELTA_T",
                    "LONGITUDE","LATITUDE","ELEVATION","PRESSURE",
                    "TEMPERATURE","SLOPE","AZM_ROTATION","ATMOS_REFRACT",
                    "FUNCTION"]


ref_angle_inp = "2019 7 25 12 30 0 2.0 0 69.184 13.3 52.33 10 1015.3 25 0 0 0.556 1".split(" ")
ref_angle_inp = [float(x) for x in ref_angle_inp]
ref_angle_inp = np.array(ref_angle_inp)

minute_sweep = np.arange(start = 0, stop = 60, step= 10)
hour_sweep = np.arange(0,24,1)

sweep_params = np.array(np.meshgrid(hour_sweep,minute_sweep)).T.reshape(-1,2)

main_data = np.tile(ref_angle_inp, (sweep_params.shape[0],1))

# print(sweep_params)
# print(main_data.shape)

main_data[:,3] = sweep_params[:,0]
main_data[:,4] = sweep_params[:,1]


if not os.path.exists(os.path.join(curr_dir,"data")):
    os.mkdir("data")

np.savetxt("./data/sweep_parameters.csv", main_data, fmt = "%.2f", delimiter= ","
            , header=','.join(REF_ANGLE_HEADERS))



