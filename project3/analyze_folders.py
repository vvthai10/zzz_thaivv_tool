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

IS_SPECIAL_1 = False
PATH_TO_CHECK = ""
ROOT_NAME = ""

def get_list_img_concat(list_image, have_image_0, have_image_neg_1):
    # default là lấy cả chuỗi, nếu mà có ảnh 0 thì xóa hết ảnh -1
    list_results = []
    if have_image_0 and have_image_neg_1:
        for image in list_image:
            if "_-1" not in image:
                list_results.append(image)
    else:
        list_results = list_image
    return list_results

def handle_make_images(file_list, path_save):
    id_file_list = set()
    for item in file_list:
        if "_" not in item or "armani" in item or ".txt" in item or "low" in item or "rm" == item or "pecial" in item or "Copy" in item or "copy" in item:
            continue
        number = item.split('_')[0]
        try:
            test = int(number)
            id_file_list.add(number)
        except:
            continue
    try:
        id_file_list = sorted(list(id_file_list), key=lambda x: int(x))
    except:
        print("Error ", id_file_list)
        
    n_id_files = len(id_file_list)
    if n_id_files == 0:
        print("LEN ID ", id_file_list, file_list)
        return
    
    # if os.path.isdir(path_save):
    #     shutil.rmtree(path_save)
    os.mkdir(path_save)
        
    
    root_path_project3 = path_save
    
    for i in tqdm(range(n_id_files)):
        id_file = id_file_list[i]
        img_list_with_id = glob.glob(f"{id_file}_*", recursive = True)
        
        image_0 =  glob.glob(f"{id_file}_0*", recursive = True)
        image_neg_1 =  glob.glob(f"{id_file}_-1*", recursive = True)
        have_image_0 = True if len(image_0) > 0 else False
        have_image_neg_1 = True if len(image_neg_1) > 0 else False
            
        list_temp = []
        for img in img_list_with_id:
            if "V" not in img and "v" not in img and '.mp4' not in img:
                list_temp.append(img)
        
        if len(list_temp) == 0:
            continue
        
        try:
            img_list_with_id = sorted(list_temp, key=lambda x: int(x.split('_')[1].split('.')[0]))
        except:
            print("[ERROR 72] list_temp = ", list_temp)
        
        
        list_concat = get_list_img_concat(img_list_with_id, have_image_0, have_image_neg_1)
        
        path_check = f"{PATH_TO_CHECK}/{id_file}.jpg"
        if IS_SPECIAL_1 and os.path.exists(path_check):
            continue
        
        # TODO: read images and concat images
        path_save_concat_image = f"{root_path_project3}/{id_file}.jpg"
        try:
            # images = [Image.open(img_path) for img_path in list_concat]
            images = []
            for img_path in list_concat:
                img = np.array(Image.open(img_path))
                if len(img.shape) == 2:
                    img = Image.open(img_path).convert('RGBA')
                elif img.shape[2] == 2:
                    img = Image.open(img_path).convert('RGBA')
                elif img.shape[2] == 4:
                    new_img = img[:, :, :3] 
                    new_img[img[:, :, 3] == 0] = [255, 255, 255]
                    img = Image.fromarray(new_img.astype('uint8'), 'RGB')
                else:
                    img = Image.open(img_path)
                images.append(img)
            width, height = images[0].size
            concat_image = Image.new("RGB", (width * len(images), height))
            x_offset = 0
            for img in images:
                if img.size != (width, height):
                    img = img.resize((width, height))
                concat_image.paste(img, (x_offset, 0))
                x_offset += width
        except:
            # images = []
            # for img_path in list_concat:
            #     print(img_path)
            #     images.append(Image.open(img_path))
            # width, height = images[0].size
            # concat_image = Image.new("RGB", (width * len(images), height))
            # x_offset = 0
            # for img in images:
            #     if img.size != (width, height):
            #         img = img.resize((width, height))
            #     concat_image.paste(img, (x_offset, 0))
            #     x_offset += width
            print("Warn 95", list_concat , " with concat list ", list_concat)
            continue
        # TODO: save images
        concat_image.save(path_save_concat_image)

def get_json_files_in_results2(parent_folder):
    results2_path = os.path.join(parent_folder, "**", "results2", "*.json")
    json_files = glob.glob(results2_path, recursive=True)
    return json_files

def check_missing_images(folder_names, parent_folder):
    print("check_missing_images")
    result = []
    
    json_files = glob.glob(os.path.join(parent_folder, "**", "results2", "*.json"), recursive=True)
    for json_file in json_files:
        if "\\Results\\" in json_file:
            continue
        folder_name = os.path.basename(os.path.dirname(os.path.dirname(json_file)))
        worker_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(json_file)))))
        
        if folder_name in folder_names and worker_name == ROOT_NAME:
            with open(json_file, 'r', encoding="utf-8") as f:
                json_data = json.load(f)
                image_names_in_json = set(json_data.keys())
                unmatched_files = []
                folder_path = f"{parent_folder}/{ROOT_NAME}_{folder_name}"
                if os.path.exists(folder_path):
                    print("CHECK FOLDER DOUBLE NAME: ", folder_path)
                    for file in os.listdir(folder_path):
                        if ".ini" in file or ".txt" in file:
                            continue
                        if os.path.isfile(os.path.join(folder_path, file)) and file not in image_names_in_json:
                            unmatched_files.append(file)
                        
                    result.append({
                        "folder_name": f"{ROOT_NAME}_{folder_name}",
                        "missing_count": len(unmatched_files),
                        "missing_files": unmatched_files
                    })
                else:
                    folder_path = f"{parent_folder}/{folder_name}"
                    if os.path.exists(folder_path):
                        for file in os.listdir(folder_path):
                            if ".ini" in file or ".txt" in file:
                                continue
                            if os.path.isfile(os.path.join(folder_path, file)) and file not in image_names_in_json:
                                unmatched_files.append(file)
                        
                    result.append({
                        "folder_name": folder_name,
                        "missing_count": len(unmatched_files),
                        "missing_files": unmatched_files
                    })
        elif worker_name == ROOT_NAME:
            print("NOTE HAVE FILE JSON BUT NOT HAVE FOLDER: ", folder_name)
    return result

def generate_tobelabel_file_and_folder(analysis_result, tobelabel_path):
    print("generate_tobelabel_file_and_folder")
    tobelabel_txt_path = os.path.join(tobelabel_path, "Tobelabel.txt")
    
    tobelabel_folder = os.path.join(tobelabel_path, "ToBeLabeled")
    if not os.path.exists(tobelabel_folder):
        # shutil.rmtree(tobelabel_folder)
        os.makedirs(tobelabel_folder)
    
    with open(tobelabel_txt_path, "a", encoding="utf-8") as tobelabel_file:
        for entry in tqdm(analysis_result):
            folder_name = entry["folder_name"]
            unmatched_files = entry["missing_files"]

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


parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

output_path = "G:\\.shortcut-targets-by-id\\1sMl0hDz5LmdFqQ_BKOWCt-gdlWYZgubk\\Project 3 - Group1 - Phase1-10\\Phase5 - Job 88/"
# output_path = "D:\\fix_viettech/Results/" 
# output_path = "D:\\fix_viettech\\Phase1 - Job 90/"

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Make images for project 3<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    ROOT_NAME = dpath.split("\\")[-1]
    # ROOT_NAME = ROOT_NAME[:-1]
    
    # Make folder in output
    output_name_path = output_path
    # if os.path.exists(output_name_path):
    #     shutil.rmtree(output_name_path)
    # os.mkdir(output_name_path)
    
    os.chdir(dpath)
    folderList = glob.glob("*", recursive = True)
    folderList = sorted(folderList)
    count_each_folder = []
    total_count = 0
    for foldername in folderList:
        print(foldername)
        
        if "desktop.ini" == foldername or ".txt" in foldername or ".gsheet" in foldername or "results" in foldername or "rm" == foldername or "low" in foldername or "Copy" in foldername or "copy" in foldername or "rm" == foldername or "pecial" in foldername:
            continue
        
        # TODO: Handle each child folder
        folder_path = os.path.join(dpath, foldername)
        os.chdir(folder_path)
        
        # TODO: handle to images
        file_list = glob.glob("*_*", recursive = True)
        file_list = sorted(file_list)
        save_path = f"{output_name_path}/{foldername}"
        if os.path.exists(save_path):
            root_name = dpath.split("\\")[-1]
            # root_name = root_name[:-1]
            save_path = f"{output_name_path}/{ROOT_NAME}_{foldername}"
        handle_make_images(file_list, save_path)
        
        # TODO: handle to special folder
        # special_folder_list = glob.glob("special*/", recursive = True)
        # if len(special_folder_list)  > 0:
        #     # if os.path.isdir(f"{output_name_path}/{foldername}"):
        #     #     shutil.rmtree(f"{output_name_path}/{foldername}")
        #     # os.mkdir(f"{output_name_path}/{foldername}")
        #     if not os.path.isdir(f"{output_name_path}/{foldername}"):
        #         os.mkdir(f"{output_name_path}/{foldername}")
        # for special_folder in special_folder_list:
        #     if "1" in special_folder:
        #         IS_SPECIAL_1 = True
        #     os.chdir(special_folder)
        #     file_list = glob.glob("*_*", recursive = True)
        #     PATH_TO_CHECK = f"{output_name_path}/{foldername}"
        #     print(PATH_TO_CHECK)
        #     handle_make_images(file_list,f"{output_name_path}/{foldername}/{special_folder}")
        #     IS_SPECIAL_1 = False
        #     os.chdir("../")
            
        
        # TODO: Count
        path_count = f"{output_name_path}/{foldername}/"
        if os.path.exists(path_count):
            count = 0
            list_file_jpg = os.listdir(path_count)
            for file in list_file_jpg:
                if ".jpg" in file:
                    count += 1
                
            count_each_folder.append({
                "folder": foldername,
                "count": count 
            })
            total_count += count
        os.chdir(dpath) 
        
    result = check_missing_images(folderList, output_path)
    generate_tobelabel_file_and_folder(result,output_path)
         
                
        