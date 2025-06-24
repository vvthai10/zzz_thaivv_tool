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

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

import os
import shutil
import glob

def get_map_json(path):
    print("get map json")
    results = {}
    json_path_list = glob.glob(os.path.join(path, "**/*.json"), recursive=True)
    for json_path in tqdm(json_path_list):
        folder = Path(json_path).parts[-3]
        if "special" in folder:
            folder = Path(json_path).parts[-4]
            
        # init object
        if folder not in results.keys():
            results[folder] = {
                "main": [],
                "special": []
            }
        
        # add json path
        if "special" in json_path:
            results[folder]["special"].append(json_path)
        else:
            results[folder]["main"].append(json_path)
            
    return results

if __name__ == "__main__":
    print("================= MERGE RESULTS ===================")
    dpath = args.dpath
    
    main_results = os.path.join(dpath, "Results")
    new_results = os.path.join(dpath, "New/Results")
    merge_results = os.path.join(dpath, "results_merge")
    
    
    if not os.path.exists(main_results) or not os.path.exists(new_results):
        print("Can't process: Not contain 2 results folder")
        exit()
    
    if os.path.exists(merge_results):
        shutil.rmtree(merge_results)
    os.makedirs(merge_results)
    
    main_map = get_map_json(main_results)
    new_map = get_map_json(new_results)
    
    """
        - Case 1: folder just in main -> Copy to results_merge
        - Case 2: folder just in special -> Copy to results_merge
        - Case 3: folder in both:
            - Not duplicate file json -> Copy to results_merge
            - Duplicate json file ...
    """
    print("merge results...")
    processed_folder = []
    for folder in tqdm(main_map.keys()):
        processed_folder.append(folder)
        if folder not in new_map.keys():
            main_json = main_map[folder]["main"][0]
            src_path = "/".join(Path(main_json).parts[:-1])
            dst_path = src_path.replace("Results", "results_merge")
            shutil.copytree(src_path, dst_path)
            
            for special_json in main_map[folder]["special"]:
                src_path = "/".join(Path(special_json).parts[:-1])
                dst_path = src_path.replace("Results", "results_merge")
                shutil.copytree(src_path, dst_path)
        else:
            # process main results
            n_main = len(main_map[folder]["main"])
            n_new_main = len(new_map[folder]["main"])
            if n_main != 0 and n_new_main != 0:
                print(f"folder {folder} has case n_main != 0 and n_new_main != 0")
                pass
            elif n_main == 0 and n_new_main != 0:
                print(f"folder {folder} has case n_main == 0 and n_new_main != 0")
                pass
            elif n_main != 0 and n_new_main == 0:
                main_json = main_map[folder]["main"][0]
                src_path = "/".join(Path(main_json).parts[:-1])
                dst_path = src_path.replace("Results", "results_merge")
                shutil.copytree(src_path, dst_path)
            
            # process special results
            n_special = len(main_map[folder]["special"])
            n_new_special = len(new_map[folder]["special"])
            if n_special != 0 and n_new_special != 0:
                print(f"folder {folder} has case n_special != 0 and n_new_special != 0")
                pass
            elif n_special == 0 and n_new_special != 0:
                for special_json in new_map[folder]["special"]:
                    src_path = "/".join(Path(special_json).parts[:-1])
                    dst_path = src_path.replace("New/Results", "results_merge")
                    shutil.copytree(src_path, dst_path)
            elif n_special != 0 and n_new_special == 0:
                print(f"folder {folder} has case n_special != 0 and n_new_special == 0")
                pass
            
        
    for folder in tqdm(new_map.keys()):
        if folder not in processed_folder:
            if len(new_map[folder]["main"]) != 0:
                main_json = new_map[folder]["main"][0]
                src_path = "/".join(Path(main_json).parts[:-1])
                dst_path = src_path.replace("New/Results", "results_merge")
                shutil.copytree(src_path, dst_path)
            
            for special_json in new_map[folder]["special"]:
                src_path = "/".join(Path(special_json).parts[:-1])
                dst_path = src_path.replace("New/Results", "results_merge")
                shutil.copytree(src_path, dst_path)
            
            
        
    
        
