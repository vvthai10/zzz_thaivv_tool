"""
Description: Use data from project1, split it 2 folder: garment and model
@author: vvthai
"""
import os
import shutil
import argparse
from tqdm import tqdm

# python project2/processing_data.py "/mnt/d/Workspaces/viettechtool/Mock 2/VTT/Project 1 data/Hong/"
# /mnt/d/Workspaces/viettechtool/tools/project2

PROJECT2_PATH = "/mnt/d/Workspaces/viettechtool/tools/project2/data"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dpath")
    args = parser.parse_args()

    # Read all child folder
    folderNames = os.listdir(args.dpath)
    for folder in tqdm(folderNames, desc = "Processing"):
        '''
        Step:
         - Create folder project2/folder
         - Copy image have garment_[0,-1] to project2/folder/garment
         - Copy another images to project2/folder/model
        '''
        if "." in folder or "result" in folder:
            continue

        # create new folder
        new_folder_path = os.path.join(PROJECT2_PATH, folder)
        os.makedirs(new_folder_path, exist_ok=True)

        # create new child folders: garment and model
        garment_folder_path = os.path.join(new_folder_path, "garment")
        os.makedirs(garment_folder_path, exist_ok=True)
        model_folder_path = os.path.join(new_folder_path, "model")
        os.makedirs(model_folder_path, exist_ok=True)

        # read folder 
        folder_path = os.path.join(args.dpath, folder)
        fileNames = os.listdir(folder_path)
        for file in fileNames:
            file_path = os.path.join(folder_path, file)
            new_path = ""
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', ".webp")):
                if "_-1" in file or "_0" in file:
                    new_path = os.path.join(garment_folder_path, file)
                else:
                    new_path = os.path.join(model_folder_path, file)
            
                shutil.copy2(file_path, new_path)

