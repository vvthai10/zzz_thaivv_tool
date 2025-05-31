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
    
    level2_pattern = os.path.join(dpath, "*", "New")
    new_folder_path_list = glob.glob(level2_pattern, recursive=False)
    for _,new_folder_path in enumerate(tqdm(new_folder_path_list)):
            
        file_path_list = glob.glob(f"{new_folder_path}/*/count_images*", recursive=False)
        map_result = {}
        for file_path in file_path_list:
            maker_name = os.path.basename(os.path.dirname(file_path))
            total_image = int(os.path.basename(file_path).split(".txt")[0].split("_")[-1])
            map_result[maker_name] = total_image
        
        combined_count_file_path = os.path.join(new_folder_path, "total_count.txt")
        with open(combined_count_file_path, "w") as f:
            for maker in map_result:
                f.write(f"{maker} {map_result[maker]}\n")      
        
    