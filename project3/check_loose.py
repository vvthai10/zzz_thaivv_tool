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


WARNING_PATH = "G:\\My Drive\\viettechtools\\Project 3 - Warning"

LIST_PHASE_PATHS = [
    "G:\\.shortcut-targets-by-id\\1sMl0hDz5LmdFqQ_BKOWCt-gdlWYZgubk\\Project 3 - Group1 - Phase1-10\\Phase5 - Job 88\\round1\\Dinh Dat\\Kham/",
]
   
parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()
            

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Check Loose<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    LIST_PHASE_PATHS = [dpath]
    for phase_path in LIST_PHASE_PATHS:
        temp = "\\".join(phase_path.split("\\")[3:])
        print(temp)
        os.chdir(phase_path)
        list_folder_branch = glob.glob("*", recursive=True)
        name_folder = []
        cnt_losses = []
        path_images = []
        for folder_branch in list_folder_branch:
            print(folder_branch)
            if "desktop.ini" == folder_branch or ".txt" in folder_branch:
                continue
            
            folder_path = os.path.join(phase_path, folder_branch)
            os.chdir(folder_path)
            
            # Lấy tất cả các file hình ảnh
            list_images_files = glob.glob("*.jpg", recursive = True)
        
            # Lấy thông tin json file
            json_file = None
            folder_results2 = glob.glob("*results2*", recursive = True)
            if len(folder_results2) != 0:
                results2_path = os.path.join(folder_path, "*results2*")
                # Lấy thông tin các file json:
                list_json_path = glob.glob(f"{results2_path}\\*.json", recursive = True)
                # print(list_json_path)
                if len(list_json_path) != 0:
                    json_file_path = f"\\\\?\\{os.path.abspath(list_json_path[0])}"  # Thêm tiền tố \\?\ để hỗ trợ đường dẫn dài
                    with open(json_file_path, 'r', encoding='utf-8') as file:
                        json_file = json.load(file)
                             
            # TH1: Ko có file json, đưa tất cả các hình vào folder warning 
            if json_file == None:
                if len(list_images_files) == 0:
                    continue
                name_folder.append(folder_branch)     
                cnt_losses.append(len(list_images_files))  
                full_path_images = [folder_path + "\\" + image_path for image_path in list_images_files]
                path_images.extend(full_path_images)    
            else:
                child_loss_image_path = []
                cnt_loss = 0
                for image in list_images_files:
                    if image in json_file:
                        if 'labels' in json_file[image] and isinstance(json_file[image]['labels'], dict) and not json_file[image]['labels']:
                            cnt_loss += 1
                            child_loss_image_path.append(image)
                    else:
                        cnt_loss += 1
                        child_loss_image_path.append(image)
                
                if cnt_loss * 100 / len(list_images_files) < 15:
                    continue
                name_folder.append(folder_branch)     
                cnt_losses.append(cnt_loss)  
                full_path_images = [folder_path + "\\" + image_path for image_path in child_loss_image_path]
                path_images.extend(full_path_images)    
        
        warning_path = f"{WARNING_PATH}\\{temp}"
        if os.path.exists(warning_path):
            shutil.rmtree(warning_path)
        os.makedirs(warning_path) 
        with open(warning_path+'\\warning.txt', 'w') as file:
            for item1, item2 in zip(name_folder, cnt_losses):
                file.write(f"{item1} {item2}\n")
                
        # Copy images
        for _,image_path in enumerate(tqdm(path_images)):
            image_path_split = image_path.split("\\")[3:]
            temp_image_path = "\\".join(image_path_split)
            new_image_path = f"{WARNING_PATH}\\{temp_image_path}"
            parent_path = '\\'.join(new_image_path.split("\\")[:-1])
            if not os.path.exists(parent_path):
                os.makedirs(parent_path) 
            shutil.copy2(image_path, new_image_path)
            
            
            
        
        