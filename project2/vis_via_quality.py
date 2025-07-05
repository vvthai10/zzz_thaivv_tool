#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 00:23:59 2023

@author: minhvo
"""
import os
import json 
import cv2
import glob
import numpy as np
from fuzzywuzzy import fuzz
import argparse
from tqdm import tqdm
import shutil 

c1 = (0, 0, 0)
c2 = (255, 0, 0)
c3 = (0, 255, 0)
c4 = (255, 255, 0)
c5 = (0, 0, 255)
c6 = (255, 0, 255)
c7 = (0, 255, 255)
c8 = (255, 255, 255)
c9 = (87, 200, 45)
c10 = (0, 128, 233)
c11 = (0, 231, 193)
c12 = (212, 190, 21)
c13 = (121, 254, 11)
c14 = (3, 129, 213)
c15 = (31, 79, 0)
c16 = (170, 242, 120)
c17 = (17, 242, 190)
c18 = (57, 212, 110)
c19 = (157, 12, 231)
c20 = (255, 22, 31)
c21 = (17, 122, 251)
c22 = (111, 189, 153)
c23 = (0, 212, 123)
c24 = (213, 89, 0)
c25 = (183, 139, 10)
c26 = (213, 45, 88)
c27 = (75, 139, 150)
c28 = (213, 150, 150)
c29 = (152, 10, 52)
c30 = (52, 150, 150)
c31 = (219, 26, 184)
c32 = (10, 150, 184)
c33 = (219, 120, 184)
c34 = (119, 220, 85)

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
org2 = (400, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2
project3 = False

useErrorFiles = False
def join_via_files(dpath):
    os.chdir(dpath+'/result/')
    fileNames = glob.glob("*.json", recursive = True)
    fileNames = sorted(fileNames)

    errorFiles = []
    if useErrorFiles:   
        with open('./../error.txt') as f:
            lines = f.readlines()
            for l in lines:
                if len(l)>3:
                    errorFiles.append(l.strip())


    alldata = []
    for filename in fileNames:
        if filename == 'all.json':
            continue
        
        print(filename)
        f = open(filename, errors="ignore", encoding="utf-8")
        data = json.load(f)  
        # with open(filename, "r", encoding="utf-8") as f:
        #     data = json.load(f)
        for i in data['_via_img_metadata']:
            content = data['_via_img_metadata'][i]
            filename = content['filename']
            segs = content['regions']
            if project3:
                cap = content['caption']
            
            for i in errorFiles:
                dot = filename.find(".")
                if filename[:dot] == i:
                    for seg in segs:
                        label = seg['region_attributes']['name']
                        if fuzz.partial_ratio('front right sleeve', label) > 95: 
                            seg['region_attributes']['name'] = "front left sleeve"
                        elif fuzz.partial_ratio('front left sleeve', label) > 95: 
                            seg['region_attributes']['name'] = "front right sleeve"
                    break

            
            if project3:
                img_cont = [filename, segs, cap]
            else:
                img_cont = [filename, segs]

            alldata.append(img_cont)
        f.close()

    # #clean overlapping files one with data and other with none
    # toKeepId = []
    # toDeleteId = []
    # for i in range(len(alldata)):
    #     duplication = False
    #     for j in range(len(alldata)):
    #         if i > j  and alldata[i][0] == alldata[j][0]:
    #             if len(alldata[i][1])> len(alldata[j][1]):
    #                 alldata[j][1] = alldata[i][1]
    #             else:
    #                 alldata[i][1] = alldata[j][1]


    if os.path.isdir(dpath+"/addition"):  
        os.chdir(dpath+"/addition")
        fileNames = glob.glob("*.json", recursive = True)
        fileNames = sorted(fileNames)
        if len(fileNames) > 0:
            print("Getting Addition")

        for filename in fileNames:
            f = open(filename)
            data = json.load(f)  
            for i in data['_via_img_metadata']:
                content = data['_via_img_metadata'][i]
                filename = content['filename']
                segs = content['regions']


                for data_i in alldata:
                    dot1 = data_i[0].find(".")
                    ename1 = data_i[0][:dot1]
                    dot2 = filename.find(".")
                    ename2 = filename[:dot2]
                    if ename1 == ename2:
                        for seg_i in segs:
                            data_i[1].append(seg_i)
            f.close()

    for r in range(1, 10):
        additionName = dpath+"/addition {}".format(r)
        if os.path.isdir(additionName):  
            os.chdir(additionName)
            fileNames = glob.glob("*.json", recursive = True)
            fileNames = sorted(fileNames)
            if len(fileNames) > 0:
                print("Getting Addition {}".format(r))

            for filename in fileNames:
                f = open(filename)
                data = json.load(f)  
                for i in data['_via_img_metadata']:
                    content = data['_via_img_metadata'][i]
                    filename = content['filename']
                    segs = content['regions']


                    for data_i in alldata:
                        dot1 = data_i[0].find(".")
                        ename1 = data_i[0][:dot1]
                        dot2 = filename.find(".")
                        ename2 = filename[:dot2]
                        if ename1 == ename2:
                            for seg_i in segs:
                                data_i[1].append(seg_i)
                f.close()


    if os.path.isdir(dpath+"/correction"):  
        os.chdir(dpath+"/correction")
        correctionFileNames = glob.glob("*.json", recursive = True)
        correctionFileNames = sorted(correctionFileNames)
        if len(correctionFileNames) > 0:
            print("getting Correction")

        for cfilename in correctionFileNames:
            f = open(cfilename)
            data = json.load(f)  
            for i in data['_via_img_metadata']:
                content = data['_via_img_metadata'][i]
                filename = content['filename']
                segs = content['regions']

                found = False
                for data_i in alldata:
                    dot1 = data_i[0].find(".")
                    ename1 = data_i[0][:dot1]
                    dot2 = filename.find(".")
                    ename2 = filename[:dot2]
                    if ename1 == ename2:
                        data_i[1] = segs
                        found = True
                if not found:
                    img_cont = [filename, segs]
                    alldata.append(img_cont)
            f.close()

    for r in range(1, 10):
        correctionName = dpath+"/correction {}".format(r)
        if os.path.isdir(correctionName):  
            os.chdir(correctionName)
            correctionFileNames = glob.glob("*.json", recursive = True)
            correctionFileNames = sorted(correctionFileNames)
            if len(correctionFileNames) > 0:
                print("getting Correction {}".format(r))

            for cfilename in correctionFileNames:
                f = open(cfilename, errors="ignore", encoding="utf-8")
                data = json.load(f)  
                for i in data['_via_img_metadata']:
                    content = data['_via_img_metadata'][i]
                    filename = content['filename']
                    segs = content['regions']

                    found = False
                    for data_i in alldata:
                        dot1 = data_i[0].find(".")
                        ename1 = data_i[0][:dot1]
                        dot2 = filename.find(".")
                        ename2 = filename[:dot2]
                        
                        if ename1 == ename2:
                            if ename2 == '173_0':
                                a = 0
                            data_i[1] = segs
                            found = True

                    if not found:
                        img_cont = [filename, segs]
                        alldata.append(img_cont)
                f.close()


    for data_i in alldata:
        for seg in data_i[1]:
            if seg == None:
                continue
            label = seg['region_attributes']['name']
            seg['region_attributes']['name'] = label.replace("_", " ")
    
    os.chdir(dpath+'/result/')
    with open('all.json', 'w') as f:
        json.dump(alldata, f, indent=4)

def overlay(
    image: np.ndarray,
    mask: np.ndarray,
    alpha: float = 0.5,
) -> np.ndarray:
    colored_mask = np.zeros((mask.shape[0],mask.shape[1],3), np.uint8)
    colored_mask[:,:,0] = mask
    image_combined = cv2.addWeighted(image, 1 - alpha, colored_mask, alpha, 0)
    
    return image_combined

def overlayColor(
    image: np.ndarray,
    colored_mask: np.ndarray,
    alpha: float = 0.5,
) -> np.ndarray:
    image_combined = cv2.addWeighted(image, 1 - alpha, colored_mask, alpha, 0)
    
    return image_combined

def get_id_from_images_name(name):
    gar_index = name.find("_gar")
    if gar_index != -1:
        last_underscore_before_gar = name.rfind("_", 0, gar_index)
        
        if last_underscore_before_gar != -1:
            res = name[last_underscore_before_gar + 1:gar_index]
            return int(res)
    else:
        print("[ERROR 274]", folder)
        exit()

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

folderNames = []
with open('/content/completed.txt') as f:
    lines = f.readlines()
    for l in lines:
        if len(l)>=3:
            folderNames.append(l.strip())
for folder in folderNames:
    dpath = args.dpath+"/"+folder
    print(dpath)
    if not os.path.isdir(dpath):
        print("not finding {}".format(folder))
        exit()
    print('Working on {}'.format(folder))
    
    join_via_files(dpath)
    f = open(dpath+'/result/all.json')
    data = json.load(f)  
    if os.path.exists(dpath+'/Result/all2.json'):
        print("read all2.json")
        f = open(dpath+'/Result/all2.json')
        data = json.load(f)
        
    if os.path.isdir(dpath+"/results1"):
        shutil.rmtree(dpath +"/results1/")
    os.makedirs(dpath +"/results1")
            
    os.chdir(dpath)
    imgNames = glob.glob("*", recursive = True)
    imgNames = sorted(imgNames)
    imgNames2 = []
    for n in imgNames:
        if not os.path.isdir(n):
            imgNames2.append(n)                
            
    missed_labels = []
    total_segments = []
    for data_i in data:
        img_name = data_i[0]
        if img_name == "LOEWE_MEN_TROUSERS_SHORTS_001_gar_0":
            print(data_i)
        if os.path.isfile(dpath +'/'+img_name):
            img = cv2.imread(dpath +'/'+img_name)
        else:
            dot = img_name.find(".")
            ename = img_name[:dot]
            found = False
            for imgName2 in imgNames2:
                dot = imgName2.find(".")
                ename2 = imgName2[:dot]
                if ename == ename2:
                    img = cv2.imread(dpath +'/'+imgName2)
                    if img is None:
                        print("No {}".format(img_name))
                        continue
                    found = True
                    break
            if not found:
                continue
        print(img_name)
        seg_img = np.zeros((img.shape[0], img.shape[1],3), np.uint8)
        third_img = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8) * 255
        
        all_centers = []
        all_contours = []
        found_missing_labels = False
        count_segment = 0
        for seg in data_i[1]:
            if seg == None:
                continue
            label = seg['region_attributes']['name']
            try:
                x = seg['shape_attributes']['all_points_x']
            except:
                continue
            x = seg['shape_attributes']['all_points_x']
            y = seg['shape_attributes']['all_points_y']
            
            count_segment += 1
            if fuzz.partial_ratio('background', label) > 95: #cho dress
                if label != "background":
                    print(f"{label} with {fuzz.partial_ratio('background', label)}")
                color = c14
            elif fuzz.partial_ratio('hat', label) > 95: #cho dress
                color = c15
            elif fuzz.partial_ratio('hair', label) > 95:
                color = c1
            elif fuzz.partial_ratio('watch', label) > 95:
                color = c2
            elif fuzz.partial_ratio('glasses', label) > 95\
                or fuzz.partial_ratio('mask', label) > 95:
                color = c3
            elif fuzz.partial_ratio('left hand skin', label) > 95:
                color = c4
            elif fuzz.partial_ratio('right hand skin', label) > 95:
                color = c8
            elif fuzz.partial_ratio('left leg skin', label) > 95:
                color = c10
            elif fuzz.partial_ratio('right leg skin', label) > 95:
                color = c18
            elif fuzz.partial_ratio('body skin', label) > 95:
                color = c19
            elif fuzz.partial_ratio('face skin', label) > 95:
                color = c5
            elif fuzz.partial_ratio('scarf', label) > 95:
                color = c5
            elif fuzz.partial_ratio('person bag', label) > 95:
                color = c6
            elif fuzz.partial_ratio('top', label) > 95:
                color = c7
            elif fuzz.partial_ratio('dress', label) > 95:
                color = c11
            elif fuzz.partial_ratio('skirt', label) > 95:
                color = c12
            elif fuzz.partial_ratio('ring', label) > 95:
                color = c13
            elif fuzz.partial_ratio('left pants', label) > 95 :
                color = c14
            elif fuzz.partial_ratio('right pants', label) > 95:
                color = c15
            elif fuzz.partial_ratio('left sleeves', label) > 95:
                color = c16
            elif fuzz.partial_ratio('right sleeves', label) > 95:
                color = c17
            elif fuzz.partial_ratio('left shoes', label) > 95 or fuzz.partial_ratio('boots', label) > 95:
                if label != "left shoes":
                    print(f"{label} with {fuzz.partial_ratio('left shoes', label)}")
                color = c18
            elif fuzz.partial_ratio('right shoes', label) > 95 or\
                fuzz.partial_ratio('boots', label) > 95:
                if label != "right shoes":
                    print(f"{label} with {fuzz.partial_ratio('right shoes', label)}")
                color = c19
            elif fuzz.partial_ratio('left tights', label) > 95:
                color = c20
            elif fuzz.partial_ratio('right tights', label) > 95:
                color = c21
            elif fuzz.partial_ratio('left socks', label) > 95:
                color = c22
            elif fuzz.partial_ratio('right socks', label) > 95:
                color = c23
            elif fuzz.partial_ratio('band', label) > 95:
                color = c24
            elif fuzz.partial_ratio('gloves', label) > 95:
                color = c25
            elif fuzz.partial_ratio('jumpsuit', label) > 95:
                color = c26
            elif fuzz.partial_ratio('inner top', label) > 95:
                color = c27
            elif fuzz.partial_ratio('inner bottom', label) > 95:
                color = c32
            elif fuzz.partial_ratio('inner dress', label) > 95:
                color = c33
            elif fuzz.partial_ratio('inner sleeve', label) > 95:
                color = c34
            elif fuzz.partial_ratio('panty', label) > 95:
                color = c28
            elif fuzz.partial_ratio('hair accessory', label) > 95:
                color = c29
            elif fuzz.partial_ratio('1-piece swimwear', label) > 95:
                color = c30
            elif fuzz.partial_ratio('whole body long', label) > 95:
                color = c31
            else:
                count_segment -= 1
                print(img_name)
                print(label)
                color = c9
                found_missing_labels = True
                missed_labels.append(img_name)

            color2 = ( int (color [ 0 ]), int (color [ 1 ]), int (color [ 2 ])) 
            arr = np.array([x,y])
            # print("CHECK HERE")
            # print(arr)
            center = arr.mean(1)
            all_centers.append([label, center])
            cv2.fillPoly(seg_img, pts = [np.transpose(arr)], color=color2)
            cv2.fillPoly(third_img, pts = [np.transpose(arr)], color=color2)
        
            contour = np.transpose(arr)
            contour = np.expand_dims(contour, axis=1)
            all_contours.append(contour)
        overlayImg = overlayColor(img, seg_img)
        
        total_segments.append(
            {
            "image": img_name[:-4],
            "total": count_segment 
            }
        )
        # if total_segments[0]["image"][0].isdigit():
        #     total_segments.sort(key=lambda x: int(x["image"].split("_")[0]), reverse=False)
        # else:
        #     total_segments.sort(key=lambda x: get_id_from_images_name(x["image"]), reverse=False)

        # print(total_segments)
        
        f = 'total label: {}'.format(len(data_i[1]))
        if len(data_i[1]) == 0:
            missed_labels.append(img_name)
            print(img_name)
            found_missing_labels = True

        fontsize = max(0.5,overlayImg.shape[0]/1024*0.5)
        overlayImg = cv2.putText(overlayImg, f, org, font, fontsize, (255, 0, 0), 1, cv2.LINE_AA)  
        third_img = cv2.putText(third_img, f, org, font, fontsize, (255, 0, 0), 1, cv2.LINE_AA)  
        
        for name_center in all_centers:
            name = name_center[0].strip()
            center = name_center[1]
            fontsize = max(0.5,overlayImg.shape[0]/1024*0.5)
            cv2.circle(overlayImg, (int(center[0]), int(center[1])), 2,  (0, 0, 255), thickness=2)
            cv2.circle(third_img, (int(center[0]), int(center[1])), 2,  (0, 0, 255), thickness=2)
            overlayImg = cv2.putText(overlayImg, name, (int(center[0]), int(center[1])), font,fontsize, (0, 255, 0), 1, cv2.LINE_AA) 
            third_img = cv2.putText(third_img, name, (int(center[0]), int(center[1])), font,fontsize, (0, 255, 0), 1, cv2.LINE_AA) 
        
        for contour in all_contours:
            col = list(np.random.choice(range(256), size=3))
            cv2.drawContours(overlayImg, contour, -1, ( int (col[ 0 ]), int (col [ 1 ]), int (col [ 2 ])), 4, cv2.FILLED)
            cv2.drawContours(third_img, contour, -1, ( int (col[ 0 ]), int (col [ 1 ]), int (col [ 2 ])), 4, cv2.FILLED)
            
        dot = img_name.find(".")
        # if found_missing_labels:
        #     os.makedirs(dpath +"/results1/missing", exist_ok=True)
        #     fn = dpath +"/results1/missing/" + img_name[:dot]+".jpg"
        # else:
        fn = dpath +"/results1/" + img_name[:dot]+".jpg"
        im_v = cv2.hconcat([img, overlayImg, third_img])
        cv2.imwrite(fn,im_v)
    

    # with open("sample.json", "w", encoding="utf-8") as file:
    #     file.write(json.dumps(total_segments))
    txt_file = open("test.txt", "w", encoding="utf-8")
    for line in total_segments:
        txt_file.write(line["image"] + " " + str(line["total"]) + "\n")
    txt_file.write("total " + str(len(total_segments)))
    txt_file.close()

    if len(missed_labels)>0:
        print("{} has {} missing".format(folder, len(missed_labels)))
        fn = dpath +'/results1/missing_labels.txt'
        with open(fn, 'w') as fp:
            for item in missed_labels:
                fp.write("%s\n" % item)
    print('Done\n')