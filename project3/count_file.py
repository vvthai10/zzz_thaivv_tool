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

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Count label<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    
    os.chdir(dpath)
    list_folder_branch = glob.glob("*", recursive=True)
    cnt_whole_body = 0
    cnt_else = 0
    for folder_branch in tqdm((list_folder_branch)):
        # print(folder_branch)
        if "desktop.ini" == folder_branch or ".txt" in folder_branch:
            continue
        
        folder_path = os.path.join(dpath, folder_branch)
        os.chdir(folder_path)
        
        folder_results2 = glob.glob("*", recursive = True)
        name_results2 = ""
        for name in folder_results2:
            if name in ["Result2", "Results2", "result2", "results2"]:
               name_results2 = name
               break 
            elif "results2" in name:
               name_results2 = name
               break
        if name_results2 != "":
            os.chdir(name_results2)
            # print(name_results2)
            json_path = glob.glob("*.json", recursive = True)
            if len(json_path) != 0:
                name_json = json_path[0]
                name_json = f"\\\\?\\{os.path.abspath(name_json)}"
                with open(name_json, 'r', encoding="utf8") as f:
                    data = json.load(f)
                for name in data:
                    labels = json.dumps(data[name]['labels'])
                    if "whole-body" in labels:
                        cnt_whole_body += 1
                    if "top" in labels or "bottom" in labels:
                        cnt_else += 1
                        
                # print(cnt_whole_body)
                # print(cnt_else)
            os.chdir(folder_path)
        os.chdir(dpath)
    with open(f"{dpath}/whole_body_{cnt_whole_body}_else_{cnt_else}.txt", "w") as f:
        pass