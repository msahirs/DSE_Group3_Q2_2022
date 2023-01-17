import pandas as pd
import os
def merge_CSVs(file_a,file_b,output_dir):

    if os.path.exists(file_a) | os.path.exists(file_a) == False:
        raise "Input files not present"


    a = pd.read_csv(file_a)
    b = pd.read_csv(file_b)
    comb = pd.concat([a,b],axis=1)
    
    with open(os.path.join(os.getcwd(),output_dir,"merged_ME.csv"), 'w',) as f:\
        comb.to_csv(f,index = False)

    # merged.to_csv(os.path.join(os.getcwd(),output_dir,"merged.csv"), index=False)

cwd = os.getcwd()

file_b = os.path.join(cwd,"data","input_archive","relev_locs_zero","SPA_Output_ME.csv")
file_a = os.path.join(cwd,"data","input_archive","relev_locs_zero","sweep_parameters_ME.csv")

merge_CSVs(file_a,file_b,"data/input_archive/relev_locs_zero")

