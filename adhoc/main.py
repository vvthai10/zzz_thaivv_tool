import pandas as pd
import glob
import os  
from rapidfuzz import fuzz 

SAVE_PATH = "/content/drive/MyDrive/viettechtools/Dataset"

def process_folder(folder, image):
    print(f"Processing folder: {folder} with image: {image}")
    path_phase = "/content/drive/MyDrive/viettechtools/Phase2"
    list_maker_folders = os.listdir(path_phase)
    for maker in list_maker_folders:
      folder_path = os.path.join(path_phase, maker)
      child_list_folders = [f for f in glob.glob(f"{folder_path}/**", recursive=True) if os.path.isdir(f)]
      for child_folder in child_list_folders:
        base_name = os.path.basename(child_folder)
        if fuzz.partial_ratio(base_name.lower(), folder.lower()) >= 95:
          target_folder = child_folder
          image_id = int(image.split("_")[-1])
          image_files = glob.glob(f"{target_folder}/{image_id}_*", recursive=True)

          if len(image_files) > 0:
            if not os.path.exists(f"{SAVE_PATH}/{image}"):
                os.makedirs(f"{SAVE_PATH}/{image}")
            else:
                continue
                
            for img_file in image_files:
                base_name = os.path.basename(img_file)
                save_file = f"{SAVE_PATH}/{image}/{base_name}"
                os.system(f"cp \"{img_file}\" \"{save_file}\"")

            print("Copy done ✅")
    


if __name__ == "__main__":
    
    df = pd.read_csv("/content/zzz_thaivv_tool/adhoc//map_phase.csv", header=0)
    map_phase = dict(zip(df["Spree phases"], df["VTT job number"]))
    
    folder_to_check = []
    
    with open("/content/zzz_thaivv_tool/adhoc/original_garment_folders.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            phase, folder, image = line.split("\t")
            
            num_phase = int(phase.split("_")[-1])
            vtt_phase = map_phase.get(num_phase, "-1")
            if vtt_phase == "-1":
                continue
            
            if phase == "Phase_002":
              print("... ", image)

            if not os.path.exists(f"{SAVE_PATH}/{image}"):
                os.makedirs(f"{SAVE_PATH}/{image}")
            else:
                continue

            if vtt_phase == 8: # and "womens_bottom_page_1" in folder
                process_folder("_".join(folder.split("_")[:-1]), image)
            
    # folder_to_check = list(set(folder_to_check))
    # print(folder_to_check)