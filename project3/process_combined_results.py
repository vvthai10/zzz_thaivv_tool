import os
import subprocess
import argparse
import glob


parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

COPY_COMMAND = "python ./new_copy_files.py"
COUNT_COMMAND = "python ./new_count_files.py"
CHECK_LOOSE_COMMAND = "python ./new_check_loose.py"
CHECK_EXISTED_COMMAND = "python ./new_check_existed.py"
LOSS_COUNT_COMMAND = "python ./new_loss_count.py"

if __name__ == "__main__":
    dpath = args.dpath
    
    maker_list = glob.glob(os.path.join(dpath, '*', '*/'))
    for maker in maker_list:
        if "Results" in maker:
            continue
        
        print("HANDLE COPY FILE")
        command_run = f'{COPY_COMMAND} "{maker}"'
        subprocess.run(command_run)
        
        print("HANDLE COUNT FILE")
        command_run = f'{CHECK_LOOSE_COMMAND} "{maker}"'
        subprocess.run(command_run)
    
    
    print("HANDLE CHECK EXISTED COMMAND")
    command_run = f'{CHECK_EXISTED_COMMAND} "{dpath}"'
    subprocess.run(command_run)
    
    print("HANDLE COUNT COMMAND ALL")
    command_run = f'{COUNT_COMMAND} "{dpath}/Results"'
    subprocess.run(command_run)
    
    print("HANDLE LOSS COUNT COMMAND")
    warning_path = ""
    command_run = f'{LOSS_COUNT_COMMAND} "{maker}/Results"'
    subprocess.run(command_run)
        
    