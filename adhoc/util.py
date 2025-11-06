import pandas as pd
import glob
import os   

SAVE_PATH = "D:\\fix_viettech\\Dataset"

def process_folder(folder, image):
    print(f"Processing folder: {folder} with image: {image}")
    path_phase = "D:\\fix_viettech\\Phase 1"
    matches = glob.glob(f"{path_phase}/**/{folder}", recursive=True)
    if len(matches) != 1:
        print(f"Some mistake in matches folder: {folder}")
        print(matches)
        return
    
    target_folder = matches[0]
    image_id = int(image.split("_")[-1])
    image_files = glob.glob(f"{target_folder}/{image_id}_*", recursive=True)
    
    if not os.path.exists(f"{SAVE_PATH}/{image}"):
        os.makedirs(f"{SAVE_PATH}/{image}")
        
    for img_file in image_files:
        base_name = os.path.basename(img_file)
        save_file = f"{SAVE_PATH}/{image}/{base_name}"
        os.system(f"copy \"{img_file}\" \"{save_file}\"")
    


if __name__ == "__main__":
    
    df = pd.read_csv("./map_phase.csv", header=0)
    map_phase = dict(zip(df["Spree phases"], df["VTT job number"]))
    
    folder_to_check = []
    
    with open("./original_garment_folders.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            phase, folder, image = line.split("\t")
            
            num_phase = int(phase.split("_")[-1])
            vtt_phase = map_phase.get(num_phase, "-1")
            if vtt_phase == "-1":
                continue
            
            if vtt_phase == 1 and "womens_bottom_page" in folder:
                process_folder("_".join(folder.split("_")[:-1]), image)
                exit()
            
    # folder_to_check = list(set(folder_to_check))
    # print(folder_to_check)