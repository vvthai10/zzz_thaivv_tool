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


save_path = "D:\\fix_viettech\Minh Sang"

if __name__ == "__main__":
    dpath = args.dpath
    
    special_folder_list = glob.glob(f"{dpath}/*/special*", recursive=False)
    
    map_count_image_in_garment_folder = {}
    total_count = 0

    for special in special_folder_list:
        brand = special.split("\\")[-2]
        special_name = special.split("\\")[-1]

        new_brand = os.path.join(save_path, brand)
        print(new_brand)
        if not os.path.exists(new_brand):
            os.mkdir(new_brand)

        shutil.copytree(special, os.path.join(new_brand,special_name))
        
        images_list = glob.glob(f"{special}/**/*.jpg", recursive=True)
        total_count += len(images_list)
        map_count_image_in_garment_folder[brand] = len(images_list)
        
    sorted_data = dict(sorted(map_count_image_in_garment_folder.items(), key=lambda x: x[0].lower()))
    path_save_file = f"{save_path}/count_images_{total_count}.txt"
    with open(path_save_file, "w") as f:
        for garment in sorted_data:
            f.write(f"{garment} {map_count_image_in_garment_folder[garment]}\n")