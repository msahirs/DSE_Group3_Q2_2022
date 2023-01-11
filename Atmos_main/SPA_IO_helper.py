import pandas as pd
import os
def merge_CSVs(file_a,file_b,output_dir):

    if os.path.exists(file_a) | os.path.exists(file_a) == False:
        raise "Input files not present"


    a = pd.read_csv(file_a).astype("string")
    b = pd.read_csv(file_b).astype("string")
    comb = pd.concat([a,b],axis=1)
    print(comb.shape)
    with open(os.path.join(os.getcwd(),output_dir,"merged.csv"), 'w',) as f:\
        comb.to_csv(f,index = False)

    # merged.to_csv(os.path.join(os.getcwd(),output_dir,"merged.csv"), index=False)

cwd = os.getcwd()

file_b = os.path.join(cwd,"data","SPA_Output.csv")
file_a = os.path.join(cwd,"data","sweep_parameters.csv")

merge_CSVs(file_a,file_b,"data")

