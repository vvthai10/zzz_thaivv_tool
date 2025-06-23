#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 23:43:48 2023

@author: minhvo 
"""


# python make_video_folders.py "/Users/minhvo/Google Drive/My Drive/z/CaoVietThanh/GAP_Activewear and Workout Clothes For Men/"
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

folder_error = []
models_special1 = []
total_cnt_models_special1 = 0
TOTAL_CNT_IMAGES = 0
IS_EXISTED_RESULTS = False
WARN_LOST_FILES = []

def format_all_file_folder_name(root_path: str):
    if IS_EXISTED_RESULTS:
        return
    job = root_path.split("\\")[-2].split(" ")[-1].split("_")[0]
    list_folder = os.listdir(root_path)
    # TODO: format name root folder
    print("Format name folder")
    for idx, folder in enumerate(tqdm(list_folder)):
        folder = list_folder[idx]
        if os.path.isdir(os.path.join(root_path, folder)):
            # new_folder = folder
            new_folder = folder.split("_")
            new_folder.insert(1, job)
            new_folder = "_".join(str(x) for x in new_folder)
            # print("Change ", folder, " to ", new_folder)
            if " " in new_folder: 
                new_folder = new_folder.replace(" ", "_")
            if "," in new_folder: 
                new_folder = new_folder.replace(",", "_")
            if "&" in new_folder: 
                new_folder = new_folder.replace("&", "_")
            if "@" in new_folder: 
                new_folder = new_folder.replace("@", "_")
            # if "-" in new_folder: 
            #     new_folder = new_folder.replace("-", "_")
            
            if folder != new_folder:
                os.rename(os.path.join(root_path, folder), os.path.join(root_path, new_folder))
    # TODO: format name folder specials 
    list_folder = os.listdir(root_path)
    print("Format name specials folder")
    for _, folder in enumerate(tqdm(list_folder)):
        if ".ini" in folder or "txt" in folder or "gsheet" in folder or ".DS_Store" in folder:
            continue

        folder_path = os.path.join(root_path, folder)
        list_child = os.listdir(folder_path)
        for child in list_child:
            # TODO: handle format special_x folder:
            if child == "special_1" or child == "Special 1" or child == "SPECIAL_1" or child == "SPECIAL 1" or child == "special":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special1"))
            if child == "special_2" or child == "Special 2" or child == "SPECIAL_2" or child == "SPECIAL 2":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special2"))
            if child == "special_3" or child == "Special 3" or child == "SPECIAL_3" or child == "SPECIAL 3":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special3"))
            if child == "special_4" or child == "Special 4" or child == "SPECIAL_4" or child == "SPECIAL 4":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special4"))
            if child == "special_5" or child == "Special 5" or child == "SPECIAL_5" or child == "SPECIAL 5":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special5"))
            if child == "special_6" or child == "Special 6" or child == "SPECIAL_6" or child == "SPECIAL 6":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special6"))
            if child == "special_7" or child == "Special 7" or child == "SPECIAL_7" or child == "SPECIAL 7":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special7"))
            if child == "special_8" or child == "Special 8" or child == "SPECIAL_8" or child == "SPECIAL 8":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special8"))
          
    # TODO: format file name: --1 -> -1 V1 .mp4 --> V1.mp4
    list_folder = os.listdir(root_path)
    print("Format name files")
    for _, folder in enumerate(tqdm(list_folder)):
        if ".ini" in folder or "txt" in folder or "gsheet" in folder  or ".DS_Store" in folder:
            continue

        folder_path = os.path.join(root_path, folder)
        list_child = os.listdir(folder_path)
        for _, child in enumerate(tqdm(list_folder)):
            # TODO: handle special_x folder
            if child in ["special1","special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
                special_path = os.path.join(folder_path, child)
                special_files = os.listdir(special_path)
                for spe_file in special_files:
                    if ".ini" in spe_file or "rm" in spe_file  or "txt" in spe_file:
                        continue
                    if "_0" in spe_file or "_-1" in spe_file:
                        name_file = spe_file.split(".")[0]
                        check_files_garment = glob.glob(special_path + "/" + name_file + "*", recursive = True)
                        if len(check_files_garment) > 1:
                            ("Warn 81 name ", folder_path, spe_file)
                    new_spe_file = spe_file
                    if " " in new_spe_file:
                        new_spe_file = new_spe_file.replace(" ", "")
                    if "-" in new_spe_file and new_spe_file.find("_-") == -1:
                        new_spe_file = new_spe_file.replace("-", "_")
                    if "(" in new_spe_file or "--" in new_spe_file or not "_" in new_spe_file:
                        print("Warn 88 name ", folder_path, new_spe_file)
                    
                    if spe_file != new_spe_file:
                        print("Format special file name ", spe_file, new_spe_file)
                        os.rename(os.path.join(special_path, spe_file), os.path.join(special_path, new_spe_file))
                continue
            
            if ".ini" in child or "rm" in child or ".txt" in child:
                continue
            if "_0" in child or "_-1" in child:
                name_file = child.split(".")[0]
                check_files_garment = glob.glob(folder_path + "/" + name_file + "*", recursive = True)
                if len(check_files_garment) > 1:
                    ("Warn 81 name ", folder_path, child)
            new_child = child
            if " " in new_child:
                new_child = new_child.replace(" ", "")
            if "-" in new_child and new_child.find("_-") == -1:
                new_child = new_child.replace("-", "_")
            if "(" in new_child or "--" in new_child or not "_" in new_child or "_" not in new_child:
                print("Warn 88 name ", folder_path, new_child)
            
            if child != new_child:
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, new_child))

def link_and_save_image(path_name: str, format_file: list):
    global TOTAL_CNT_IMAGES
    try:
        try:
            os.chdir(path_name)
        except Exception:
            print(f"Do not find {path_name}")
            return
            
        filelist = glob.glob("*", recursive = True)
        filelist = sorted(filelist)
        nfiles = len(filelist)
        
        ta = []
        sub_ta = []
        o_gid = -1
        maxSubImage = 0
        print('Tabling files... ')
        for i in tqdm(range(nfiles)):
            f = filelist[i]
            if "txt" in f or f == 'special and mistake.gsheet' or f == "desktop.ini" or f == "special"or f == "SPECIAL_6" or f == "SPECIAL_2" or f == "special_1" or f == "SPECIAL_1" or f == "SPECIAL 1" or f == "special1" or f == 'special2' or f == "low_res" or f == "Special" or f == "SPECIAL" or  f == "Doubt" or  f == "videos" or f == "mistake" or f == "rm" or f == "mistake.txt" or f == "special.txt":
                continue
            if os.path.isdir(f):
                continue

            dot = f.find(".")
            ## Add format file
            if f[dot:] not in format_file:
                format_file.append(f[dot:])
                
            if f[dot:] == ".webm" or f[dot:] == ".mp4" or f[dot:] == ".mkv" or f[dot:] == ".mp3" or f[dot:] == ".mov" or f[dot:] == ".ts" or f[dot:] == ".txt":
                continue
                
            if f.find(").") > -1:
                fn = dpath+"/"+foldername+"/"+f
                if path_name != ".":
                    fn = dpath+"/"+foldername+"/"+path_name+"/"+f
                print("[ALERT 130 - Remove file] ",fn)
                os.remove(fn)
                continue
        
            sp = f.find("_")
            try:
                temp = f[:sp]
                temp = temp.replace("`", "")
                garmentId = int(temp) 
            except:
                print("[ALERT 139] ", f)
                exit()
            try:
                imageId = int(f[sp+1:f.find(".")])
            except:
                print("[ALERT 144] ", f)
                exit()  

            try:
                img = cv2.imread(f)
            except:
                print(f)
                print("[ALERT 156] ", f)
            if img is None:
                print(f)
                folder_error.append(foldername)
                print("[ALERT 151] ", f)
                continue
            
            if garmentId != o_gid:
                o_gid = garmentId
                
                if len(sub_ta)==0:
                    sub_ta = [f]
                else:
                    ta.append([o_gid, sub_ta])  
                    maxSubImage = max(maxSubImage, len(sub_ta))
                    sub_ta = [f]     
            else:
                sub_ta.append(f)

        if len(ta) == 0 and o_gid != -1:
            ta.append([o_gid, sub_ta])  
            maxSubImage = len(sub_ta)
        elif o_gid != -1:
            ta.append([o_gid, sub_ta])  
            maxSubImage = max(maxSubImage, len(sub_ta)) 

        print('maxSubImage: {}'.format(maxSubImage))
        print('Num folder: {}'.format(len(ta)))  

        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        org2 = (400, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        
        img_h = 640
        img_w = 480
        
        
        # Xử lý các trường hợp move vào mistake -- Chỉ làm khi run results1:
        # chỉ có 1 người mẫu hoặc garment và ko có video
        list_handled = []
        if phase == 1:
            for ita in tqdm(ta):
                if len(ita[1]) <= 2:
                    if len(ita[1]) == 1:
                        f = ita[1][0]
                        sp = f.find("_")
                        garmentId = int(f[:sp]) 
                        list_check = glob.glob(f"{garmentId}_*")
                        # Trường hợp chỉ có 1 người mẫu or garment và ko có video --> move vào mistake không đếm cnt
                        if len(list_check) == 1:
                            list_handled.append(ita[1][0])
                            if not os.path.exists("rm"):
                                os.mkdir("rm")
                            shutil.move(ita[1][0], "rm/"+ita[1][0]) 
                    if len(ita[1]) == 2:
                        f = ita[1][0]
                        sp = f.find("_")
                        garmentId = int(f[:sp]) 
                        list_check = glob.glob(f"{garmentId}_*")
                        
                        cnt_garment = 0
                        for garment in ita[1]:
                            if "_-1" in garment or "_0" in garment:
                                cnt_garment += 1
                        # Nếu cả 2 là garment và ko có video thì move vào rm
                        if cnt_garment == 2 and len(list_check) == 2:
                            list_handled.append(ita[1][0])
                            if not os.path.exists("rm"):
                                os.mkdir("rm")
                            for garment in ita[1]:
                                shutil.move(garment, "rm/"+garment)
                
        if os.path.exists("rm") and len(os.listdir("rm")) == 0:
            os.rmdir("rm")
            
        check_duplicated = []
        # cnt: count của main folder + count của special(special1)
        cnt = 0
        for ita in ta:
            if ita[1][0] in list_handled:
                continue
            check_duplicated.append(ita[1][0].split("_")[0])
            cnt += 1 
        # print("root ", check_duplicated)
        try:
            os.chdir("special1")
            garment_special1 = []
            list_files_special1 = glob.glob("*", recursive = True)
            for f in list_files_special1:
                if f == 'special and mistake.gsheet' or f == "desktop.ini" or f == "special"or f == "SPECIAL_6" or f == "SPECIAL_2" or f == "special_1" or f == "SPECIAL_1" or f == "SPECIAL 1" or f == "special1" or f == 'special2' or f == "low_res" or f == "Special" or f == "SPECIAL" or  f == "Doubt" or  f == "videos" or f == "mistake" or f == "rm" or f == "mistake.txt" or f == "special.txt":
                    continue
                garmentID = f.split("_")[0]
                if garmentID in check_duplicated:
                    continue
                garment_special1.append(garmentID)
            # print("special ", garment_special1)
            cnt += len(list(set(garment_special1)))     
            os.chdir("../")
        except:
            pass
        
        size = (img_w*(maxSubImage+2), img_h)
        if phase == 1:
            if path_name in ["special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
                folderPath = dpath +f"/results1_{path_name}/"+foldername+"_{}".format(cnt)
            else:
                folderPath = dpath +"/results1/"+foldername+"_{}".format(cnt)
        elif phase == 2:
            folderPath = dpath +"/results2/"+foldername+"_{}".format(cnt)
        os.makedirs(folderPath, exist_ok=True)

        print('Making result!')
        for ita in tqdm(ta):
            # print(ita)
            if ita[1][0] in list_handled:
                continue
            bimg = np.zeros((img_h,img_w*(maxSubImage+4),3), dtype=np.uint8)

            f = ita[1][0]
            sp = f.find("_")
            garmentId = int(f[:sp]) 
            
            # Trường hợp là 1 ảnh garment + 1 video -> move vào result1
            if len(ita[1]) == 1:
                list_check = glob.glob(f"{garmentId}_*")
                if "_-1" in f or "_0" in f:
                    if phase == 1:
                        TOTAL_CNT_IMAGES += 1
                        for file in list_check:
                            shutil.copy(file, folderPath)
                    continue

            # Trường hợp chỉ có ảnh 2 garment +- video --> move vào result1
            if len(ita[1]) == 2:
                list_check = glob.glob(f"{garmentId}_*")
                cnt_garment = 0
                for img in list_check:
                    if f"{garmentId}_0" in img or f"{garmentId}_-1" in img:
                        cnt_garment += 1
                if cnt_garment == 2:
                    if phase == 1:
                        TOTAL_CNT_IMAGES += 1
                        for file in list_check:
                            shutil.copy(file, folderPath)
                    continue
            
            sp = f.find("_")
            garmentId = int(f[:sp]) 
            imageId = int(f[sp+1:f.find(".")])
            try:
                for i in range(0, len(ita[1])):
                    fn = dpath+"/"+foldername+"/"+path_name+"/"+ita[1][i]
                    f1 = ita[1][i]
                    sp = f1.find("_")
                    imageId = int(f1[sp+1:f1.find(".")])

                    # img = cv2.imread(fn) 
                    img = np.array(Image.open(fn))
                    if len(img.shape) == 2:
                        img = np.array(Image.open(fn).convert('RGBA'))
                    if img.shape[2] == 2:
                        img = np.array(Image.open(fn).convert('RGBA'))
                    if img.shape[2] == 4:
                        new_img = img[:, :, :3] 
                        new_img[img[:, :, 3] == 0] = [255, 255, 255]
                        img = new_img
                        
                        # img = np.array(Image.open(fn).convert('RGB'))

                    h,w,c = img.shape
                    
                    rimg = cv2.resize(img, [img_w, img_h])
                    f = '{}:{}x{}'.format(imageId,w,h)
                    rimg = cv2.putText(rimg, f, org, font,fontScale, color, thickness, cv2.LINE_AA)    
                    bimg[0:img_h, img_w*(imageId+1):img_w*(imageId+2)] = rimg  
            except Exception as err:
                if not no_images_output:
                    print("[ALERT 328] ", ita)
                    print(err)
                    exit()
            f = '{}'.format(garmentId)
            bimg = cv2.putText(bimg, f, org2, font,fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
            f = folderPath+"/{}.jpg".format(garmentId)
            
            if not no_images_output:
                im = Image.fromarray(bimg)
                im.save(f)
                TOTAL_CNT_IMAGES += 1
        
        # TODO: Copy all txt file to result1
        if phase == 1:
            list_txt_link =  glob.glob(f"*.txt")
            for _,txt_link in enumerate(tqdm(list_txt_link)):
                if not txt_link.split(".")[0].isnumeric() and not txt_link.split("_")[0].isnumeric():
                    continue
                shutil.copy(txt_link, folderPath)
        
        # TODO: Copy all video to result1, 3 type videos: mp4, mov, ts
        if phase == 1:
            if not no_images_output:
                list_videos = glob.glob(f"*.mp4")
                for video in list_videos:
                    shutil.copy(video, folderPath)
                list_videos = glob.glob(f"*.mov")
                for video in list_videos:
                    shutil.copy(video, folderPath)
                list_videos = glob.glob(f"*.ts")
                for video in list_videos:
                    shutil.copy(video, folderPath)   
                list_videos = glob.glob(f"*V1.webm")
                for video in list_videos:
                    shutil.copy(video, folderPath)    
                list_videos = glob.glob(f"*V1.mkv")
                for video in list_videos:
                    shutil.copy(video, folderPath)     
                
        
        list_files_existed = glob.glob(f"{folderPath}/*.jpg", recursive = True)
        if len(list_files_existed) < cnt:
            print("f[WARN LOST FILES] {folderPath}")
            WARN_LOST_FILES.append(folderPath)
        
    except Exception as e:
        print(e)
        pass

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()


# 0: copy results1
# 1: run results1
# 2: run results2
# 3: copy results2
# 4: run resuls3
phase = 1

print("=================== PHASE ", phase, " ========================")

no_images_output = True
if phase == 1:
    no_images_output = False
     
# copy text file from results1 to each folder
if phase == 0:
    print("Copy result files")
    dpath = args.dpath
    os.chdir(dpath)
    for result in ["results1", "results1_special2", "results1_special3", "results1_special4", "results1_special5", "results1_special6", "results1_special7", "results1_special8"]:
        if not os.path.isdir(dpath+result):
            continue
        print("Make folder ", result)
        os.chdir(dpath+result)
        folderList = glob.glob("*", recursive = True)
        if len(folderList) == 0:
            continue
        folderList = sorted(folderList)
        no_results = 0
        for foldername in tqdm(folderList):
            if ".gsheet" in foldername or foldername == "desktop.ini" or foldername == 'Special &Mistake.gsheet' or foldername == 'Special and Mistake.xlsx' or foldername == 'special & mistake.gsheet' or foldername == 'special and mistake.xlsx' or foldername == 'Special& mistake.gsheet' or foldername == 'Special& Mistake.gsheet' or foldername == 'Special&mistake (1).gsheet' or foldername == 'Special&Mistake.gsheet' or foldername == 'special and mistake .gsheet' or foldername == 'Special&mistake.gsheet' or foldername == "Special & Mistake.gsheet" or foldername == "special and mistake.gsheet" or foldername == "Clothing_collection.gsheet" or foldername == "Special& Mistakes.gsheet" or foldername == "Special and mistake.gsheet" or foldername == "Clothing collection.gsheet" or foldername == "special_and_mistake.xlsx" or foldername == "mistake&special.gsheet" or foldername == 'Clothing collection.xlsx' or foldername == 'SPECIAL AND MISTAKE.xlsx' or foldername == 'Clothing Collection.gsheet' or foldername == 'Special and mistake.gsheet' or foldername == 'Special and mistake.xlsx' or foldername == 'Special and Mistake.gsheet' or foldername == 'Mistake and Special .gsheet':
                continue          
            
            sp = foldername.rindex("_")
            foldername2 = foldername[:sp]
            if int(foldername[sp+1:])==0:
                continue
            
            os.chdir(foldername)
            txt_files = glob.glob("*.txt", recursive = True)
            for txt in txt_files:
                if txt.split(".")[0].isdigit():
                    continue
                n2 = dpath+"/"+foldername2+'/'+ str.lower(txt)
                if result == "results1_special2":
                    n2 = dpath+"/" + foldername2+'/' + "special2" + "/" + str.lower(txt)
                if result == "results1_special3":
                    n2 = dpath+"/" + foldername2+'/' + "special3" + "/" + str.lower(txt)
                if result == "results1_special4":
                    n2 = dpath+"/" + foldername2+'/' + "special4" + "/" + str.lower(txt)
                if result == "results1_special5":
                    n2 = dpath+"/" + foldername2+'/' + "special5" + "/" + str.lower(txt)
                if result == "results1_special6":
                    n2 = dpath+"/" + foldername2+'/' + "special6" + "/" + str.lower(txt)
                if result == "results1_special7":
                    n2 = dpath+"/" + foldername2+'/' + "special7" + "/" + str.lower(txt)
                if result == "results1_special8":
                    n2 = dpath+"/" + foldername2+'/' + "special8" + "/" + str.lower(txt)
                
                shutil.copy(txt, n2)
            if len(txt_files) == 0:
                print("folder with no results files: {}".format(foldername))
                no_results = no_results + 1
            os.chdir(dpath+result)
        print("no results: {}/{}".format(no_results, len(folderList)))
elif phase == 3:
    dpath = args.dpath
    os.chdir(dpath)
    os.chdir(dpath+'/results2')
    folderList = glob.glob("*", recursive = True)
    folderList = sorted(folderList)
    for foldername in tqdm(folderList):
        if foldername == "special and mistake.gsheet" or foldername == "Clothing_collection.gsheet" or foldername == "Special& Mistakes.gsheet" or foldername == "Special and mistake.gsheet" or foldername == "Clothing collection.gsheet" or foldername == "special_and_mistake.xlsx" or foldername == "mistake&special.gsheet" or foldername == 'Clothing collection.xlsx' or foldername == 'SPECIAL AND MISTAKE.xlsx' or foldername == 'Clothing Collection.gsheet' or foldername == 'Special and mistake.gsheet' or foldername == 'Special and mistake.xlsx' or foldername == 'Special and Mistake.gsheet' or foldername == 'Mistake and Special .gsheet':
            continue

        sp = foldername.rindex("_")
        foldername2 = foldername[:sp]
        if int(foldername[sp+1:])==0:
            continue
        
        os.chdir(foldername)
        txtfiles = glob.glob("*.txt", recursive = True)
        for txt in txtfiles:
            n2 = dpath+"/"+foldername2+'/'+txt
            shutil.copy(txt, n2)
        if len(txtfiles) == 0:
            print("folder with no results flies: {}".format(foldername))
        os.chdir(dpath+'/results2')
else:
    dpath = args.dpath

    if phase == 1:
        if os.path.exists(dpath +"/results1"):
            IS_EXISTED_RESULTS = True
        format_all_file_folder_name(dpath)

    format_file = []
    os.chdir(dpath)
    format_file = []
    if phase == 1:
        os.makedirs(dpath +"/results1", exist_ok=True)
        os.makedirs(dpath +"/results1_special2/", exist_ok=True)
        os.makedirs(dpath +"/results1_special3/", exist_ok=True)
        os.makedirs(dpath +"/results1_special4/", exist_ok=True)
        os.makedirs(dpath +"/results1_special5/", exist_ok=True)
        os.makedirs(dpath +"/results1_special6/", exist_ok=True)
        os.makedirs(dpath +"/results1_special7/", exist_ok=True)
        os.makedirs(dpath +"/results1_special8/", exist_ok=True)
    elif phase == 2:
        if os.path.isdir(dpath+"/results2"):
            shutil.rmtree(dpath +"/results2/")
        else:
            os.mkdir(dpath + "/results2")

    nMistakesFiles = 0
    folderList = glob.glob("*", recursive = True)
    folderList = sorted(folderList)
    for foldername in folderList:
        print(foldername)
        # if foldername not in ["vpo_167_men_jackets"]:
        #     continue
        if "desktop.ini" == foldername or ".txt" in foldername or "results" in foldername or ".gsheet" in foldername:
            continue
        folder_path = os.path.join(dpath, foldername)
        list_child = os.listdir(folder_path)
        for child in list_child:
            # TODO: handle format special_x folder:
            if child == "special_1" or child == "special 1" or child == "Special 1" or child == "SPECIAL_1" or child == "SPECIAL 1" or child == "special":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special1"))
            if child == "special_2" or child == "special 2" or child == "Special 2" or child == "SPECIAL_2" or child == "SPECIAL 2":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special2"))
            if child == "special_3" or child == "special 3" or child == "Special 3" or child == "SPECIAL_3" or child == "SPECIAL 3":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special3"))
            if child == "special_4" or child == "special 4" or child == "Special 4" or child == "SPECIAL_4" or child == "SPECIAL 4":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special4"))
            if child == "special_5" or child == "special 5" or child == "Special 5" or child == "SPECIAL_5" or child == "SPECIAL 5":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special5"))
            if child == "special_6" or child == "special 6" or child == "Special 6" or child == "SPECIAL_6" or child == "SPECIAL 6":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special6"))
            if child == "special_7" or child == "special 7" or child == "Special 7" or child == "SPECIAL_7" or child == "SPECIAL 7":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special7"))
            if child == "special_8" or child == "special 8" or child == "Special 8" or child == "SPECIAL_8" or child == "SPECIAL 8":
                os.rename(os.path.join(folder_path, child), os.path.join(folder_path, "special8"))
        if foldername == 'mistake' or foldername == 'results1_special2' or foldername == 'results1_special3'  or foldername == 'results1_special4' or foldername == 'results1_special5' or foldername == 'results1_special6' or foldername == 'results1_special7' or foldername == 'results1_special8' or foldername == 'results2' or foldername == 'results1' or foldername == 'results3' or foldername == 'results4' or foldername == 'results5' or foldername == 'results6' or foldername == 'videos':
            continue
        if "results" in foldername or "special" in foldername:
            continue
        try:
            os.chdir(foldername)
        except:
            continue
        
        # convert all images to more readable format: start
        if phase == 1:     
            for special in ["special1", "special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
                try: 
                    os.chdir(special)
                    filelist = glob.glob("*.avif", recursive = True)
                    for fn in filelist:
                        avif_img = Image.open(fn)
                        sp = fn.find(".")
                        nfn = '{}.png'.format(fn[0:sp])
                        avif_img.save(nfn)
                        os.remove(fn)
                    
                    filelist = glob.glob("*.jfif", recursive = True)
                    for fn in filelist:
                        jfif_img = Image.open(fn)
                        sp = fn.find(".")
                        nfn = '{}.png'.format(fn[0:sp])
                        jfif_img.save(nfn)
                        os.remove(fn)

                    if special == "special1":
                        filelist = glob.glob("*", recursive = True)
                        for fn in filelist:
                            if fn == "desktop.ini" or "txt" in fn or "rm" == fn or "mistake" == fn or "special1" == fn:
                                continue
                            fn2 = "../" + fn
                            shutil.copy(fn, fn2)                       
                      
                    os.chdir('../')
                except:
                    print("no ", special)

            filelist = glob.glob("*.avif", recursive = True)
            for fn in filelist:
                avif_img = Image.open(fn)
                sp = fn.find(".")
                nfn = '{}.png'.format(fn[0:sp])
                avif_img.save(nfn)
                os.remove(fn)
            
            filelist = glob.glob("*.jfif", recursive = True)
            for fn in filelist:
                # print(fn)
                jfif_img = Image.open(fn)
                sp = fn.find(".")
                nfn = '{}.png'.format(fn[0:sp])
                jfif_img.save(nfn)
                os.remove(fn)   
        # convert all images to more readable format: done

        # copy annotated data over for final results2: start  
        if phase == 2:
            # clear out the bad data
            for special in [".", "special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
                try:
                    os.chdir(special)
                    path = Path("mistake.txt")
                    if path.is_file():
                        os.makedirs(dpath +foldername + "/" + special +"/rm/", exist_ok=True)
                        total_file = 0
                        cur_garmentID = -1
                        n_file_move = 0
                        with open("mistake.txt") as file:
                            for item in file:
                                if "-" in item and item.find("_-") == -1:
                                    item = item.replace("-", "_")
                                space = item.find("_")
                                # move all to rm folder
                                if space<0:
                                    garmentID = int(item)  
                                    fl = glob.glob("{}_*".format(garmentID), recursive = True)
                                    for f in fl:
                                        shutil.move(f, "rm/" + f)  
                                else:
                                    if not "V" in item:
                                        garmentID = int(item[:space])
                                        if cur_garmentID == -1:
                                            cur_garmentID = garmentID
                                            fl = glob.glob("{}_*".format(garmentID), recursive = True)
                                            total_file = len(fl)
                                        elif cur_garmentID != garmentID:
                                            if total_file - n_file_move <= 2:
                                                fl = glob.glob("{}_*".format(cur_garmentID), recursive = True)
                                                if len(fl) == 2:
                                                    cnt_check = 0
                                                    for f in fl:
                                                        if "_-1" in f or "_0" in f:
                                                            cnt_check += 1
                                                    if cnt_check == 2:
                                                        for f in fl:
                                                            shutil.move(f, "rm/" + f) 
                                                elif len(fl) == 1:
                                                    if "_0" in fl[0] or "_-1" in fl[0]:
                                                        shutil.move(fl[0], "rm/" + fl[0]) 

                                            cur_garmentID = garmentID
                                            fl = glob.glob("{}_*".format(garmentID), recursive = True)
                                            total_file = len(fl)
                                            n_file_move = 1

                                        imgId = int(item[space+1:])
                                        fl = glob.glob("{}_{}*".format(garmentID, imgId), recursive = True)
                                        for f in fl:
                                            n_file_move += 1
                                            shutil.move(f, "rm/" + f)  
                                    # Move video
                                    else:
                                        fl = glob.glob("{}.*".format(item), recursive = True)
                                        for f in fl:
                                            shutil.move(f, "rm/" + f) 
                    
                        # Trường hợp đọc hết file
                        if total_file - n_file_move <= 2:
                            fl = glob.glob("{}_*".format(cur_garmentID), recursive = True)
                            if len(fl) == 2:
                                cnt_check = 0
                                for f in fl:
                                    if "_-1" in f or "_0" in f:
                                        cnt_check += 1
                                # TODO move garment to rm
                                if cnt_check == 2:
                                    for f in fl:
                                        shutil.move(f, "rm/" + f) 
                            elif len(fl) == 1:
                                if "_0" in fl[0] or "_-1" in fl[0]:
                                    shutil.move(fl[0], "rm/" + fl[0])
                    else:
                        nMistakesFiles = nMistakesFiles+1
                        
                    if special != ".":
                        os.chdir("../") 
                except Exception as e:
                    pass
                    # print("[handle mistake file]  err: ", e)
                    
            for special in [".", "special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
                try:
                    os.chdir(special)
                    
                    path = Path("special.txt")
                    if not os.path.exists("special1"):
                        os.mkdir("special1")
                    if path.is_file():
                        with open("special.txt") as file:
                            for item in file:
                                if "-" in item and item.find("_-") == -1:
                                    item = item.replace("-", "_")
                                space = item.find("_")
                                if space<0:
                                    garmentID = int(item)                 
                                    fl = glob.glob("{}_*".format(garmentID), recursive = True)
                                    for f in fl:
                                        shutil.move(f, "special1/" + f)
                                else:
                                    if not "V" in item:
                                        garmentID = int(item[:space])
                                        imgId = int(item[space+1:])  
                                        fl = glob.glob("{}_{}*".format(garmentID, imgId), recursive = True)
                                        for f in fl:
                                            shutil.move(f, "special1/" + f)  
                                    else:
                                        fl = glob.glob("{}.*".format(item), recursive = True)
                                        for f in fl:
                                            shutil.move(f, "special1/" + f)
                                            
                    if special != ".":
                        os.chdir("../") 
                except  Exception as e:
                    pass
                    # print("[handle special file]  err: ", e)

            for special in [".", "special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
                try:
                    os.chdir(special)
                    
                    list_images_0 = glob.glob("*_0.*")
                    for image in list_images_0:
                        garmentID = int(image.split("_")[0])
                        fl = glob.glob("{}_*".format(garmentID), recursive = True)
                        # Have garmentID_0 and garmentID_-1 and video
                        if len(fl) == 3:
                            cnt_check = 0
                            for f in fl:
                                if "_0" in f or "-1" in f or "_V" in f:
                                    cnt_check += 1
                            if cnt_check == 3:
                                for f in fl:
                                    # if "_V" in f:
                                    #     continue
                                    shutil.move(f, "special1/" + f)  
                        # Have garmentID_0 and garmentID_-1
                        if len(fl) == 2:
                            cnt_check = 0
                            for f in fl:
                                if "_0" in f or "-1" in f:
                                    cnt_check += 1
                            if cnt_check == 2:
                                for f in fl:
                                    shutil.move(f, "special1/" + f)  
                        # Have garmentID_0 or garmentID_-1
                        if len(fl) == 1:
                            shutil.move(fl[0], "special1/" + fl[0]) 
                    
                    list_images_minus_1 = glob.glob("*_-1.*")
                    for image in list_images_minus_1:
                        garmentID = int(image.split("_")[0])
                        fl = glob.glob("{}_*".format(garmentID), recursive = True)
                        # Have garmentID_0 and garmentID_-1 and video
                        if len(fl) == 3:
                            cnt_check = 0
                            for f in fl:
                                if "_0" in f or "-1" in f or "_V" in f:
                                    cnt_check += 1
                            if cnt_check == 3:
                                for f in fl:
                                    # if "_V" in f:
                                    #     continue
                                    shutil.move(f, "special1/" + f)  
                        # Have garmentID_0 and garmentID_-1
                        if len(fl) == 2:
                            cnt_check = 0
                            for f in fl:
                                if "_0" in f or "-1" in f:
                                    cnt_check += 1
                            if cnt_check == 2:
                                for f in fl:
                                    shutil.move(f, "special1/" + f)  
                        # Have garmentID_0 or garmentID_-1
                        if len(fl) == 1:
                            shutil.move(fl[0], "special1/" + fl[0]) 

                    if len(os.listdir("special1")) == 0:
                        os.rmdir("special1")
                                            
                    if special != ".":
                        os.chdir("../") 
                except  Exception as e:
                    pass
                    # print("[handle special file] err: ", e)
        # copy annotated data over for final results2: done

        if phase == 2:
            try:
                os.chdir("special1")
                cnt_models_special1 = 0
                filelist = glob.glob("*", recursive = True)
                for fn in filelist:
                    if fn == "desktop.ini" or "txt" in fn or "rm" == fn or "mistake" == fn or "special1" == fn or "_-1" in fn or "_0" in fn:
                        continue
                    cnt_models_special1 += 1
                total_cnt_models_special1 += cnt_models_special1
                models_special1.append({
                    "name": foldername,
                    "cnt": cnt_models_special1,
                })
                os.chdir(os.path.join(dpath,foldername))
            except:
                models_special1.append({
                    "name": foldername,
                    "cnt": 0,
                })
        
        # make results: start
        for folder in [".", "special2", "special3", "special4", "special5", "special6", "special7", "special8"]:
            # if folder != "special7":
            #     continue
            print("Make results for {}".format(os.path.join(foldername, folder))) 
            link_and_save_image(folder, format_file)
            os.chdir(os.path.join(dpath,foldername))
        # make results: done

        print('Done\n')
        with open(dpath+"/"+"format.txt", "w") as output:
            for format in format_file:
                output.write(format+"\n")
        os.chdir('../')
    if phase == 2:
        with open(dpath+"/"+"models_special1_" + str(total_cnt_models_special1) + ".txt", "w") as f:
            for obj in models_special1:
                f.write(f"{obj['name']} {obj['cnt']}\n")
        
    # if phase == 1:
    #     os.chdir(dpath)
    #     os.chdir("../")
    #     with open(dpath.split("\\")[-1].replace("/","")+f"_count_images_{TOTAL_CNT_IMAGES}.txt", "w") as output:
    #         pass
    print('#folders wo mistake files: {}/{}'.format(len(folderList) - nMistakesFiles, len(folderList)))
    if phase == 1:
        if len(WARN_LOST_FILES) > 0:
            print(WARN_LOST_FILES)