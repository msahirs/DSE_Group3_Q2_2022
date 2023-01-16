from subprocess import Popen, PIPE, STDOUT
import os
import numpy as np
import pandas as pd
from multiprocessing.dummy import Pool

curr_dir = os.getcwd()

P_COUNT = 10
APP_NAME = "SPA.exe"
APP_PATH = ""
EXP_DATA = os.path.join(curr_dir,"data","sweep_parameters.pkl")
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

def get_lines(process):
    return process.communicate()[0].decode().splitlines()

def main():

    data = pd.read_pickle(EXP_DATA, compression='zip')
    
    line_count = data.shape[0]

    print(f"Input data of {line_count} rows")
    
    SPA_output = np.zeros((line_count,len(SPA_OUTPUT_HEADERS)))

    p_offset = line_count % P_COUNT != 0
    p_iter = line_count//P_COUNT

    for c in range(p_iter):
        
        if p_offset != 0 & c*P_COUNT >= line_count:
            input = [data.iloc[line_count-1 - p_offset,:].astype(str) for i in reversed(range(p_offset))]
        
        else:
            input = [data.iloc[c*P_COUNT + i,:].astype(str) for i in range(P_COUNT)]

        # print(input)

        # raise"error"
        
        # subprocess.run([APP_PATH, *line], check = True)
        # run commands in parallel
        raw_out = [Popen([APP_PATH, *input[i]], shell=True,
                   stdin=None, stdout=PIPE, stderr=STDOUT, close_fds=True).communicate()[0].decode().replace(" \r\n","") for i in range(P_COUNT)]
        
        
            

        

        

        # outputs = Pool(len(raw_out)).map(get_lines, raw_out)
        



        if p_offset != 0 & c*P_COUNT >= line_count:

            for x in reversed(range(len(raw_out))):
                
                SPA_output[line_count-1-x,:] = np.fromstring(raw_out[x], dtype = float, sep = " ")
        
        else:

            for x in range(len(raw_out)):
                
                
                SPA_output[c*P_COUNT + x,:] = np.fromstring(raw_out[x], dtype = float, sep = " ")

        if c*P_COUNT > 500:
            print( "Done")

            return 0

    if not os.path.exists(os.path.join(curr_dir,"data")):
        os.mkdir("data")

    np.savetxt("./data/SPA_output.csv", SPA_output, fmt = "%.3f", delimiter= ","
            , header=','.join(SPA_OUTPUT_HEADERS)) 

    print("SPA done! Data file successfully written") 

if __name__ == '__main__':

    main()

