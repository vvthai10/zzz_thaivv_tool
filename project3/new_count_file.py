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
    
    cnt_whole_body = 0
    cnt_else = 0
    
    json_file_list = glob.glob(os.path.join(dpath, "**/*.json"), recursive=True)
    cnt = 0
    for json_file in tqdm(json_file_list):
        
        child_cnt_whole_body = 0
        child_cnt_else = 0
        
        with open(json_file,'r', encoding="utf8") as f:
            data = json.load(f)
        for name in data:
            labels = json.dumps(data[name]['labels'])
            cnt = 0
            if "whole-body" in labels:
                cnt_whole_body += 1
                child_cnt_whole_body += 1
                cnt += 1
            if "top" in labels or "bottom" in labels:
                cnt_else += 1
                child_cnt_else += 1
                cnt += 1
                
            if cnt > 1:
                print("/".join(Path(json_file).parts[:-3]))
                print(name)
                
        if "Results" not in json_file and "results_merge" not in json_file:
            child_path = "/".join(Path(json_file).parts[:-3])
            with open(f"{child_path}/whole_body_{child_cnt_whole_body}_else_{child_cnt_else}.txt", "w") as f:
                pass
    
    print(f"whole_body_{cnt_whole_body}_else_{cnt_else}")
    with open(f"{dpath}/whole_body_{cnt_whole_body}_else_{cnt_else}.txt", "w") as f:
        pass
    