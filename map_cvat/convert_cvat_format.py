import cv2
import numpy as np
import json
from tqdm import tqdm
import os
import shutil 
from PIL import Image, ImageDraw
import argparse
import re
import shutil

map_dict = {0: "background", 1: "top" , 2: "panty | skirt",  3: "dress | jumpsuit | 1-piece swimwear | whole body long", 4: "left sleeves", 5: "right sleeves", 6: "left pants",
       7: "right pants", 8: "left hand skin | right hand skin | left leg skin | right leg skin | body skin | face skin", 9: "hair", 10: "left shoes | right shoes | left boots | right boots", 11: "left tights | right tights | left socks | right socks", 
       12: "band | watch | ring | gloves | glasses | hair accessories| person earring | person bag | mask | scarf | hat"}

map_color_rgb = {0: (0, 0, 0), 1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 0), 4: (255, 255, 0), 5: (0, 255, 255), 6: (255, 0, 255),
    7: (128, 128, 128), 8: (128, 0, 128), 9: (128, 0, 0), 10: (0, 128, 0), 11: (0, 0, 128), 12: (128, 128, 0), 13: (0, 128, 128),
    14: (255, 128, 0), 15: (128, 255, 0), 16: (0, 128, 255), 17: (255, 0, 128), 18: (128, 0, 255), 19: (0, 255, 128), 20: (255, 128, 128),
    21: (128, 255, 128), 22: (128, 128, 255), 23: (255, 255, 128), 24: (255, 128, 255), 25: (128, 255, 255), 26: (192, 192, 192), 27: (64, 64, 64), 
    28: (192, 64, 64), 29: (64, 192, 64)}

LABEL_JSON_PATH = "/content/zzz_thaivv_tool/map_cvat/labels.json"
BACKGROUND_COLOR = None

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

with open(LABEL_JSON_PATH, "r") as f:
    label_colors = json.load(f)

label2id = {}
for item in label_colors:
    class_name = item["name"]
    class_id = item["id"]
    rgb = hex_to_rgb(item["color"])
    map_color_rgb[class_id] = rgb 
    label2id[class_name] = class_id
    if class_name == "background":
        BACKGROUND_COLOR = rgb
    
# for id_, names in map_dict.items():
#     for name in names.split('|'):
#         label2id[name.strip()] = id_
    
parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()
dpath = args.dpath

cvat_path = os.path.join(dpath, "cvat_format")
if os.path.exists(cvat_path):
   shutil.rmtree(cvat_path) 

os.makedirs(os.path.join(cvat_path, "ImageSets/Segmentation"), exist_ok=True)
os.makedirs(os.path.join(cvat_path, "SegmentationClass"), exist_ok=True)
os.makedirs(os.path.join(cvat_path, "SegmentationObject"), exist_ok=True)

try:
  with open(os.path.join(dpath, "result/all.json"), "r") as f:
    data = json.load(f)
except:
  with open(os.path.join(dpath, "Result/all.json"), "r") as f:
    data = json.load(f)

default_txt = []

for entry in tqdm(data):
    image_name, annotations = entry
    base_name = os.path.splitext(image_name)[0]
    
    # if base_name not in ["DressCode_dresses_images_021950_0.jpg", "DressCode_dresses_images_021972_0.jpg"]:
    #     continue
    
    image_path = os.path.join(dpath, image_name)
    # NOTE: condition use to dev tool
    if not os.path.exists(image_path):
        continue
    
    default_txt.append(base_name)
    try:
        with Image.open(image_path) as im:
            width, height = im.size
    except Exception as e:
        raise FileNotFoundError(f"Image file not found: {dpath}/{data[0]}")
    
    mask_class = Image.new("RGB", (width, height), color=BACKGROUND_COLOR)
    draw_class = ImageDraw.Draw(mask_class)

    mask_vis = Image.new("L", (width, height), 0)
    draw_vis = ImageDraw.Draw(mask_vis)
    obj_id = 1
    
    
    for ann in annotations:
        if ann is None:
          continue
        label = ann["region_attributes"]["name"].strip()
        label = re.sub(r'[0-9]+', '', label)
        # if label == "background":
        #     print(f"Warning: have background label in {image_name}")
        if label.split()[-1].isdigit():
            label = " ".join(label.split()[:-1])
        label = label.replace("  ", " ")
        if "top_" in label:
            label = "top"
        if "inner" in label:
            label = "inner top"
        if "-piece swimwear" in label:
            label = "1-piece swimwear"
        if "ing" in label:
            label = "ring"
        if "hair accessories" in label or "hair acccessory" in label:
            label = "hair accessory"
        if "left sleeve" in label:
            label = "left sleeves"
        if "right sleeve" in label or "rigth sleeves" in label:
            label = "right sleeves"
        if "left hand skind" in label:
            label = "left hand skin"
        if "face skinskinned" in label:
            label = "face skin"
        if "right  boots" in label:
            label = "right boots"
        if "left  boots" in label or "left bootes" in label or "leef boots" in label:
            label = "left boots"
        if "lef socks" in label:
            label = "left socks"
        if "skin body" in label or "body dkin" in label:
            label = "body skin"
        if "left sleeeves" in label or "left sleevs" in label:
            label = "left sleeves"
        if "body panty" in label:
            label = "panty"
        if "left tigts" in label or "leftf tights" in label:
            label = "left tights"
        if "scaft" in label:
            label = "scarf"
        if "backrground" in label or "backgroud" in label:
            label = "background"
        if "oerson bag" in label:
            label = "person bag"
        if "right sọcks" in label:
            label = "right socks"
        if "body panty" in label:
            label = "panty"
        if "body panty" in label:
            label = "panty"
        if "body panty" in label:
            label = "panty"
        if "body panty" in label:
            label = "panty"
        if "body panty" in label:
            label = "panty"

        if "not defined" in label:
          continue

        shape = ann["shape_attributes"]
        try:
          class_id = label2id[label.strip()]
        except:
          print(base_name)
          class_id = label2id[label.strip()]
          exit()
        color = map_color_rgb[class_id]
        poly = list(zip(shape["all_points_x"], shape["all_points_y"]))

        draw_class.polygon(poly, fill=color)
        draw_vis.polygon(poly, fill=obj_id)
        obj_id += 1

    mask_class.save(os.path.join(cvat_path, f"SegmentationClass/{base_name}.png"))
    mask_vis.save(os.path.join(cvat_path, f"SegmentationObject/{base_name}.png"))
    
    with open(os.path.join(cvat_path, "ImageSets/Segmentation/default.txt"), "w") as f:
        for name in default_txt:
            f.write(name + "\n")
            
    if os.path.exists(LABEL_JSON_PATH):
        with open(LABEL_JSON_PATH, "r") as f:
            label_data = json.load(f)

        with open(os.path.join(cvat_path, "labelmap.txt"), "w") as f:
            f.write("# label:color_rgb:parts:actions\n")
            for item in label_data:
                name = item["name"]
                rgb = hex_to_rgb(item["color"])
                rgb_str = ",".join(str(c) for c in rgb)
                f.write(f"{name}:{rgb_str}::\n")
                
ZIP_NAME = os.path.join(dpath, "cvat_format")
shutil.make_archive(ZIP_NAME, 'zip', cvat_path)