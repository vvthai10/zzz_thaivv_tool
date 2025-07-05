"""
    @author: thaivv
    @description: dùng để kiểm tra file all.json. 
        - Xem có hình nào trong files này nhưng lại khong có hình ở ngoài
        - Xem có hình nào trong folder nhưng lại không có trong files
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
import json
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()


if __name__ == "__main__":
    print("================= CHECK LOST ===================")
    dpath = args.dpath

    # Get all.json path
    try:
        all_path = glob.glob(os.path.join(dpath, "**","all.json"))[0]
    except:
        print("Not existed file all.json")
        exit()
    # Read content
    with open(all_path, 'r') as f1:
        all_data = json.load(f1)
        
    image_name_all_json = []
    for obj_image in all_data:
        image_name_all_json.append(obj_image[0].split(".")[0])
        
    # Get images list
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp"]
    # Use glob with multiple extensions
    image_list = []
    for ext in image_extensions:
        image_list.extend(glob.glob(os.path.join(dpath, "**", ext), recursive=True))
        
    image_name_folder = []
    for image_path in image_list:
        if "Result" in image_path or "results1" in image_path:
            continue
        image_name = Path(image_path).parts[-1].split(".")[0]
        if " (1)" in image_name:
            image_name = image_name.replace(" (1)", "(1)")
        image_name_folder.append(image_name)
        
    image_not_in_folder = list(set(image_name_all_json) - set(image_name_folder))
    image_not_in_json = list(set(image_name_folder) - set(image_name_all_json))
    
    if len(image_not_in_folder) > 0:
        print("contain image_not_in_folder")
        save_path_image_not_in_folder = os.path.join(dpath, "image_not_in_folder.txt")
        with open(save_path_image_not_in_folder, 'w', encoding='utf-8') as fp:
            for image in image_not_in_folder:
                fp.write("%s\n" % image)
    
    if len(image_not_in_json) > 0:
        print("contain image_not_in_json")
        save_path_image_not_in_json = os.path.join(dpath, "image_not_in_json.txt")
        with open(save_path_image_not_in_json, 'w', encoding='utf-8') as fp:
            for image in image_not_in_json:
                fp.write("%s\n" % image)
                
                
    # Write all2.json (exclude image not in folder)
    new_all_data = []
    if len(image_not_in_folder) > 0:
        for obj_image in all_data:
            name = obj_image[0].split(".")[0]
            if name not in image_not_in_folder:
                new_all_data.append(obj_image)
                
    all2_path = all_path.replace("all.json", "all2.json")
    with open(all2_path, 'w') as f:
        json.dump(new_all_data, f, indent=4)