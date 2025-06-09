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
    dpath = args.dpath
    arr_folder = []
    arr_count = []
    arr_child_folder = []
    arr_child_count = []
    
    warning_list = glob.glob(os.path.join(dpath,"**/warning.txt"), recursive=True)
    total_map = {}
    detail_map = {}
    for warning in warning_list:
        split = warning.split("\\")
        name_1, name_2 = split[-3], split[-2]
        
        total_map[name_1] = 0
        with open(warning, "r") as f:
            for line in f:
                parts = line.split(' ')
                strings = ''.join(parts[:-1])
                miss = int(parts[-1])
                
                total_map[name_1] += miss
                
                name_detail = f"{name_1} -- {name_2} -- {strings}"
                detail_map[name_detail] = miss
                
    with open(dpath+'\\warning.txt', 'w') as file:
        for key in total_map.keys():
            if total_map[key] == 0:
                continue
            file.write(f"{key}: {total_map[key]}\n")
                
    with open(dpath+'\\warning_detail.txt', 'w') as file:
        for key in detail_map.keys():
            if detail_map[key] == 0:
                continue
            file.write(f"{key}: {detail_map[key]}\n")
            
            
    # TODO: Handle special
    warning_list = glob.glob(os.path.join(dpath,"**/warning_special.txt"), recursive=True)
    total_map = {}
    detail_map = {}
    for warning in warning_list:
        split = warning.split("\\")
        name_1, name_2 = split[-3], split[-2]
        
        total_map[name_1] = 0
        with open(warning, "r") as f:
            for line in f:
                parts = line.split(' ')
                strings = ''.join(parts[:-1])
                miss = int(parts[-1])
                
                total_map[name_1] += miss
                
                name_detail = f"{name_1} -- {name_2} -- {strings}"
                detail_map[name_detail] = miss
                
    with open(dpath+'\\warning_special.txt', 'w') as file:
        for key in total_map.keys():
            if total_map[key] == 0:
                continue
            file.write(f"{key}: {total_map[key]}\n")
                
    with open(dpath+'\\warning_detail_special.txt', 'w') as file:
        for key in detail_map.keys():
            if detail_map[key] == 0:
                continue
            file.write(f"{key}: {detail_map[key]}\n")
                
    