import subprocess

ROOT_PATH = "/content/drive/MyDrive/viettechtools/"

project3_path = ROOT_PATH + "Project 3 - Group8 - Phase71-80/Phase72 - Job 96/"
project1_path = ROOT_PATH + "Project 1 - Phase12 - Job 91 - 100/Job 96/"

# Danh sách các tham số
# params = [
#     {"dpath": ROOT_PATH + "Project 1 - Phase12 - Job 91 - 100\Job 96/Duy Phung/"},
#     {"dpath": ROOT_PATH + "Project 1 - Phase12 - Job 91 - 100\Job 96/Minh Chinh/"},
#     {"dpath": ROOT_PATH + "Project 1 - Phase12 - Job 91 - 100\Job 96/Minh Nhat/"},
#     {"dpath": ROOT_PATH + "Project 1 - Phase12 - Job 91 - 100\Job 96/Quang Hai/"},
#     {"dpath": ROOT_PATH + "Project 1 - Phase12 - Job 91 - 100\Job 96/Van Sang/"},
# ]
params = []
for maker in ["Duy Phung"]: #, "Minh Chinh", "Minh Nhat", "Quang Hai", "Van Sang"
    params.append({"dpath": project1_path + maker + "/"})

# Phase 64; Phase 77; Phase 79

# Lệnh Python cơ bản
base_command = "python ./project3/re_make_images.py"

# Duyệt qua từng tham số và chạy lệnh
for param in params:
    input_file = param["dpath"]
    # project3_path = param["project3_path"]
    command = f'{base_command} "{input_file}" "{project3_path}"'
    
    print(f"Running: {command}")
    subprocess.run(command, shell=True)
