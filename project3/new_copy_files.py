"""
    Desc: Copy các folder results trong các folder con qua folder Results ngoài
    - Vì sẽ có cả trong folder chính và folder special trong nên cần handle cả 2
"""

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

PHASE_PATH = r"G:\\.shortcut-targets-by-id\\1h5Rp-00ViX9Sq_94KxJNvRiTTnjXCIyV\\Project 3 - Group2 - Phase11-20\\Phase13 - Job 80\\New"

def add_unc_prefix(path):
    if not path.startswith("\\\\?\\"):
        return f"\\\\?\\{os.path.abspath(path)}"
    return path

created = os.path.join(PHASE_PATH, "Results")
if not os.path.exists(created):
    os.mkdir(created)
            
def copy_results2_folder(folder2_list, dest_folder):
    save_path = dest_folder
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for folder2 in folder2_list:
        # create folder special
        if "special" in folder2:
            special_name = folder2.split("\\")[-2]
            special_path = os.path.join(dest_folder, special_name)
            if os.path.exists(special_path):
                shutil.rmtree(special_path)
            os.makedirs(special_path)
            save_path = special_path
            
        folder_name = os.path.basename(folder2.rstrip('/'))
        dst = os.path.join(save_path, folder_name)
        shutil.copytree(folder2, dst)
        

if __name__ == "__main__":
    dpath = args.dpath
    os.chdir(dpath)
    list_folder_branch = glob.glob("*", recursive=True)
    
    existing_folders = [f.lower() for f in os.listdir(os.path.join(PHASE_PATH, "Results"))]
    for folder_branch in list_folder_branch:
        print(folder_branch)
        
        
        if "desktop.ini" == folder_branch or ".txt" in folder_branch:
            continue
        
        if folder_branch.lower() in existing_folders:
            print("WARNINGGGGGGGGG: Existed folder same name: " + folder_branch)
        
        
        folder_path = os.path.join(dpath, folder_branch)
        
        folder_results2 = glob.glob(f"{folder_path}/**/*results2*", recursive=True)
        if len(folder_results2) == 0:
            save_path = os.path.join(PHASE_PATH, "Results", folder_branch)
            if os.path.exists(save_path):
                shutil.rmtree(save_path)
            os.makedirs(save_path)
            continue
        
        # Nếu tồn tại results2 thì move garment + results2 to Results
        save_path = os.path.join(PHASE_PATH, "Results", folder_branch)
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)
        
        copy_results2_folder(folder_results2, save_path)

