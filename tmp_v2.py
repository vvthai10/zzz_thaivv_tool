import glob
import os
import argparse
from tqdm import tqdm

def split_txt_files(parent_folder):
    # Tìm tất cả file .txt trong folder cha và các folder con
    txt_files = glob.glob(os.path.join(parent_folder, '**', '*.txt'), recursive=True)
    
    for _,file_path in enumerate(tqdm(txt_files)):
        check_number = file_path.split("\\")[-1].split(".")[0]
        if check_number.isnumeric():
            os.remove(file_path)
        

def main():
    if os.path.exists(dpath):
        split_txt_files(dpath)
        print("Hoàn thành!")
    else:
        print("Folder không tồn tại!")

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

if __name__ == "__main__":
    dpath = args.dpath
    main()