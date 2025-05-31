from PIL import Image
from pathlib import Path
import pillow_avif
import numpy as np
import glob
import cv2
import os
import json
from pathlib import Path  
import shutil 
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

# LIST_PHASE_PATHS = [
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase11 - Job 82/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase12 - Job 81/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase13 - Job 80/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase14 - Job 79/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase15 - Job 78/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase16 - Job 77/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase17 - Job 76/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase18 - Job 75/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase19 - Job 74/",
#     "G:\\My Drive\\viettechtools\\Project 3 - Warning\\Project 3 - Group2 - Phase11-20\\Phase20 - Job 73/",
# ]

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Count label<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    LIST_PHASE_PATHS = [dpath]
    for path in LIST_PHASE_PATHS:
        list_folder_branch = os.listdir(path)
        arr_folder = []
        arr_count = []
        arr_child_folder = []
        arr_child_count = []
        for folder_branch in tqdm((list_folder_branch)):
            # print(folder_branch)
            if "desktop.ini" == folder_branch or ".txt" in folder_branch:
                continue
            
            text_save = f"{folder_branch}"
            loss_count = 0
            folder_path = os.path.join(path, folder_branch)
            warning_files = glob.glob(f"{folder_path}/**/warning.txt", recursive=True)
            for file in warning_files:
                # print(file.split("\\")[6:-1])
                text_save_copy = text_save
                for text in file.split("\\")[6:-1]:
                    text_save_copy = text_save_copy + " -- " + text
                
                # print(folder_path)
                with open(file, 'r') as f:
                    for line in f:
                        parts = line.split(' ')
                        strings = ''.join(parts[:-1])
                        cnt = parts[-1]
                        loss_count += int(cnt)
                        text_save_temp = text_save_copy + " -- " + strings
                        arr_child_folder.append(text_save_temp)
                        # print(strings)
                        arr_child_count.append(int(cnt))
                            
            arr_folder.append(folder_branch)
            arr_count.append(loss_count)
            
        with open(path+'\\warning.txt', 'w') as file:
            for item1, item2 in zip(arr_folder, arr_count):
                file.write(f"{item1} {item2}\n")
                
        with open(path+'\\warning_detail.txt', 'w') as file:
            for item1, item2 in zip(arr_child_folder, arr_child_count):
                file.write(f"{item1}: {item2}\n")
      