'''
TODO:
    - Tạo 2 mảng object:
        - 1 của project 3: name folder và path
        - 1 của project 1: name của folder và path và name của folder cha (vì sẽ có trường hợp trùng folder)
        
    - For từng folder của project 3: 
        - Tìm folder trong các folder project 1:
            - Lấy thông tin file results2/labels
            - Lấy thông tin id
'''

import os
import glob
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from pathlib import Path
import numpy as np
from pathlib import Path  
import shutil 
import argparse
from tqdm import tqdm
import coloredlogs
import logging
import json

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
parser.add_argument("project3_path")
args = parser.parse_args()

# Set up logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(levelname)s: %(message)s')


# project3_path = "G:\\.shortcut-targets-by-id\\1OykkoAyFDokBetyw74SuGYrCSciw2abg\\Project 3 - Group5 - Phase41-50\\Phase42 - Job 51/"
# project3_path = "D:\\fix_viettech/Results/" 

def find_path_in_project3(maker_project1):
    '''
        TODO: Tìm folder có cùng maker bên project1. Sẽ chỉ có 2 trường hợp:
            - Cùng cấp bên ngoài 
            - Nẳm trong 1 cấp (roundx)
    '''
    
    level1_pattern = os.path.join(project3_path, maker_project1)
    if os.path.isdir(level1_pattern):
        return level1_pattern
    
    level2_pattern = os.path.join(project3_path, "*", maker_project1)
    level2 = glob.glob(level2_pattern, recursive=False)
    if len(level2) > 0:
        for path in level2:
            if "/New/" not in path:
                return path
    
    logger.error(f"[56] can't find folder have maker project 1 {maker_project1}")
    exit()

def make_list_path_garment_project3(path_in_project3):
    pattern = os.path.join(path_in_project3, "**/*.jpg")
    
    set_folder_garment = set()
    folder_list = []
    all_paths = glob.glob(pattern, recursive=True)   
    
    for path in all_paths:
        if ".ini" in path or ".json" in path or "result" in path or "correction" in path or "special" in path or "Special" in path or "SPECIAL" in path:
            continue
        name = os.path.basename("/".join(path.split("/")[:-1]))
        if name == "New":
            continue
        if name not in set_folder_garment:
            folder_info = {
                'name': name,
                'path': "/".join(path.split("/")[:-1])
            }
            folder_list.append(folder_info)
            set_folder_garment.add(name)

    return folder_list

def re_make_images(list_path_garment_project3, path_project1):
    '''
        TODO: Hàm này sẽ check xem folder garment trong project3:
            - Có folder đó bên project1?
            - Có tồn tại file result2/labels.json
            - Tạo thêm các ảnh mới dựa trên thông tin trong file labels
            - Tạo lại các folder special
    '''
    for obj in list_path_garment_project3:
        garment_name, garment_path_project3 = obj["name"], obj["path"]
        
        # if garment_name != "elvineclothing_men_shirts":
        #     continue
        
        # TODO: Có folder đó bên project1?
        garment_path_project1 = os.path.join(path_project1, garment_name)
        if not os.path.exists(garment_path_project1):
           logger.error(f"[94] not found {garment_path_project1}") 
           exit()
        
        # TODO: Có tồn tại file result2/labels.json
        path_json_project3 = None
        json_project3 = glob.glob(os.path.join(garment_path_project3, f"**/*.json"))
        if len(json_project3) > 1:
            print(json_project3)
        if len(json_project3) > 0:
            path_json_project3 = json_project3[0]
            
        list_id_in_json_project3 = []
        if path_json_project3:
            try:
                with open(path_json_project3, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    for img_key, _ in data.items():
                        list_id_in_json_project3.append(int(img_key.split(".")[0]))
                list_id_in_json_project3.sort()
                            
            except json.JSONDecodeError:
                logger.error(f"[116] can't read json file {path_json_project3}")
                exit()
        
        # TODO: - Tạo thêm các ảnh mới dựa trên thông tin trong file labels
        process_path = garment_path_project1
        
        # TODO: Get image ids
        images_list = glob.glob(f"{process_path}/*_*", recursive=True)
        image_ids = set()
        for img_path in images_list:
            img_name = os.path.basename(img_path)
            if "_" not in img_name or "armani" in img_name or ".txt" in img_name or "low" in img_name or "rm" == img_name or "pecial" in img_name or "Copy" in img_name or "copy" in img_name or "V1" in img_name:
                continue
            img_id = img_name.split("_")[0]
            try:
                nb_img_id = int(img_id)
                image_ids.add(nb_img_id)
            except:
                continue
            
        # TODO: sorted it
        try:
            image_ids = sorted(list(image_ids), key=lambda x: int(x))
        except:
            logger.error(f"[144] can't sorted {image_ids}")
            
        list_image_id_remake = []
        for img in image_ids:
            if img not in list_id_in_json_project3:
                list_image_id_remake.append(img)
                
        if len(list_image_id_remake) > 0:
            logger.info(f"handle remake image {garment_name}")
            handle_remake_image(garment_path_project1, garment_path_project3, list_image_id_remake)
                
        # TODO: - Tạo lại các folder special
        for sub in ["special1", "special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
            garment_path_special_project1 = os.path.join(garment_path_project1, sub)
            if os.path.exists(garment_path_special_project1):
                # project3_new_folder_path = os.path.join(garment_path_project3, "New")
                # if not os.path.exists(project3_new_folder_path):
                #     os.mkdir(project3_new_folder_path)
                logger.info(f"handle remake special image {garment_name} {sub}")
                handle_remake_image_special(garment_path_special_project1, None, sub, image_ids)
                
                
    # TODO: Make a file count 
    maker_name = path_project1.split("/")[-2]
    try:
        project3_root_new_folder_path = os.path.join(project3_path, "New")
        project3_new_folder_of_maker_path = os.path.join(project3_root_new_folder_path, maker_name)
        list_renew_images = glob.glob(f"{project3_new_folder_of_maker_path}/**/*.jpg", recursive=True)

        total_count = 0
        map_count_image_in_garment_folder = {}
        for img_path in list_renew_images:
            renew_garment_name = img_path.split("/")[-2]
            if "special" in renew_garment_name:
                renew_garment_name = img_path.split("/")[-3]
            if renew_garment_name not in map_count_image_in_garment_folder.keys():
                map_count_image_in_garment_folder[renew_garment_name] = 0
            map_count_image_in_garment_folder[renew_garment_name] += 1
            total_count += 1
        
        sorted_data = dict(sorted(map_count_image_in_garment_folder.items(), key=lambda x: x[0].lower()))
        
        path_save_file = f"{project3_new_folder_of_maker_path}/count_images_{total_count}.txt"
        with open(path_save_file, "w") as f:
            for garment in sorted_data:
                f.write(f"{garment} {map_count_image_in_garment_folder[garment]}\n")
    except:
        pass
                
                
def handle_remake_image(garment_path_project1, garment_path_project3, list_image_id_remake):
    project3_root_new_folder_path = os.path.join(project3_path, "New")
    if not os.path.exists(project3_root_new_folder_path):
        os.mkdir(project3_root_new_folder_path)
    
    [maker_name, garment_name] = garment_path_project1.split("/")[-2:]
    project3_new_folder_of_maker_path = os.path.join(project3_root_new_folder_path, maker_name)
    if not os.path.exists(project3_new_folder_of_maker_path):
        os.mkdir(project3_new_folder_of_maker_path)
    
    project3_new_folder_path = os.path.join(project3_new_folder_of_maker_path, garment_name)
    if os.path.exists(project3_new_folder_path):
        shutil.rmtree(project3_new_folder_path)
    os.mkdir(project3_new_folder_path)
    
    for _, id in enumerate(tqdm(list_image_id_remake)):
        list_image = glob.glob(f"{garment_path_project1}/{id}_*", recursive=True)

        # TODO: Add image same id from folder special1
        list_special1_image = []
        if os.path.exists(os.path.join(garment_path_project1, "special1")):
            list_special1_image = glob.glob(f"{garment_path_project1}/special1/{id}_*", recursive=True)
            
        list_process_image = []
        list_special1_name_image = []
        existed_img_0 = False
        existed_img_neg_1 = False
        for img_path in [*list_image, *list_special1_image]:
            img = os.path.basename(img_path)
            if "V" not in img and "v" not in img and '.mp4' not in img and ".txt" not in img:
                list_process_image.append(img)
                
                if "special1" in img_path:
                    list_special1_name_image.append(img)
                    
                # Check img is _0 or _-1
                if "_0" in img:
                    existed_img_0 = True
                if "_-1" in img:
                    existed_img_neg_1 = True
                    
        if len(list_process_image) == 0:
            continue
        try:
            list_process_image = sorted(list_process_image, key=lambda x: int(x.split('_')[1].split('.')[0]))
        except:
            logger.warning(f"[197] sorted {list_process_image}")
            
        list_make_image = get_list_img_concat(list_process_image, existed_img_0, existed_img_neg_1)
        # TODO: concat and save
        handle_concat_save_image(garment_path_project1, 
                                project3_new_folder_path, 
                                id,
                                list_make_image, 
                                list_special1_name_image)
        
def handle_remake_image_special(garment_path_special_project1, project3_new_folder_path, type_special, main_image_ids):
    project3_root_new_folder_path = os.path.join(project3_path, "New")
    if not os.path.exists(project3_root_new_folder_path):
        os.mkdir(project3_root_new_folder_path)
    
    [maker_name, garment_name] = garment_path_special_project1.split("/")[-3:-1]
    
    project3_new_folder_of_maker_path = os.path.join(project3_root_new_folder_path, maker_name)
    if not os.path.exists(project3_new_folder_of_maker_path):
        os.mkdir(project3_new_folder_of_maker_path)
    
    project3_new_folder_garment_path = os.path.join(project3_new_folder_of_maker_path, garment_name)
    if not os.path.exists(project3_new_folder_garment_path):
        os.mkdir(project3_new_folder_garment_path)
    
    project3_special_new_folder_path = os.path.join(project3_new_folder_garment_path, type_special)
    if os.path.isdir(project3_special_new_folder_path):
        shutil.rmtree(project3_special_new_folder_path)
    os.mkdir(project3_special_new_folder_path)

    # TODO: Read all image in special:
    images_list = glob.glob(f"{garment_path_special_project1}/*_*", recursive=True)
    image_ids = set()
    for img_path in images_list:
        img_name = os.path.basename(img_path)
        if "_" not in img_name or "armani" in img_name or ".txt" in img_name or "low" in img_name or "rm" == img_name or "pecial" in img_name or "Copy" in img_name or "copy" in img_name or "V1" in img_name:
            continue
        img_id = img_name.split("_")[0]
        try:
            nb_img_id = int(img_id)
            if type_special == "special1" and nb_img_id in main_image_ids:
                continue
            image_ids.add(nb_img_id)
        except:
            continue

    # TODO: sorted it
    try:
        image_ids = sorted(list(image_ids), key=lambda x: int(x))
    except:
        logger.error(f"[144] can't sorted {image_ids}")
    
    for _, id in enumerate(tqdm(image_ids)):
        list_image = glob.glob(f"{garment_path_special_project1}/{id}_*", recursive=True)
        list_process_image = []
        existed_img_0 = False
        existed_img_neg_1 = False
        for img_path in list_image:
            img = os.path.basename(img_path)
            if "V" not in img and "v" not in img and '.mp4' not in img and ".txt" not in img:
                list_process_image.append(img)
                    
                # Check img is _0 or _-1
                if "_0" in img:
                    existed_img_0 = True
                if "_-1" in img:
                    existed_img_neg_1 = True
                    
        if len(list_process_image) == 0:
            continue
        try:
            list_process_image = sorted(list_process_image, key=lambda x: int(x.split('_')[1].split('.')[0]))
        except:
            logger.warning(f"[197] sorted {list_process_image}")

        list_make_image = get_list_img_concat(list_process_image, existed_img_0, existed_img_neg_1)
        # TODO: concat and save
        handle_concat_save_image(garment_path_special_project1, 
                                project3_special_new_folder_path, 
                                id,
                                list_make_image, 
                                [])     
        
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

def handle_concat_save_image(garment_path_project1, project3_new_folder_path, id_img, list_make_image, list_special1_name_image):
    path_to_save = f"{project3_new_folder_path}/{id_img}.jpg"
    try:
        images = []
        for img_name in list_make_image:
            img_path = os.path.join(garment_path_project1, img_name)
            if img_name in list_special1_name_image:
                img_path = os.path.join(garment_path_project1, f"special1/{img_name}")
                
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
        logger.warning("[225]", list_make_image , " with concat list ", list_make_image)
        return
    concat_image.save(path_to_save)
        
if __name__ == "__main__":
    logger.info("run to remake image in project 3")
    dpath = args.dpath
    project3_path = args.project3_path
    # project3_path = "G:\\.shortcut-targets-by-id\\1g3WkCvNoD7IgPMIfFdWUU3sZrFXxR0Nv\\Project 3 - Group8 - Phase71-80\\Phase78 - Job 102/"
    
    maker_project1 = dpath.split("/")[-2]
    path_in_project3 = find_path_in_project3(maker_project1)
    logger.info(path_in_project3)
    list_path_garment_project3 = make_list_path_garment_project3(path_in_project3)
    re_make_images(list_path_garment_project3, dpath)
    
    
    
    
    
    
