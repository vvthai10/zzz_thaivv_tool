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
c9 = (128, 31, 89)
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

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
org2 = (400, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2
project3 = False

def sort_by_time_created(listFile):
    fileInfoList = [(file_path, os.path.getmtime(file_path)) for file_path in listFile]
    sortedFileInfo = sorted(fileInfoList, key=lambda x: x[1])
    fileNames = [file_path for file_path, _ in sortedFileInfo]

    return fileNames


useErrorFiles = False
def join_via_files(dpath):
    os.chdir(dpath+'/Result/')
    fileNames = glob.glob("*.json", recursive = True)

    # TODO: Sort all file by time created
    fileNames = sort_by_time_created(fileNames)

    errorFiles = []
    if useErrorFiles:   
        with open('./../error.txt') as f:
            lines = f.readlines()
            for l in lines:
                if len(l)>3:
                    errorFiles.append(l.strip())


    alldata = []
    added = []
    for filename in fileNames:
        if filename == 'all.json':
            continue

        f = open(filename)
        data = json.load(f)  
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

            if filename not in added:
                added.append(filename)
                alldata.append(img_cont)
            else:
                idx = added.index(filename)
                # print(f"Exist file {filename} with idx={idx} => file {alldata[idx][0]}")
                alldata[idx][1] = segs
                if project3:
                    alldata[idx][2] = cap
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


    if os.path.isdir(dpath+"/Addition"):  
        os.chdir(dpath+"/Addition")
        fileNames = glob.glob("*.json", recursive = True)
        # fileNames = sorted(fileNames)
        # TODO: Sort all file by time created
        fileNames = sort_by_time_created(fileNames)

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
        additionName = dpath+"/Addition {}".format(r)
        if os.path.isdir(additionName):  
            os.chdir(additionName)
            fileNames = glob.glob("*.json", recursive = True)
            # fileNames = sorted(fileNames)
            # TODO: Sort all file by time created
            fileNames = sort_by_time_created(fileNames)

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


    if os.path.isdir(dpath+"/Correction"):  
        os.chdir(dpath+"/Correction")
        correctionFileNames = glob.glob("*.json", recursive = True)
        # correctionFileNames = sorted(correctionFileNames)
        # TODO: Sort all file by time created
        correctionFileNames = sort_by_time_created(correctionFileNames)
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
        correctionName = dpath+"/Correction {}".format(r)
        if os.path.isdir(correctionName):  
            os.chdir(correctionName)
            correctionFileNames = glob.glob("*.json", recursive = True)
            # correctionFileNames = sorted(correctionFileNames)
            # TODO: Sort all file by time created
            correctionFileNames = sort_by_time_created(correctionFileNames)

            if len(correctionFileNames) > 0:
                print("getting Correction {}".format(r))

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

    for data_i in alldata:
        for seg in data_i[1]:
            if seg == None:
                continue
            label = seg['region_attributes']['name']
            seg['region_attributes']['name'] = label.replace("_", " ")
    
    # TODO: Write alldata after processing in file all.json
    os.chdir(dpath+'/Result/')
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


parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

folderNames = []
with open('./../completed.txt') as f:
    lines = f.readlines()
    for l in lines:
        if len(l)>3:
            folderNames.append(l.strip())

for folder in folderNames:
    dpath = args.dpath+"/"+folder
    if not os.path.isdir(dpath):
        print("not finding {}".format(folder))
        exit()
    print('Working on {}'.format(folder))
    
    join_via_files(dpath)
    f = open(dpath+'/Result/all.json')
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
    for data_i in data:
        img_name = data_i[0]
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

        seg_img = np.zeros((img.shape[0], img.shape[1],3), np.uint8)
        
        all_centers = []
        all_contours = []
        found_missing_labels = False
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
            
            if fuzz.partial_ratio('front top trunk', label) > 95: #cho dress
                color = c14
            elif fuzz.partial_ratio('front bottom trunk', label) > 95: #cho dress
                color = c15
            elif fuzz.partial_ratio('front trunk', label) > 95:
                color = c1
            elif fuzz.partial_ratio('front inner trunk', label) > 95:
                color = c2
            elif fuzz.partial_ratio('front left sleeve', label) > 95:
                color = c3
            elif fuzz.partial_ratio('front right sleeve', label) > 95:
                color = c4
            elif fuzz.partial_ratio('front right leg', label) > 95:
                color = c8
            elif fuzz.partial_ratio('front left leg', label) > 95:
                color = c10
            elif fuzz.partial_ratio('back bottom trunk', label) > 95:
                color = c18
            elif fuzz.partial_ratio('back top trunk', label) > 95:
                color = c19
            elif fuzz.partial_ratio('back trunk', label) > 95:
                color = c5
            elif fuzz.partial_ratio('back top', label) > 95:
                color = c5
            elif fuzz.partial_ratio('back right sleeve', label) > 95:
                color = c6
            elif fuzz.partial_ratio('back left sleeve', label) > 95:
                color = c7
            elif fuzz.partial_ratio('back right leg', label) > 95:
                color = c11
            elif fuzz.partial_ratio('back left leg', label) > 95:
                color = c12
            elif fuzz.partial_ratio('back inner trunk', label) > 95:
                color = c13
            elif fuzz.partial_ratio('background', label) > 95 or fuzz.partial_ratio('Background', label) > 95:
                color = c14
            elif fuzz.partial_ratio('front right long trunk', label) > 95 or fuzz.partial_ratio('Front right long trunk', label) > 95:
                color = c15
            elif fuzz.partial_ratio('front left long trunk', label) > 95 or fuzz.partial_ratio('Front left long trunk', label) > 95:
                color = c16
            elif fuzz.partial_ratio('extra', label) > 95:
                color = c17
            elif fuzz.partial_ratio('front inner left sleeve', label) > 95:
                color = c18
            elif fuzz.partial_ratio('front inner right sleeve', label) > 95:
                color = c19
            elif fuzz.partial_ratio('back inner left sleeve', label) > 95:
                color = c20
            elif fuzz.partial_ratio('back inner right sleeve', label) > 95:
                color = c21
            elif fuzz.partial_ratio('front inner right leg', label) > 95:
                color = c22
            elif fuzz.partial_ratio('front inner left leg', label) > 95:
                color = c23
            elif fuzz.partial_ratio('belly', label) > 95:
                color = c24
            elif fuzz.partial_ratio('removed', label) > 95:
                color = c25
            else:
                print(img_name)
                print(label)
                color = c9
                found_missing_labels = True
                missed_labels.append(img_name)

            color2 = ( int (color [ 0 ]), int (color [ 1 ]), int (color [ 2 ])) 
                    
            arr = np.array([x,y])
            center = arr.mean(1)
            all_centers.append([label, center])
            cv2.fillPoly(seg_img, pts = [np.transpose(arr)], color=color2)
        
            contour = np.transpose(arr)
            contour = np.expand_dims(contour, axis=1)
            all_contours.append(contour)
        overlayImg = overlayColor(img, seg_img)
        
        f = 'total label: {}'.format(len(data_i[1]))
        if len(data_i[1]) == 0:
            missed_labels.append(img_name)
            print(img_name)
            found_missing_labels = True

        fontsize = max(0.5,overlayImg.shape[0]/1024*0.5)
        overlayImg = cv2.putText(overlayImg, f, org, font, fontsize, (255, 0, 0), 1, cv2.LINE_AA)  
        
        for name_center in all_centers:
            name = name_center[0].strip()
            center = name_center[1]
            fontsize = max(0.5,overlayImg.shape[0]/1024*0.5)
            cv2.circle(overlayImg, (int(center[0]), int(center[1])), 2,  (0, 0, 255), thickness=2)
            overlayImg = cv2.putText(overlayImg, name, (int(center[0]), int(center[1])), font,fontsize, (0, 255, 0), 1, cv2.LINE_AA) 
        
        for contour in all_contours:
            col = list(np.random.choice(range(256), size=3))
            cv2.drawContours(overlayImg, contour, -1, ( int (col[ 0 ]), int (col [ 1 ]), int (col [ 2 ])), 4, cv2.FILLED)
            
        dot = img_name.find(".")
        if found_missing_labels:
            os.makedirs(dpath +"/results1/missing", exist_ok=True)
            fn = dpath +"/results1/missing/" + img_name[:dot]+".jpg"
        else:
            fn = dpath +"/results1/" + img_name[:dot]+".jpg"
        im_v = cv2.hconcat([img, overlayImg])
        cv2.imwrite(fn,im_v)
        
    if len(missed_labels)>0:
        print("{} has {} missing".format(folder, len(missed_labels)))
        fn = dpath +'/results1/missing_labels.txt'
        with open(fn, 'w') as fp:
            for item in missed_labels:
                fp.write("%s\n" % item)
    print('Done\n')