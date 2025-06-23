from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
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
import json

def get_images_files(dpath):
    print("Get image_dict")
    image_dict = {}
    parent_path = os.path.abspath(dpath)
    
    image_pattern = os.path.join(parent_path, "**", "*.[pj][np][g]*")
    all_images = glob.glob(image_pattern, recursive=True)
    
    results_path = os.path.join(parent_path, "Results")
    images = [img for img in all_images if not img.startswith(results_path)]
    
    for image_path in images:
        rel_path = os.path.relpath(image_path, parent_path)
        branch_folder = rel_path.split(os.sep)[-2]
        special_name = None
        if "special" in branch_folder:
            special_name = branch_folder
            branch_folder = rel_path.split(os.sep)[-3]
        
        if branch_folder != "Results":
            if branch_folder not in image_dict:
                parent_name = '\\'.join(rel_path.split(os.sep)[:-1])
                if special_name != None:
                    parent_name = '\\'.join(rel_path.split(os.sep)[:-2])
                image_dict[branch_folder] = {
                    "parents_folder_name": parent_name,
                    "main": [],
                }
            filename = os.path.basename(image_path)
            if special_name != None:
                if special_name not in image_dict[branch_folder].keys():
                    image_dict[branch_folder][special_name] = []
                image_dict[branch_folder][special_name].append(filename)
            else:
                image_dict[branch_folder]["main"].append(filename)
    return image_dict

def check_json_images(dpath):
    images_dict = get_images_files(dpath)
    results_folder = os.path.join(dpath, "Results")
    
    # Chia làm 2 loại error: main, special
    error_main = {}
    error_special = {}
    
    json_pattern = os.path.join(results_folder, "**", "*.json")
    json_list = glob.glob(json_pattern, recursive=True)
    
    for _, json_path in enumerate(tqdm(json_list)):
        # if "brax_men_jackets" not in json_path:
        #     continue
        rel_path = os.path.relpath(json_path, results_folder)
        folder_parts = rel_path.split(os.sep)
        branch_folder = folder_parts[0]
        if branch_folder not in images_dict.keys():
            continue
        obj_name = "main"
        if "special" in rel_path:
            obj_name = folder_parts[1]
            
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for img, _ in data.items():
                    if img not in images_dict[branch_folder][obj_name]:
                        parent_folder = images_dict[branch_folder]["parents_folder_name"]
                        if obj_name == "main":
                            if parent_folder not in error_main:
                                error_main[parent_folder] = []
                            error_main[parent_folder].append(img)
                        else:
                            if parent_folder not in error_special:
                                error_special[parent_folder] = []
                            error_special[parent_folder].append(img)
        except json.JSONDecodeError:
            print(f"Can't read json file {json_path}")
            exit()
        except Exception as e:
            print(f"Can't read json file {json_path}: {str(e)}")
            exit()
            
    return error_main, error_special

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()


if __name__ == '__main__':
    dpath = args.dpath
    error_main, error_special = check_json_images(dpath)
    
    results_path = os.path.join(dpath, "Results")
    
    error_file_path = os.path.join(results_path, "error.txt")
    if error_main:
        with open(error_file_path, 'w', encoding='utf-8') as file:
            # file.write("Các thư mục có nội dung JSON không khớp với hình ảnh thực tế:\n")
            for folder, missing_images in error_main.items():
                file.write(f"{folder}\n")
                for img in missing_images:
                    file.write(f"  - {img}\n")
    else:
        print("Không tìm thấy lỗi nào trong main!!!")
        
    error_file_path = os.path.join(results_path, "error_special.txt")
    if error_special:
        with open(error_file_path, 'w', encoding='utf-8') as file:
            # file.write("Các thư mục có nội dung JSON không khớp với hình ảnh thực tế:\n")
            for folder, missing_images in error_special.items():
                file.write(f"{folder}\n")
                for img in missing_images:
                    file.write(f"  - {img}\n")
    else:
        print("Không tìm thấy lỗi nào trong special!!!")
    