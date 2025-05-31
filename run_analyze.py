import subprocess

project3_path = "G:\\.shortcut-targets-by-id\\1g3WkCvNoD7IgPMIfFdWUU3sZrFXxR0Nv\\Project 3 - Group8 - Phase71-80\\Phase72 - Job 96/"

# Danh sách các tham số
params = [
    {"dpath": "G:\\.shortcut-targets-by-id\\11XdxCzX6-8v4ONGSZY-wIDv_XJhHvsFl\\Project 1 - Phase13 - Job 101 - 110\\Job 108\\Dinh Dat/"},
]

# Phase 64; Phase 77; Phase 79

# Lệnh Python cơ bản
base_command = "python .\\project3\\re_make_images.py"

# Duyệt qua từng tham số và chạy lệnh
for param in params:
    input_file = param["dpath"]
    # project3_path = param["project3_path"]
    command = f'{base_command} "{input_file}" "{project3_path}"'
    
    print(f"Running: {command}")
    subprocess.run(command, shell=True)
