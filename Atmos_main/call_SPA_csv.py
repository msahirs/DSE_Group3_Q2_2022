import subprocess
import os
import csv
import numpy as np

curr_dir = os.getcwd()
APP_NAME = "SPA.exe"
APP_PATH = ""
EXP_DATA = os.path.join(curr_dir,"data","input_archive","relev_locs_zero","sweep_parameters_ME.csv")
SPA_OUTPUT_HEADERS = ["JULIAN DAY", "L", "B", "R","H","DELTA PSI",
                    "DELTA EPSILON","EPSILON","ZENITH","AZIMUTH",
                    "INCIDENCE","DEL_E"]


if not os.path.exists(os.path.join(curr_dir,"build","Solar_Angle_Calculator",APP_NAME)):
    raise ImportError("Application not found. \n Program Terminating")

else:
    APP_PATH = os.path.join(curr_dir,"build","Solar_Angle_Calculator", APP_NAME)


if not os.path.exists(EXP_DATA):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i

def main():
    
    line_count = row_count(EXP_DATA)

    with open(EXP_DATA, 'r') as datafile:

        parser = csv.reader(datafile)
        next(parser)

        SPA_output = np.zeros((line_count,len(SPA_OUTPUT_HEADERS)))

        for i, line in enumerate(parser):
            
            # subprocess.run([APP_PATH, *line], check = True)
            raw_out = subprocess.Popen([APP_PATH, *line], stdout=subprocess.PIPE)
            decoded_out = raw_out.communicate()[0].decode()
            
            if i%100 == 0:
                print("SPA at datapoint =",i)

            decoded_out = np.fromstring(decoded_out, dtype = float, sep = " ")
            
            SPA_output[i,:] = decoded_out

    if not os.path.exists(os.path.join(curr_dir,"data")):
        os.mkdir("data")

    np.savetxt("./data/input_archive/relev_locs_zero/SPA_output_ME.csv", SPA_output, fmt = "%.3f", delimiter= ","
            , header=','.join(SPA_OUTPUT_HEADERS)) 

    print("SPA done! Data file successfully written") 

if __name__ == '__main__':
    main()

