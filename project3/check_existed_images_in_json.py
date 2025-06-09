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

def get_image_files(parent_folder):
    print("Get image_dict")
    image_dict = {}
    parent_path = os.path.abspath(parent_folder)
    
    image_pattern = os.path.join(parent_path, "**", "*.[pj][np][g]*")
    all_images = glob.glob(image_pattern, recursive=True)
    
    results_path = os.path.join(parent_path, "Results")
    images = [img for img in all_images if not img.startswith(results_path)]
    
    for image_path in images:
        rel_path = os.path.relpath(image_path, parent_path)
        top_folder = rel_path.split(os.sep)[-2]
        
        if top_folder != "Results":
            if top_folder not in image_dict:
                image_dict[top_folder] = {
                    "parents_folder_name": '\\'.join(rel_path.split(os.sep)[:-1]),
                    "images": []
                }
            filename = os.path.basename(image_path)
            image_dict[top_folder]["images"].append(filename)
    return image_dict

def check_json_images(parent_folder):
    results_folder = os.path.join(parent_folder, "Results")
    actual_images = get_image_files(parent_folder)
    print("Check json_images")
    
    if not os.path.exists(results_folder):
        return {"error": "Folder Results không tồn tại!"}, []
    
    # Biến missing_folders thành dictionary: key là folder, value là mảng các ảnh thiếu
    missing_folders = {}
    
    json_pattern = os.path.join(results_folder, "**", "*.json")
    all_json_files = glob.glob(json_pattern, recursive=True)
    
    for _, json_path in enumerate(tqdm(all_json_files)):
        
        if "gabrielahearst_men_suiting" not in json_path:
            continue
        rel_path = os.path.relpath(json_path, results_folder)
        folder_parts = rel_path.split(os.sep)
        target_folder = folder_parts[0]
        print(target_folder)
        if target_folder not in actual_images:
            continue
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for img_key, img_data in data.items():
                    if img_key not in actual_images[target_folder]["images"]:
                        # Nếu folder chưa có trong missing_folders, khởi tạo mảng rỗng
                        if actual_images[target_folder]["parents_folder_name"] not in missing_folders:
                            missing_folders[actual_images[target_folder]["parents_folder_name"]] = []
                        # Thêm tên ảnh thiếu vào mảng của folder tương ứng
                        missing_folders[actual_images[target_folder]["parents_folder_name"]].append(img_key)
                        
        except json.JSONDecodeError:
            print(f"Can't read json file {json_path}")
            exit()
        except Exception as e:
            print(f"Can't read json file {json_path}: {str(e)}")
            exit()
    
    return missing_folders

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

if __name__ == '__main__':
    dpath = args.dpath
    missing_folders = check_json_images(dpath)
    
    results_path = os.path.join(dpath, "Results")
    error_file_path = os.path.join(results_path, "error.txt")
    
    if missing_folders:
        with open(error_file_path, 'w', encoding='utf-8') as file:
            # file.write("Các thư mục có nội dung JSON không khớp với hình ảnh thực tế:\n")
            for folder, missing_images in missing_folders.items():
                file.write(f"{folder}\n")
                for img in missing_images:
                    file.write(f"  - {img}\n")
    else:
        print("Không tìm thấy lỗi nào!!!")