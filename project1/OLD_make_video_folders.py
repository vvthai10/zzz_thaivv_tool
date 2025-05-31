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


# list_file_name = [
# "billyreid_men_jackets_outerwear",
# "mugler_women_knitwear",
# "nililotan_men_sweaters",
# "billyreid_men_polos_tees_henleys",
# "mugler_women_tops",
# "nililotan_men_tees",
# "billyreid_men_shirting",
# "mybeachyside_women_tops",
# "nililotan_men_tops",
# "billyreid_men_sweaters_knits",
# "nanushka_men_knitwear",
# "nililotan_women_jackets",
# "billyreid_women_jackets_outerwear",
# "nanushka_men_outerwear",
# "nililotan_women_outerwear",
# "billyreid_women_sweaters_knits",
# "nanushka_men_shirts",
# "nililotan_women_sweaters",
# "billyreid_women_tops",
# "nanushka_men_tshirts_vests",
# "nililotan_women_sweats",
# "nanushka_women_jackets_blazers",
# "nililotan_women_sweats",
# "minnierose_women_cardigans",
# "nanushka_women_knitwear",
# "nililotan_women_tees",
# "minnierose_women_crewneck",
# "nanushka_women_knitwear",
# "nililotan_women_tops",
# "minnierose_women_jackets",
# "nanushka_women_outerwear",
# "ninaricci_women_coats_jackets",
# "minnierose_women_sweater",
# "nanushka_women_shirts",
# "ninaricci_women_knitwear",
# "minnierose_women_tops",
# "nanushka_women_sweatshirts",
# "ninaricci_women_shirts",
# "minnierose_women_tshirts",
# "nanushka_women_tops",
# "ninaricci_women_tops",
# "minnierose_women_vests",
# "nicholasdaley_men_outerwear",
# "nn07_men_jackets",
# "minnierose_women_vneck",
# "nicholasdaley_men_tops",
# "mugler_women_coat_jacket",
# "nililotan_men_jackets_outerwear",
# ]

def link_and_save_image(path_name: str):
    exist_folder = False
    try:
        os.chdir(path_name)
        exist_folder = True
            
        filelist = glob.glob("*", recursive = True)
        filelist = sorted(filelist)
        nfiles = len(filelist)

        ta = []
        sub_ta = []
        o_gid = -1
        maxSubImage = 0
        print('Tabling files...')
        for i in tqdm(range(nfiles)):
            f = filelist[i]
            if f == 'special and mistake.gsheet' or f == "desktop.ini" or f == "special"or f == "SPECIAL_6" or f == "SPECIAL_2" or f == "special_1" or f == "SPECIAL_1" or f == "SPECIAL 1" or f == "special 1" or f == 'special2' or f == "low_res" or f == "Special" or f == "SPECIAL" or  f == "Doubt" or  f == "videos" or f == "mistake" or f == "rm" or f == "mistake.txt" or f == "special.txt":
                continue
            if os.path.isdir(f):
                continue

            dot = f.find(".")
            if f[dot:] == ".webm" or f[dot:] == ".mp4" or f[dot:] == ".mov" or f[dot:] == ".ts" or f[dot:] == ".txt":
                continue
            if f.find(").") > -1:
                fn = dpath+"/"+foldername+"/" + f if path_name == "." else dpath+"/"+foldername+"/" + path_name + "/" + f
                # fn = dpath+"/"+foldername+"/" + f
                print("[REMOVE FILE 49] ",fn)
                os.remove(fn)
                continue
        
            sp = f.find("_")
            try:
                garmentId = int(f[:sp]) 
            except:
                print("[WARN HERE 57] ", f)
                exit()
            try:
                imageId = int(f[sp+1:f.find(".")])
            except:
                print("[WARN HERE 62] ", f)
                exit()  
            img = cv2.imread(f)
            if img is None:
                print("[WARN HERE 66] ", f)
                exit()
            if img.shape[0] + img.shape[1] < 400 and imageId > 0:
                print("[COPY HERE 69] ", f)
                if not os.path.exists("low_res"):
                    os.mkdir("low_res")
                shutil.move(f, "low_res/"+f)  
                continue
            
            if garmentId != o_gid:
                if len(sub_ta)==0:
                    sub_ta = [f]
                else:
                    ta.append([o_gid, sub_ta])  
                    maxSubImage = max(maxSubImage, len(sub_ta))
                    sub_ta = [f]     

                o_gid = garmentId
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

        cnt = 0
        for ita in tqdm(ta):
            if len(ita[1])<2:
                f = ita[1][0]
                sp = f.find("_")
                garmentId = int(f[:sp]) 
                list_check = glob.glob(f"{garmentId}_*")
                if len(list_check) == 1:
                    continue
            cnt = cnt+1
        
        size = (img_w*(maxSubImage+2), img_h)

        if phase == 1:
            if path_name in ["special2", "special3", "special4"]:
                folderPath = dpath +f"/results1_{path_name}/"+foldername+"_{}".format(cnt)
            else:
                folderPath = dpath +"/results1/"+foldername+"_{}".format(cnt)
        elif phase == 2:
            folderPath = dpath +"/results2/"+foldername+"_{}".format(cnt)
        os.makedirs(folderPath, exist_ok=True)

        print('Making result!')
        for ita in tqdm(ta):
            # print(ita)
            try:
                bimg = np.zeros((img_h,img_w*(maxSubImage+4),3), dtype=np.uint8)

                f = ita[1][0]
                sp = f.find("_")
                garmentId = int(f[:sp]) 
                
                if len(ita[1])<2:
                    list_check = glob.glob(f"{garmentId}_*")
                    if len(list_check) < 2:
                        continue
                    # print(list_check)
                    # print(os.getcwd())
                    # print(folderPath)
                    for file in list_check:
                        shutil.copy(file, folderPath)
                    continue

                # Check image just clothes 
                if len(ita[1]) <= 2:
                    list_check = glob.glob(f"{garmentId}_*")
                    cnt = 0
                    for img in list_check:
                        if f"{garmentId}_0" in img or f"{garmentId}_-1" in img:
                            cnt += 1
                    
                    if cnt >= 2:
                        # print(list_check)
                        # print(os.getcwd())
                        # print(folderPath)
                        for file in list_check:
                            shutil.copy(file, folderPath)
                        continue

                    
                imageId = int(f[sp+1:f.find(".")])  
                
                for i in range(0, len(ita[1])):
                    if path_name not in ["special2", "special3", "special4"]:
                        fn = dpath+"/"+foldername+"/"+ita[1][i]
                    else:
                        fn = dpath+"/"+foldername+"/"+path_name+"/"+ita[1][i]
                    f1 = ita[1][i]
                    sp = f1.find("_")
                    imageId = int(f1[sp+1:f1.find(".")])
                    img = cv2.imread(fn) 
                    h,w, c = img.shape

                    rgba_img = cv2.imread(fn, cv2.IMREAD_UNCHANGED) 
                    if len(rgba_img.shape) == 3 and rgba_img.shape[2] == 4:
                        rgb_img = cv2.cvtColor(rgba_img, cv2.COLOR_RGBA2RGB)
                        alpha_channel = rgba_img[:, :, 3]
                        mask = (alpha_channel == 0)
                        rgb_img[mask] = [255, 255, 255]
                        img = rgb_img
                    
                    rimg = cv2.resize(img, [img_w, img_h])
                    f = '{}:{}x{}'.format(imageId,w,h)
                    rimg = cv2.putText(rimg, f, org, font,fontScale, color, thickness, cv2.LINE_AA)    
                    bimg[0:img_h, img_w*(imageId+1):img_w*(imageId+2)] = rimg   

                f = '{}'.format(garmentId)
                bimg = cv2.putText(bimg, f, org2, font,fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
                f = folderPath+"/{}.jpg".format(garmentId)
                if not no_images_output:
                    cv2.imwrite(f, bimg)
            except:
                print("[WARNING 157] ", ita)
    except:
        if not exist_folder:
            pass
        else:
            exit()

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

# 0: copy results1
# 1: run results1
# 2: run results2
# 3: copy results2
# 4: run results3
phase = 1
print("[TYPE RUN] ", phase)
no_images_output = True
if phase == 1:
    no_images_output = False
     
# copy text file from results1 to each folder
if phase == 0:
    dpath = args.dpath
    os.chdir(dpath)
    os.chdir(dpath+'/results1')
    folderList = glob.glob("*", recursive = True)
    folderList = sorted(folderList)
    noresults = 0
    for foldername in tqdm(folderList):
        if "desktop" in foldername or foldername == 'Special &Mistake.gsheet' or foldername == 'Special and Mistake.xlsx' or foldername == 'special & mistake.gsheet' or foldername == 'special and mistake.xlsx' or foldername == 'Special& mistake.gsheet' or foldername == 'Special& Mistake.gsheet' or foldername == 'Special&mistake (1).gsheet' or foldername == 'Special&Mistake.gsheet' or foldername == 'special and mistake .gsheet' or foldername == 'Special&mistake.gsheet' or foldername == "Special & Mistake.gsheet" or foldername == "special and mistake.gsheet" or foldername == "Clothing_collection.gsheet" or foldername == "Special& Mistakes.gsheet" or foldername == "Special and mistake.gsheet" or foldername == "Clothing collection.gsheet" or foldername == "special_and_mistake.xlsx" or foldername == "mistake&special.gsheet" or foldername == 'Clothing collection.xlsx' or foldername == 'SPECIAL AND MISTAKE.xlsx' or foldername == 'Clothing Collection.gsheet' or foldername == 'Special and mistake.gsheet' or foldername == 'Special and mistake.xlsx' or foldername == 'Special and Mistake.gsheet' or foldername == 'Mistake and Special .gsheet':
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
            noresults = noresults + 1
        os.chdir(dpath+'/results1')
    print("no resulst: {}/{}".format(noresults, len(folderList)))
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
    os.chdir(dpath)
    if phase == 1:
        os.makedirs(dpath +"/results1", exist_ok=True)
        os.makedirs(dpath +"/results1_special2/", exist_ok=True)
        os.makedirs(dpath +"/results1_special3/", exist_ok=True)
        os.makedirs(dpath +"/results1_special4/", exist_ok=True)
    elif phase == 2:
        if os.path.isdir(dpath+"/results2"):
            shutil.rmtree(dpath +"/results2/")

    nMistakesFiles = 0
    folderList = glob.glob("*", recursive = True)
    folderList = sorted(folderList)
    for foldername in folderList:
        print(foldername)
        # if foldername in list_file_name:
        #     continue
        if foldername == 'mistake' or foldername == 'results1_special2' or foldername == 'results1_special3'  or foldername == 'results1_special4' or foldername == 'results2' or foldername == 'results1' or foldername == 'results3' or foldername == 'results4' or foldername == 'videos':
            continue
        try:
            os.chdir(foldername)
        except:
            continue

        # check for all obvious naming format: start
        if True:
            filelist = glob.glob("*-*", recursive = True)
            for fn in filelist:
                if fn.find("_-") > -1:
                    continue
                nfn = fn.replace("-", "_")
                shutil.move(fn, nfn)

            filelist = glob.glob("*", recursive = True)
            filelist = sorted(filelist)
            nfiles = len(filelist)
            for i in tqdm(range(nfiles)):
                f = filelist[i]
                if f == "special_1" or f == "Special 1" or f == "SPECIAL_1" or f == "SPECIAL 1" or f == "special":
                    os.rename(f, "special 1")
                if f == "special 2" or f == "Special 2":
                    os.rename(f, "special2")
                if f == "special 3" or f == "Special 3":
                    os.rename(f, "special3")
                if f == "special 4" or f == "Special 4":
                    os.rename(f, "special4")
        # check for all obvious naming format: done

        # convert all images to more readable format: start
        if phase == 1:  
            for folder in [".", "special 1","special2", "special3", "special4"]:     
                try: 
                    os.chdir(folder)
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

                    # if folder == "special 1":
                    #     filelist = glob.glob("*", recursive = True)
                    #     for fn in filelist:
                    #         fn2 = "../" + fn
                    #         shutil.copy(fn, fn2)  
                    if folder != ".":
                        os.chdir('../')
                except:
                    print("no {}".format(folder)) 
        # convert all images to more readable format: done

        # copy annotated data over for final results2: start  
        if phase == 2:
            # clear out the bad data
            path = Path("mistake.txt")
            if path.is_file():
                os.makedirs(dpath +foldername+"/rm/", exist_ok=True)
                with open("mistake.txt") as file:
                    for item in file:
                        if len(item)<2:
                            continue
                        space = item.find("_")
                        if space<0:
                            garmentID = int(item)               
                            fl = glob.glob("{}_*".format(garmentID), recursive = True)
                            for f in fl:
                                shutil.move(f, "rm/"+f)  
                        else:
                            if not "V" in item:
                                garmentID = int(item[:space])
                                imgId = int(item[space+1:])-1
                                fl = glob.glob("{}_{}*".format(garmentID, imgId), recursive = True)
                                for f in fl:
                                    shutil.move(f, "rm/"+f)  
                            else:
                                fl = glob.glob("{}.*".format(item), recursive = True)
                                for f in fl:
                                    shutil.move(f, "rm/"+f) 
            else:
                nMistakesFiles = nMistakesFiles+1
                            
            path = Path("special.txt")
            if path.is_file():
                with open("special.txt") as file:
                    for item in file:
                        if len(item)<2:
                            continue
                        space = item.find("_")
                        if space<0:
                            garmentID = int(item)                 
                            fl = glob.glob("{}_*".format(garmentID), recursive = True)
                            for f in fl:
                                dot = f.find(".")
                                ename = f[dot+1:]
                                if ename == "webm":
                                    continue
                                img = cv2.imread(f)
                                if img.shape[0] + img.shape[1]<600:
                                    shutil.move(f, "low_res/"+f)  
                        else:
                            if not "V" in item:
                                garmentID = int(item[:space])
                                imgId = int(item[space+1:])-1   
                                fl = glob.glob("{}_{}*".format(garmentID, imgId), recursive = True)
                                # print(fl)
                                for f in fl:
                                    img = cv2.imread(f)
                                    if img.shape[0] + img.shape[1]<600:
                                        shutil.move(f, "low_res/"+f)  
                            else:
                                fl = glob.glob("{}.*".format(item[:-1]), recursive = True)
                                for f in fl:
                                    cap = cv2.VideoCapture(f)
                                    while True:
                                        ret, frame = cap.read()
                                        if not ret:
                                            break
                                        if frame.shape[0] + frame.shape[1] < 600:
                                            shutil.move(f, "low_res/" + f)
                                            break
                                    cap.release()


            path = Path("special2.txt")
            if path.is_file():
                os.makedirs(dpath +foldername+"_special2/", exist_ok=True)
                with open("special2.txt") as file:
                    for item in file:
                        if len(item)<2:
                            continue
                        space = item.find("_")
                        if space<0:
                            garmentID = int(item)                 
                            fl = glob.glob("{}_*".format(garmentID), recursive = True)
                            for f in fl:
                                shutil.move(f, "../"+foldername+"_special2/"+f)  
        # copy annotated data over for final results2: done

        # make results: start
        for folder in [".", "special2", "special3", "special4"]:
            print("Make results for {}".format(os.path.join(foldername, folder))) 
            link_and_save_image(folder)
            os.chdir(os.path.join(dpath,foldername))
        # make results: done

        print('Done\n')
        os.chdir('../')

    print('#folders wo mistake files: {}/{}'.format(len(folderList) - nMistakesFiles, len(folderList)))