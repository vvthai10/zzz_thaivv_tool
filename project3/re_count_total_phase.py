import os
import glob
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pathlib import Path
import numpy as np
from pathlib import Path  
import shutil 
import argparse
from tqdm import tqdm
import coloredlogs
import logging
import json

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

# Set up logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(levelname)s: %(message)s')


if __name__ == "__main__":
    logger.info("run to remake image in project 3")
    dpath = args.dpath
    
    # file_path_list = glob.glob(f"{dpath}/*/count_images*", recursive=False)
    # map_result = {}
    # for _,file_path in enumerate(tqdm(file_path_list)):
    #     if "\\New\\" in file_path:
    #         continue
    #     maker_name = os.path.basename(os.path.dirname(file_path))
    #     total_image = int(os.path.basename(file_path).split(".txt")[0].split("_")[-1])
    #     map_result[maker_name] = total_image
    
    # combined_count_file_path = os.path.join(dpath, "total_count.txt")
    # with open(combined_count_file_path, "w") as f:
    #     for maker in map_result:
    #         f.write(f"{maker} {map_result[maker]}\n")      
    
    count_each_folder = []
    total_count = 0
    
    maker_list = os.listdir(dpath)
    for maker in maker_list:
        maker_path = os.path.join(dpath, maker)
        if os.path.isdir(maker_path):
            images_list = glob.glob(os.path.join(maker_path, '**', '*.jpg'), recursive=True)
            count_each_folder.append({
                "folder": maker,
                "count": len(images_list) 
            })
            total_count += len(images_list)
    
    path_save_file = f"{dpath}/count_images_{total_count}.txt"
    with open(path_save_file, "w") as f:
        for obj in count_each_folder:
            f.write(f"{obj['folder']} {obj['count']}\n")
    