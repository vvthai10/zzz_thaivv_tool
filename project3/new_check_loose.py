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
import json

DEFAULT_WARNING_PATH = "/content/drive/MyDrive/viettechtools/Project 3 - Warning"

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Check Loose<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    main_path = "/".join(dpath.split("/")[5:])
    warning_path = os.path.join(DEFAULT_WARNING_PATH, main_path)
    if not os.path.isdir(warning_path):
        os.makedirs(warning_path)
    
    folder_branch_list = glob.glob(os.path.join(dpath,"*"), recursive=True)
    warning_map = {}
    for folder_branch in folder_branch_list:
        if "desktop.ini" in folder_branch or ".txt" in folder_branch:
            continue
        
        branch_name = folder_branch.split("/")[-1]
        print(branch_name)
        if branch_name not in warning_map.keys():
            # Sẽ có tối đa 2 obj main, special1
            warning_map[branch_name] = {}
            
        warning_branch_path = os.path.join(warning_path, branch_name)
        if not os.path.isdir(warning_branch_path):
            os.makedirs(warning_branch_path)
        
        # Lấy tất cả những nơi có folder results2
        results2_list = glob.glob(os.path.join(folder_branch,"**/*results2*"), recursive=True)
        for results2 in results2_list:
            
            warning_save_path = warning_branch_path
            obj_name = "main"
            # Sử lý trường hợp của special
            if "special" in results2:
                special_name = results2.split("/")[-2]
                warning_special_path = os.path.join(warning_branch_path, special_name)
                if not os.path.isdir(warning_special_path):
                    os.makedirs(warning_special_path)
                warning_save_path = warning_special_path
                obj_name = special_name
                
            warning_map[branch_name][obj_name] = {
                "total": 0,
                "miss": 0,
                "list": []
            }
            
            try:
                # Lấy thông tin file json
                json_path = glob.glob(os.path.join(results2,"*.json"), recursive=True)[0]
                with open(json_path, 'r', encoding='utf-8') as file:
                    json_file = json.load(file)
                    
                # Lấy thông tin images tại folder cùng cấp results2
                base_path = os.path.dirname(results2)
                images_list = glob.glob(os.path.join(base_path,"*.jpg"), recursive=True)
                warning_map[branch_name][obj_name]["total"] = len(images_list)
                # Đối chiếu với trong results2:
                for image in images_list:
                    image_name = image.split("/")[-1]
                    if image_name in json_file:
                        if 'labels' in json_file[image_name] and isinstance(json_file[image_name]['labels'], dict) and not json_file[image_name]['labels']:
                            warning_map[branch_name][obj_name]["miss"] += 1
                            # image_name = image.split("\\")[-1]
                            # new_image = os.path.join(warning_save_path, image_name)
                            # shutil.copy2(image, new_image) 
                            warning_map[branch_name][obj_name]["list"].append(image)
                    else:
                        warning_map[branch_name][obj_name]["miss"] += 1
                        
                        # image_name = image.split("\\")[-1]
                        # new_image = os.path.join(warning_save_path, image_name)
                        # shutil.copy2(image, new_image) 
                        warning_map[branch_name][obj_name]["list"].append(image)
            except:
                # Nếu không có json, đưa all ảnh vào Warning:
                base_path = os.path.dirname(results2)
                images_list = glob.glob(os.path.join(base_path,"*.jpg"), recursive=True)
                warning_map[branch_name][obj_name]["total"] = len(images_list)
                warning_map[branch_name][obj_name]["miss"] += len(images_list)
                warning_map[branch_name][obj_name]["list"] = images_list
                # for image in images_list:
                #     image_name = image.split("\\")[-1]
                #     new_image = os.path.join(warning_save_path, image_name)
                #     shutil.copy2(image, new_image) 
                #     warning_map[branch_name] += 1
            
            if warning_map[branch_name][obj_name]["miss"] * 100 / warning_map[branch_name][obj_name]["total"] >= 15:
                for image in warning_map[branch_name][obj_name]["list"]:
                    image_name = image.split("/")[-1]
                    new_image = os.path.join(warning_save_path, image_name)
                    shutil.copy2(image, new_image) 
            else:
                del warning_map[branch_name][obj_name]
    
    # File này sẽ phải chia ra 2 file
    # 1 cho special
    # 1 cho main
    with open(warning_path+'/warning.txt', 'w') as file:
        for branch_name in warning_map.keys():
            if "main" not in warning_map[branch_name].keys():
                continue
            count_miss = warning_map[branch_name]["main"]["miss"]
            file.write(f"{branch_name} {count_miss}\n")
    
    with open(warning_path+'/warning_special.txt', 'w') as file:
        for branch_name in warning_map.keys():
            for obj_name in warning_map[branch_name].keys():
                if obj_name == "main":
                    continue
                
                count_miss = warning_map[branch_name][obj_name]["miss"]
                file.write(f"{branch_name} {count_miss}\n")