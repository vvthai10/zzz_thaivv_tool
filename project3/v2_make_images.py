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

IS_SPECIAL_1 = False
EXISTED_SPECIAL_1 = False
IS_MAIN_FOLDER = False
PATH_TO_CHECK = ""

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
    
    if os.path.isdir(path_save):
        shutil.rmtree(path_save)
    os.mkdir(path_save)
        
    root_path_project3 = path_save
    
    for i in tqdm(range(n_id_files)):
        id_file = id_file_list[i]
        img_list_with_id = glob.glob(f"{id_file}_*", recursive = True)

        # TODO: Get image with same id from special1
        list_file_special_1_same_id = []
        if IS_MAIN_FOLDER and EXISTED_SPECIAL_1:
            list_file_special_1 = glob.glob(f"special1/{id_file}_*", recursive=True)
            for f in list_file_special_1:
                list_file_special_1_same_id.append(f.split("\\")[-1])
                img_list_with_id.append(f.split("\\")[-1])

        image_0 =  glob.glob(f"{id_file}_0*", recursive = True)
        image_neg_1 =  glob.glob(f"{id_file}_-1*", recursive = True)
        have_image_0 = True if len(image_0) > 0 else False
        have_image_neg_1 = True if len(image_neg_1) > 0 else False
            
        list_temp = []
        for img in img_list_with_id:
            if "V" not in img and "v" not in img and '.mp4' not in img and ".txt" not in img:
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
            for img_name in list_concat:
                img_path = img_name
                if img_path in list_file_special_1_same_id:
                    img_path = f"special1/{img_path}"
                    
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

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

# output_path = "G:\\.shortcut-targets-by-id\\1ZVmA_ba9_hdC2lVbB5gzcH-WEiRKHYNo\\Project 3 - Group16 - Phase151-160\\Phase153 - Job 173/"
output_path = "D:\\fix_viettech/project 3/175/" 

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Make images for project 3<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    
    root_name = dpath.split("\\")[-1]
    root_name = root_name[:-1]
    
    # Make folder in output
    output_name_path = output_path+root_name
    if os.path.exists(output_name_path):
        shutil.rmtree(output_name_path)
            
    os.mkdir(output_name_path)
    
    os.chdir(dpath)
    folderList = glob.glob("*", recursive = True)
    folderList = sorted(folderList)
    count_each_folder = []
    total_count = 0
    for foldername in folderList:
        print(foldername)
        
        if "desktop.ini" == foldername or ".txt" in foldername or ".gsheet" in foldername or "results" in foldername or "rm" == foldername or "low" in foldername or "Copy" in foldername or "copy" in foldername or "rm" == foldername or "special" in foldername.lower():
            continue
        
        # TODO: Handle each child folder
        folder_path = os.path.join(dpath, foldername)
        os.chdir(folder_path)
        
        # TODO: handle to images
        file_list = glob.glob("*_*", recursive = True)
        file_list = sorted(file_list)
        IS_MAIN_FOLDER = True
        
        EXISTED_SPECIAL_1 = False
        is_folder_special_1 = glob.glob("special1")
        if len(is_folder_special_1) > 0:
            EXISTED_SPECIAL_1 = True
            
        handle_make_images(file_list, f"{output_name_path}/{foldername}")
        IS_MAIN_FOLDER = False
        
        # TODO: handle to special folder
        special_folder_list = glob.glob("special*/", recursive = True)
        if len(special_folder_list)  > 0:
            # if os.path.isdir(f"{output_name_path}/{foldername}"):
            #     shutil.rmtree(f"{output_name_path}/{foldername}")
            # os.mkdir(f"{output_name_path}/{foldername}")
            if not os.path.isdir(f"{output_name_path}/{foldername}"):
                os.mkdir(f"{output_name_path}/{foldername}")
            
        for special_folder in special_folder_list:
            if "1" in special_folder:
                IS_SPECIAL_1 = True
            os.chdir(special_folder)
            file_list = glob.glob("*_*", recursive = True)
            PATH_TO_CHECK = f"{output_name_path}/{foldername}"
            print(PATH_TO_CHECK)
            handle_make_images(file_list,f"{output_name_path}/{foldername}/{special_folder}")
            IS_SPECIAL_1 = False
            os.chdir("../")
            
        
        # TODO: Count
        path_count = f"{output_name_path}/{foldername}/**/*.jpg"
        if os.path.exists(f"{output_name_path}/{foldername}"):
            count = 0
            list_file_jpg = glob.glob(f"{path_count}", recursive = True)
            for file in list_file_jpg:
                if ".jpg" in file:
                    count += 1
                
            count_each_folder.append({
                "folder": foldername,
                "count": count 
            })
            total_count += count
        
        os.chdir(dpath) 
        
    # TODO: save in folder member
    path_save_file = f"{output_name_path}/count_images_{total_count}.txt"
    with open(path_save_file, "w") as f:
        for obj in count_each_folder:
            f.write(f"{obj['folder']} {obj['count']}\n")
    
        
                
        