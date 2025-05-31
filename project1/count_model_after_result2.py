#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 23:43:48 2023

@author: minhvo 
"""


# python make_video_folders.py "/Users/minhvo/Google Drive/My Drive/z/CaoVietThanh/GAP_Activewear and Workout Clothes For Men/"
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

folder_error = []
models_special1 = []
total_cnt_models_special1 = 0
# 0: copy results1
# 1: run results1
# 2: run results2
# 3: copy results2
# 4: run results3
print("===================== COUNT 2 TIMES ========================")
dpath = args.dpath
os.chdir(dpath)
folderList = glob.glob("*", recursive = True)
folderList = sorted(folderList)
for foldername in folderList:
    print(foldername)
    if "desktop.ini" == foldername or ".txt" in foldername or "results" in foldername or ".gsheet" in foldername or foldername == 'mistake' or foldername == 'results1_special2' or foldername == 'results1_special3'  or foldername == 'results1_special4' or foldername == 'results1_special5' or foldername == 'results1_special6' or foldername == 'results2' or foldername == 'results1' or foldername == 'results3' or foldername == 'results4' or foldername == 'results5' or foldername == 'results6' or foldername == 'videos' or "results" in foldername or "special" in foldername:
        continue
    
    # cd foldername
    try:
        os.chdir(foldername)
    except:
        continue
    
    try:
        os.chdir("special1")
        cnt_models_special1 = 0
        filelist = glob.glob("*", recursive = True)
        for fn in filelist:
            if fn == "desktop.ini" or "txt" in fn or "rm" == fn or "mistake" == fn or "special1" == fn or "_-1" in fn or "_0" in fn:
                continue
            cnt_models_special1 += 1
            
        total_cnt_models_special1 += cnt_models_special1
        models_special1.append({
            "name": foldername,
            "cnt": cnt_models_special1,
        })
        os.chdir('../')
    except:
        continue
    
    os.chdir('../')
    
with open(dpath+"/"+"models_special1_after_test_" + str(total_cnt_models_special1) + ".txt", "w") as f:
    for obj in models_special1:
        f.write(f"{obj['name']} {obj['cnt']}\n")

