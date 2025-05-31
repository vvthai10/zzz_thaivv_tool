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

def update_json_images(parent_folder):
    results_folder = os.path.join(parent_folder, "Results")
    actual_images = get_image_files(parent_folder)
    print("Check and update json_images")
    
    if not os.path.exists(results_folder):
        print("Folder Results không tồn tại!")
        return
    
    json_pattern = os.path.join(results_folder, "**", "*.json")
    all_json_files = glob.glob(json_pattern, recursive=True)
    
    for json_path in tqdm(all_json_files):
        rel_path = os.path.relpath(json_path, results_folder)
        folder_parts = rel_path.split(os.sep)
        target_folder = folder_parts[0]
        
        # if "Claudiepierlot_Women_Dresses" not in json_path:
        #     continue
        
        if target_folder not in actual_images:
            continue
        
        try:
            # Đọc file JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Tạo một bản sao của data để chỉnh sửa
            updated_data = {}
            modified = False
            parents_folder_name = ""
            
            # Kiểm tra từng image_key
            for img_key, img_data in data.items():
                if img_key in actual_images[target_folder]["images"]:
                    # Nếu image_key tồn tại trong thư mục thực tế, giữ lại
                    updated_data[img_key] = img_data
                else:
                    # Nếu không tồn tại, đánh dấu là đã chỉnh sửa
                    modified = True
                    # print(img_key)
                    parents_folder_name = actual_images[target_folder]["parents_folder_name"]
            
            # Nếu có thay đổi, ghi lại file JSON
            if modified:
                # print(json_path.split("\\")[-2:])
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, ensure_ascii=False, indent=4)
                    
                root_json_path = dpath + parents_folder_name + "\\" + '\\'.join(json_path.split("\\")[-2:])
                with open(root_json_path, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, ensure_ascii=False, indent=4)
                # print(root_json_path)
                # exit()
                    
            else:
                # print(f"Không có thay đổi trong file: {json_path}")
                pass
                
        except json.JSONDecodeError:
            print(f"Không thể đọc file JSON {json_path}")
            continue
        except Exception as e:
            print(f"Lỗi khi xử lý file JSON {json_path}: {str(e)}")
            continue

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

if __name__ == '__main__':
    dpath = args.dpath
    update_json_images(dpath)