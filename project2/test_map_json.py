import json

# File gốc và file all
with open('D:\\fix_viettech\\Phase1\\result\\z_1.json', 'r') as f:
    z1_data = json.load(f)

with open('D:\\fix_viettech\\Phase1\\result\\updates_all.json', 'r') as f:
    all_data = json.load(f)

# Chuyển all.json sang dict dạng: filename -> regions
all_dict = {}
for item in all_data:
    filename = item[0]
    regions = item[1]
    all_dict[filename] = regions

# Cập nhật regions trong z1_data
for img_key, img_data in z1_data['_via_img_metadata'].items():
    filename = img_data['filename']
    if filename in all_dict:
        new_regions = []
        for region in all_dict[filename]:
            new_regions.append({
                "shape_attributes": region['shape_attributes'],
                "region_attributes": region['region_attributes']
            })
        img_data['regions'] = new_regions

# Xuất ra file mới
with open('D:\\fix_viettech\\Phase1\\result\\z_1_updated.json', 'w') as f:
    json.dump(z1_data, f, indent=2)
