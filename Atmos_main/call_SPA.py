import subprocess
import os
import csv

curr_dir = os.getcwd()
APP_NAME = "SPA.exe"
APP_PATH = ""
EXP_DATA = os.path.join(curr_dir,"data","sweep_parameters.csv")

if not os.path.exists(os.path.join(curr_dir,"build","Solar_Angle_Calculator",APP_NAME)):
    raise ImportError("Application not found. \n Program Terminating")

else:
    APP_PATH = os.path.join(curr_dir,"build","Solar_Angle_Calculator", APP_NAME)


if not os.path.exists(EXP_DATA):
    raise ImportError("Datafile not found. Maybe run input generator file\n",
                        "Program Terminating")

def main():

    with open(EXP_DATA, 'r') as datafile:
        parser = csv.reader(datafile)

        for line in parser:
            # print(line)

            subprocess.run([APP_PATH, *line], check = True)


if __name__ == '__main__':
   
    main()
