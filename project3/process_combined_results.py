import os
import subprocess
import argparse
import glob


parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

COPY_COMMAND = "python /content/zzz_thaivv_tool/project3/new_copy_files.py"
COUNT_COMMAND = "python /content/zzz_thaivv_tool/project3/new_count_file.py"
CHECK_LOOSE_COMMAND = "python /content/zzz_thaivv_tool/project3/new_check_loose.py"
CHECK_EXISTED_COMMAND = "python /content/zzz_thaivv_tool/project3/new_check_existed.py"
LOSS_COUNT_COMMAND = "python /content/zzz_thaivv_tool/project3/new_loss_count.py"
WARNING_ROOT_PATH = "/content/drive/MyDrive/viettechtools/Project 3 - Warning"

if __name__ == "__main__":
    dpath = args.dpath
    
    is_new = False
    if "/New/" in dpath:
        is_new = True
    
    maker_list = glob.glob(os.path.join(dpath, '*', '*/'))
    for maker in maker_list:
        if "Results" in maker or "txt" in maker:
            continue
        
        if is_new == False and "/New/" in maker:
            continue

        tmp = "/".join(maker.split("/")[-3:-1])
        
        print("HANDLE COPY FILE " + tmp)
        command_run = f'{COPY_COMMAND} "{maker}"'
        subprocess.run(command_run, shell=True)
        
        print("HANDLE COUNT FILE ", tmp)
        command_run = f'{COUNT_COMMAND} "{maker}"'
        subprocess.run(command_run, shell=True)

        print("HANDLE CHECK LOSS FILE ", tmp)
        command_run = f'{CHECK_LOOSE_COMMAND} "{maker}"'
        subprocess.run(command_run, shell=True)
    
    
    print("HANDLE CHECK EXISTED COMMAND")
    command_run = f'{CHECK_EXISTED_COMMAND} "{dpath}"'
    subprocess.run(command_run, shell=True)
    
    print("HANDLE COUNT COMMAND ALL")
    command_run = f'{COUNT_COMMAND} "{dpath}/Results"'
    subprocess.run(command_run, shell=True)
    
    print("HANDLE LOSS COUNT COMMAND")
    warning_path = os.path.join(WARNING_ROOT_PATH, "/".join(dpath.split("/")[5:]))
    command_run = f'{LOSS_COUNT_COMMAND} "{warning_path}"'
    subprocess.run(command_run, shell=True)
        
    