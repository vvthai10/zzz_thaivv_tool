import os
import re

def find_image_files(folder_path):
    # Biểu thức chính quy để tìm file có tên dạng '_.*' và định dạng ảnh phổ biến
    image_pattern = re.compile(r"_.(png|jpg|jpeg|bmp|gif|tiff|webp)$", re.IGNORECASE)

    matched_files = []

    # Duyệt qua tất cả các thư mục con
    for root, _, files in os.walk(folder_path):
        for file in files:
            if image_pattern.search(file):
                matched_files.append(os.path.join(root, file))

    return matched_files

# Sử dụng hàm
folder_path = "G:\\.shortcut-targets-by-id\\13pReWsG8y7Uzqyu8wYYnKe5vLd_bcA7e\\Project 1 - Phase19 - Job 161 - 170\\Job 167_03_2025\\Thien"
image_files = find_image_files(folder_path)

print("Các file hình ảnh tìm thấy:")
for img in image_files:
    print(img)
