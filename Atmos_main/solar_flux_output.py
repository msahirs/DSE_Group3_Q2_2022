import os
# import numpy as np
import SunFlux as sf
import pandas as pd

curr_dir = os.getcwd()

INP_DATA_FILE = os.path.join(curr_dir,"data","merged.csv")
OUTPUT_DATA_FILE = "merged_fluxes.csv"

if not os.path.exists(INP_DATA_FILE):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

def main():
    csv2np = pd.read_csv(INP_DATA_FILE)
    
    fluxes = []

    for i in range(csv2np.shape[0]):

        flux = sf.get_flux(csv2np.iloc[i,26],csv2np.iloc[i,28], csv2np.iloc[i,14],0.054,172)

        fluxes.append(flux)

    fluxes = {"FLUXES":fluxes}
    fluxes = pd.DataFrame.from_dict(fluxes)

    merged_fluxes = pd.concat([csv2np,fluxes],axis = 1)

    with open(os.path.join(curr_dir,"data",OUTPUT_DATA_FILE), 'w',) as f:\
        merged_fluxes.to_csv(f,index = False)


if __name__ == '__main__':

    main()

