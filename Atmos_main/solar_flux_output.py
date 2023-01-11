import os
# import numpy as np
import SunFlux as sf
import pandas as pd

curr_dir = os.getcwd()

DATA_FILE = os.path.join(curr_dir,"data","merged.csv")

if not os.path.exists(DATA_FILE):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

csv2np = pd.read_csv(DATA_FILE)

fluxes = []

for i in range(csv2np.shape[0]):

    flux = sf.get_flux(csv2np.iloc[i,26],csv2np.iloc[i,28], csv2np.iloc[i,14],0.054,172)

    fluxes.append(flux)

fluxes = {"FLUXES":fluxes}
fluxes = pd.DataFrame.from_dict(fluxes)

merged_fluxes = pd.concat([csv2np,fluxes],axis = 1)

with open(os.path.join(curr_dir,"data","merged_fluxes.csv"), 'w',) as f:\
    merged_fluxes.to_csv(f,index = False)

