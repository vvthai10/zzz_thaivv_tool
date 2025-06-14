"""
    @author: thaivv
    Desc: Use to create images, which get from project1. Image with same id concat together
    Update(ver 2):
        Can process parallel
"""

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
from concurrent.futures import ProcessPoolExecutor, as_completed

parser = argparse.ArgumentParser()
parser.add_argument("project1_path")
parser.add_argument("output_path")
args = parser.parse_args()

def get_makers_project1(project1_path):
    contents = os.listdir(project1_path)
    results = []
    for content in contents:
        if ".ini" in content:
            continue
        results.append(content)
        
    return content

def handle_create_images(images, src_path, des_path, is_main_folder, have_special1):
    id_list = set()
    for img in images:
        if "_" not in img or ".txt" in img or\
            "low" in img or "rm" == img or\
            "pecial" in img or "Copy" in img or "copy" in img:
            continue
        
        number = img.split("_")[0]
        try:
            id_list.add(int(number))
        except:
            continue
        
    try:
        id_list = sorted(list(id_list), key=lambda x: int(x))
    except:
        print("error:", id_list)
    
    len_ids = len(id_list)
    if len_ids == 0:
        print("len id:", id_list, images)
        return
    
    if os.path.isdir(des_path):
        shutil.rmtree(des_path)
    os.mkdir(des_path)
    
    for i in tqdm(range(len_ids)):
        id_file = id_list[i]
        imgs_list_by_id = glob.glob(os.path.join(src_path, f"{id_file}_*"), recursive=True)
        
        # TODO: get images with same id from special1
        imgs_special_1_same_id = []
        if is_main_folder and have_special1:
            imgs_special_1 = glob.glob(os.path.join(src_path, f"special1/{id_file}_*"), recursive=True)
            for img in imgs_special_1:
                
    
    
    

def handle_make_for_each_maker(output_maker_path, project1_maker_path):
    # TODO: If existed => remove
    if os.path.exists(output_maker_path):
        shutil.rmtree(output_maker_path)
    os.mkdir(output_maker_path)
    
    # TODO: handle each branch in maker
    # 2 parts:
    # main_folder
    # special_folder
    branch_folders = glob.glob(os.path.join(project1_maker_path, "*"), recursive=True)
    branch_folders = sorted(branch_folders)
    count_each_folder = []
    total_count = 0
    for branch_folder in branch_folders:
        print(branch_folder)
        
        if "desktop.ini" == branch_folder or ".txt" in branch_folder or ".gsheet" in branch_folder or "results" in branch_folder or "rm" == branch_folder or "low" in branch_folder or "Copy" in branch_folder or "copy" in branch_folder or "rm" == branch_folder or "pecial" in branch_folder:
            continue
        
        branch_folder_path = os.path.join(project1_maker_path, branch_folder)
        images = glob.glob(os.path.join(branch_folder_path, "*_*"), recursive=True)
        
        is_main_folder=True
        have_special1=False
        if len(glob.glob(os.path.join(project1_maker_path,"special1"))) > 0:
            have_special1=True
        
        des_path = os.path.join(output_maker_path,branch_folder)
        handle_create_images(
            images=images,
            des_path=des_path,
            is_main_folder=is_main_folder,
            have_special1=have_special1,
        )
        
        # TODO: Handle special folder
        special_folders = glob.glob(os.path.join(branch_folder_path, "special*"), recursive=True)
        # Handle case if not existed des_path   
        if len(special_folders) > 0:
            if not os.path.isdir(des_path):
                os.mkdir(des_path)
                
        is_main_folder=False
        for special_folder in special_folders:
            have_special1=False
            if "1" in special_folder:
                have_special1=True
            images = glob.glob(os.path.join(branch_folder_path, f"{special_folder}/*_*"), recursive=True)
            handle_create_images(
                images=images,
                des_path=os.path.join(des_path, special_folder),
                is_main_folder=is_main_folder,
                have_special1=have_special1
            )
            
            
        # TODO: count images 
        

def process_parallel(output_path, project1_path, max_workers=4):
    folders = get_makers_project1(project1_path)
    folder_paths = [os.path.join(project1_path, folder) for folder in folders]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_folder, folder) for folder in folder_paths]

        for future in as_completed(futures):
            try:
                result = future.result()
                print("✅ Result:", result)
            except Exception as e:
                print("❌ Error in processing:", e)



if __name__ == "__main__":
    project1_path = args.project1_path
    output_path = args.output_path
    
    makers = get_makers_project1(project1_path)