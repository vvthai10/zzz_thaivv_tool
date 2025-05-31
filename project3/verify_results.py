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

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

IMAGE_EXTENSIONS = ('*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.webp')

def find_folders_with_images(src_root):
    print("find_folders_with_images")
    folders_with_images = set()
    
    for extension in IMAGE_EXTENSIONS:
        for file_path in glob.glob(f"{src_root}/**/{extension}", recursive=True):
            folder_path = os.path.dirname(file_path)
            if "special" in folder_path or  "correction" in folder_path or  "result" in folder_path:
                folder_path = os.path.dirname(folder_path)
            folders_with_images.add(folder_path)
    return folders_with_images

def copy_folders_to_destination(folders, src_root):
    print("copy_folders_to_destination")
    new_folders = set()
    for folder in tqdm(folders):
        dest_folder = os.path.join(src_root, folder.split("\\")[-1])
        # print(f"Copying folder: {folder} -> {dest_folder}")
        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)
        shutil.copytree(folder, dest_folder) #, dirs_exist_ok=True
        new_folders.add(dest_folder)
    
    return new_folders

def analyze_folders_with_results(folders):
    print("analyze_folders_with_results")
    analysis_result = []

    for folder in folders:
        results2_path = os.path.join(folder, "results2")
        if not os.path.exists(results2_path):
            continue
        
        json_file_path = None
        for file in os.listdir(results2_path):
            if file.endswith(".json"):
                json_file_path = os.path.join(results2_path, file)
                break
        if not json_file_path:
            print(f"Folder {folder} not have file json")
            continue
        
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            try:
                json_data = json.load(json_file)
                image_names_in_json = set(json_data.keys())
            except Exception as e:
                print(f"Cannot read file json {results2_path}: {e}")
                continue
            
        parent_folder = os.path.dirname(results2_path)
        unmatched_files = []
        for file in os.listdir(parent_folder):
            if ".ini" in file or ".txt" in file:
                continue
            if os.path.isfile(os.path.join(parent_folder, file)) and file not in image_names_in_json:
                unmatched_files.append(file)
        
        analysis_result.append({
            "folder_name": os.path.basename(folder),
            "unmatched_count": len(unmatched_files),
            "unmatched_files": unmatched_files,
        })
        if len(unmatched_files) != 0:
            print(f"Phân tích folder {folder}: {len(unmatched_files)} file không có trong JSON")
            print(unmatched_files)
        

    return analysis_result

def generate_tobelabel_file_and_folder(analysis_result, tobelabel_path):
    print("generate_tobelabel_file_and_folder")
    tobelabel_txt_path = os.path.join(tobelabel_path, "Tobelabel.txt")
    
    tobelabel_folder = os.path.join(tobelabel_path, "ToBeLabeled")
    if os.path.exists(tobelabel_folder):
        shutil.rmtree(tobelabel_folder)
    os.makedirs(tobelabel_folder)
    
    with open(tobelabel_txt_path, "w", encoding="utf-8") as tobelabel_file:
        for entry in tqdm(analysis_result):
            folder_name = entry["folder_name"]
            unmatched_files = entry["unmatched_files"]

            if not unmatched_files:
                continue
            
            tobelabel_file.write(f"Folder: {folder_name}\n")
            tobelabel_file.write(f"List of images without labels:\n")
            tobelabel_file.writelines(f"- {file}\n" for file in unmatched_files)
            tobelabel_file.write("\n")
            
            source_folder = os.path.join(tobelabel_path, folder_name)
            for file in unmatched_files:
                source_file_path = os.path.join(source_folder, file)
                target_folder = os.path.join(tobelabel_folder, folder_name)
                target_file_path = os.path.join(target_folder, file)
                
                os.makedirs(target_folder, exist_ok=True)
                if os.path.exists(source_file_path):
                    shutil.copy2(source_file_path, target_file_path)
                else:
                    print(f"File not existed: {source_file_path}")

def delete_folders_before(dpath, folders):
    print("delete_folders_before")
    if not os.path.exists(dpath):
        return

    for folder in before_folders:
        item_path = os.path.join(dpath, folder)

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Analysis Result for project 3<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    before_folders = os.listdir(dpath)
    folders = find_folders_with_images(dpath)
    folders = copy_folders_to_destination(folders, dpath)
    delete_folders_before(dpath, before_folders)
    # folders = ['D:\\fix_viettech\\Phase1 - Job 90\\woolworths_men_chinos']
    analysis_result = analyze_folders_with_results(folders)
    generate_tobelabel_file_and_folder(analysis_result,dpath)
    
    