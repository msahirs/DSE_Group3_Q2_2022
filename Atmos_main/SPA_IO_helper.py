import pandas as pd
import os
import csv
def merge_CSVs(file_a,file_b,output_dir):

    if os.path.exists(file_a) | os.path.exists(file_a) == False:
        raise "Input files not present"


    a = pd.read_csv(file_a)
    b = pd.read_csv(file_b)
    comb = pd.concat([a,b],axis=1)

    # comb = comb[["LONGITUDE","LATITUDE","ZENITH"]]
    
    with open(os.path.join(os.getcwd(),output_dir,"merged.csv"), 'w',) as f:\
        comb.to_csv(f,index=False, na_rep='True')
    
    with open(os.path.join(os.getcwd(),output_dir,"merged.csv"), newline='') as in_file:
        with open(os.path.join(os.getcwd(),output_dir,"merged_noLines.csv"), 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)

    # merged.to_csv(os.path.join(os.getcwd(),output_dir,"merged.csv"), index=False)

cwd = os.getcwd()

file_b = os.path.join(cwd,"data","input_archive","North_0","SPA_output.csv")
file_a = os.path.join(cwd,"data","input_archive","North_0","sweep_parameters.csv")

merge_CSVs(file_a,file_b,"data/input_archive/North_0")



