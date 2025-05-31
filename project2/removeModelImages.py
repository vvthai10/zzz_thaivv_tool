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

# 0: copy results1
# 1: run results1
# 2: run results2
# 3: copy results2
# 4: run results3


dpath = args.dpath
os.chdir(dpath)

folderList = glob.glob("*", recursive = True)
folderList = sorted(folderList)
for foldername in folderList:
    print(foldername)

    os.chdir(foldername)
    filelist = glob.glob("*", recursive = True)
    filelist = sorted(filelist)
    nfiles = len(filelist)
    for i in tqdm(range(nfiles)):
        f = filelist[i]
        fn = dpath+"/"+foldername+"/"+f
        try:
            os.remove(fn)
        except:
            continue

    os.chdir("tmp")
    filelist = glob.glob("*", recursive = True)
    filelist = sorted(filelist)
    nfiles = len(filelist)

    for i in tqdm(range(nfiles)):
        f = filelist[i]
        fn = dpath+"/"+foldername+"/tmp/"+f
        n2 =  dpath+"/"+foldername+"/" + f
        shutil.copy(fn, n2)

    # os.chdir(foldername+"/tmp")
    # filelist = glob.glob("*", recursive = True)
    # filelist = sorted(filelist)
    # nfiles = len(filelist)

    # for i in tqdm(range(nfiles)):
    #     f = filelist[i]

    #     dot = f.find(".")
    #     if f.find(").") > -1:
    #         fn = dpath+"/"+foldername+"/"+f
    #         os.remove(fn)
    #         continue
    
    #     sp = f.find("_")
    #     try:
    #         garmentId = int(f[:sp]) 
    #     except:
    #         print(f)
    #         exit()
    #     try:
    #         imageId = int(f[sp+1:f.find(".")])
    #     except:
    #         print(f)
    #         exit()  

    #     if imageId>0:
    #         fn = dpath+"/"+foldername+"/tmp/"+f
    #         os.remove(fn)
        

    os.chdir('../../')

