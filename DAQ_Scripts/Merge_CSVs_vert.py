import os
import glob
import pandas as pd

OUTPUT_DATA_FILE = "merged_FINAL.csv"

curr_dir = os.getcwd()

list_csvs = []

mypath = "data/input_archive/relev_locs/merged_all_*.csv"

for filename in glob.glob(mypath):

    code = print(filename[-6:-4])
    f_data = pd.read_csv(filename)

    f_data = f_data.assign(location = filename[-6:-4])

    list_csvs.append(f_data)

vert_csv = pd.concat(list_csvs)

print(vert_csv.shape)

with open(os.path.join(curr_dir,"data","input_archive","relev_locs",OUTPUT_DATA_FILE), 'w',) as f:\
    vert_csv.to_csv(f, index = False)
