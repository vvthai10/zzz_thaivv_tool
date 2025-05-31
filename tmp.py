import glob
import os
import argparse
from tqdm import tqdm

def split_txt_files(parent_folder):
    # Tìm tất cả file .txt trong folder cha và các folder con
    txt_files = glob.glob(os.path.join(parent_folder, '**', '*.txt'), recursive=True)
    
    for _,file_path in enumerate(tqdm(txt_files)):
        check_number = file_path.split("\\")[-1].split(".")[0]
        tmp_check_number = check_number.split("_")[0]
        if "mistake.txt" in file_path or "special.txt" in file_path or  "format.txt" in file_path or "models_special1_" in file_path or check_number.isnumeric() or tmp_check_number.isnumeric():
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_folder = os.path.dirname(file_path)
        output_folder = current_folder
        number_count = {}
        temp_lines = {}
        
        for line in lines:
            line = line.strip()  # Xóa ký tự xuống dòng
            
            if not line:  # Bỏ qua dòng trống
                continue

            if line.startswith('-'):
                for folder in number_count:
                    for number in number_count[folder]:
                        count = number_count[folder][number]
                        urls = temp_lines[folder][number]
                        
                        if count == 1:
                            # Nếu chỉ có 1 dòng, lưu thành number.txt
                            new_filename = f"{number}.txt"
                            new_file_path = os.path.join(folder, new_filename)
                            with open(new_file_path, 'w', encoding='utf-8') as new_f:
                                new_f.write(urls[0])
                        else:
                            # Nếu có nhiều hơn 1 dòng, lưu thành number_1.txt, number_2.txt, ...
                            for i, url in enumerate(urls, 1):
                                new_filename = f"{number}_{i}.txt"
                                new_file_path = os.path.join(folder, new_filename)
                                with open(new_file_path, 'w', encoding='utf-8') as new_f:
                                    new_f.write(url)
                                    
                # Lấy tên thư mục từ sau dấu - và bỏ dấu : ở cuối
                folder_name = line[1:].rstrip(':')
                # Tạo đường dẫn thư mục con
                output_folder = os.path.join(current_folder, folder_name)
                # Tạo thư mục nếu chưa tồn tại
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                # Reset đếm số khi chuyển thư mục
                number_count = {}
                temp_lines = {}
                continue
            
            try:
                parts = line.split('_', 1)  # Chia thành 2 phần tại dấu _ đầu tiên
                if len(parts) < 2:
                    raise IndexError
                number = parts[0]
                url = parts[1] 
                
                if output_folder not in number_count:
                    number_count[output_folder] = {}
                    temp_lines[output_folder] = {}
                if number not in number_count[output_folder]:
                    number_count[output_folder][number] = 0
                    temp_lines[output_folder][number] = []
                    
                number_count[output_folder][number] += 1
                temp_lines[output_folder][number].append(url)
            except IndexError:
                print(f"Lỗi: Dòng không đúng định dạng - {file_path}")
                print(f"Lỗi: Dòng không đúng định dạng - {line}")
                exit()
        
        for folder in number_count:
            for number in number_count[folder]:
                count = number_count[folder][number]
                urls = temp_lines[folder][number]
                
                if count == 1:
                    # Nếu chỉ có 1 dòng, lưu thành number.txt
                    new_filename = f"{number}.txt"
                    new_file_path = os.path.join(folder, new_filename)
                    with open(new_file_path, 'w', encoding='utf-8') as new_f:
                        new_f.write(urls[0])
                else:
                    # Nếu có nhiều hơn 1 dòng, lưu thành number_1.txt, number_2.txt, ...
                    for i, url in enumerate(urls, 1):
                        new_filename = f"{number}_{i}.txt"
                        new_file_path = os.path.join(folder, new_filename)
                        with open(new_file_path, 'w', encoding='utf-8') as new_f:
                            new_f.write(url)

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