import os
import json
import glob
import argparse

def process_txt_file(txt_path):
    # Đọc file txt
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_path = ""
    keys_to_remove = set()
    
    for line in lines:
        line = line.strip()
        
        if not line.startswith('-'):
            if current_path and keys_to_remove:
                process_json_files(current_path, keys_to_remove)
            current_path = line
            keys_to_remove = set()
        else:
            key = line.lstrip('- ').strip()
            keys_to_remove.add(key)
    
    if current_path and keys_to_remove:
        process_json_files(current_path, keys_to_remove)

def process_json_files(directory, keys_to_remove):
    directory_path =  os.path.join(dpath, directory)
    json_pattern = os.path.join(directory_path, "**", "*.json")
    all_json_files = glob.glob(json_pattern, recursive=True)
    for json_path in (all_json_files):
        if json_path.endswith('.json'):
            
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                modified = False
                for key in keys_to_remove:
                    if key in data:
                        del data[key]
                        modified = True
                
                if modified:
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    print(f"Updated file: {json_path}")
                    
            except Exception as e:
                print(f"Error processing {json_path}: {str(e)}")


def main():
    if os.path.exists(txt_file_path):
        process_txt_file(txt_file_path)
    else:
        print("File txt không tồn tại!")

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()


if __name__ == "__main__":
    dpath = args.dpath
    txt_file_path = dpath + "\\Results\\error.txt"
    
    main()