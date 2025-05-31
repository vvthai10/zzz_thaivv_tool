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

parent_folder = args.dpath
string_to_remove = "_147_147_147"

for root, dirs, files in os.walk(parent_folder, topdown=False):
    for folder_name in dirs:
        full_path = os.path.join(root, folder_name)
        
        # Kiểm tra nếu tên folder có chứa chuỗi cần xóa
        if string_to_remove in folder_name:
            # Tạo tên mới bằng cách xóa chuỗi cần xóa
            new_name = folder_name.replace(string_to_remove, "")
            new_full_path = os.path.join(root, new_name)

            # Đổi tên folder
            os.rename(full_path, new_full_path)
