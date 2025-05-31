from PIL import Image
from pathlib import Path
import pillow_avif
import numpy as np
import glob
import cv2
import os
from pathlib import Path  
import shutil 
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

import os
import shutil
import glob

PHASE_PATH = r"G:\\.shortcut-targets-by-id\\1xyV1oi1s-CghkDM_2ClrTlUcs7V4DnuA\\Project 3 - Group15 - Phase141-150\\Phase147 - Job 167"
# PHASE_PATH = "D:\\fix_viettech\\Phase82 - Job 106"
# Bổ sung hỗ trợ UNC path
def add_unc_prefix(path):
    if not path.startswith("\\\\?\\"):
        return f"\\\\?\\{os.path.abspath(path)}"
    return path

if not os.path.exists(add_unc_prefix(os.path.join(PHASE_PATH, "Results"))):
    os.mkdir(add_unc_prefix(os.path.join(PHASE_PATH, "Results")))

def copy_folder_contents(source_folder, dest_folder):
    source_folder = add_unc_prefix(source_folder)
    dest_folder = add_unc_prefix(dest_folder)
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(dest_folder, item)
        
        if "results2" in item and os.path.isdir(source_item):
            copy_folder_contents(source_item, destination_item)
        elif "results2" in source_item and ".json" in item:
            # print(source_item)
            # print(destination_item)
            shutil.copy2(source_item, destination_item)

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Copy label.json to Results<<<<<<<<<<<<<<<<<<")
    
    dpath = args.dpath
    os.chdir(dpath)
    list_folder_branch = glob.glob("*", recursive=True)

    for folder_branch in list_folder_branch:
        print(folder_branch)
        if "desktop.ini" == folder_branch or ".txt" in folder_branch:
            continue
        
        folder_path = os.path.join(dpath, folder_branch)
        os.chdir(folder_path)
        
        folder_results2 = glob.glob("*results2*", recursive=True)
        if len(folder_results2) == 0:
            save_path = os.path.join(PHASE_PATH, "Results", folder_branch)
            save_path = add_unc_prefix(save_path)
            if os.path.exists(save_path):
                shutil.rmtree(save_path)
            os.makedirs(save_path)
            continue
        
        # Nếu tồn tại results2 thì move garment + results2 to Results
        save_path = os.path.join(PHASE_PATH, "Results", folder_branch)
        save_path = add_unc_prefix(save_path)
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)
        
        copy_folder_contents(folder_path, save_path)


# PHASE_PATH = "G:\\.shortcut-targets-by-id\\1kEM8Z6hn9H0fChLv4o7s4bPcskUt0LXT\\Project 3 - Group11 - Phase 101-110\\Phase102 - Phase2/"
# if not os.path.exists(os.path.join(PHASE_PATH, "Results")):
#     os.mkdir(os.path.join(PHASE_PATH, "Results"))
            
# def copy_folder_contents(source_folder, dest_folder):
#     if not os.path.exists(dest_folder):
#         os.makedirs(dest_folder)

#     for item in os.listdir(source_folder):
#         source_item = os.path.join(source_folder, item)
#         destination_item = os.path.join(dest_folder, item)
#         # print(item)
#         if "results2" in item and os.path.isdir(source_item):
#             copy_folder_contents(source_item, destination_item)
#         elif "results2" in source_item and ".json" in item:
#             print(source_item)
#             print(destination_item)
#             shutil.copy2(source_item, destination_item)

# if __name__ == "__main__":
#     print(">>>>>>>>>>>>>>>>>>>>Copy label.json to Results<<<<<<<<<<<<<<<<<<")
#     dpath = args.dpath
    
#     os.chdir(dpath)
#     list_folder_branch = glob.glob("*", recursive=True)
#     for folder_branch in list_folder_branch:
#         print(folder_branch)
#         if "desktop.ini" == folder_branch or ".txt" in folder_branch:
#             continue
        
#         folder_path = os.path.join(dpath, folder_branch)
#         os.chdir(folder_path)
        
#         folder_results2 = glob.glob("*results2*", recursive = True)
#         # print(folder_results2)
#         if len(folder_results2) == 0:
#             save_path = os.path.join(PHASE_PATH, "Results", folder_branch)
#             if os.path.exists(save_path):
#                 shutil.rmtree(save_path)
#             os.makedirs(save_path)
#             continue
        
#         # Nếu tồn tại results2 thì move garment + results2 to Results
#         save_path = os.path.join(PHASE_PATH, "Results", folder_branch)
#         if os.path.exists(save_path):
#             shutil.rmtree(save_path)
#         os.makedirs(save_path)
        
#         # print(folder_path)
#         # print(save_path)
#         copy_folder_contents(folder_path, save_path)
        
        