import cv2
import numpy as np
import json
import tqdm
import os

map_dict = {0: "background", 1: "top" , 2: "panty | skirt",  3: "dress | jumpsuit | 1-piece swimwear | whole body long", 4: "left sleeves", 5: "right sleeves", 6: "left pants",
       7: "right pants", 8: "left hand skin | right hand skin | left leg skin | right leg skin | body skin | face skin", 9: "hair", 10: "left shoes | right shoes | left boots | right boots", 11: "left tights | right tights | left socks | right socks", 
       12: "band | watch | ring | gloves | glasses | hair accessories| person earring | person bag | mask | scarf | hat"}

map_color_rgb = {0: (0, 0, 0), 1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 0), 4: (255, 255, 0), 5: (0, 255, 255), 6: (255, 0, 255),
    7: (128, 128, 128), 8: (128, 0, 128), 9: (128, 0, 0), 10: (0, 128, 0), 11: (0, 0, 128), 12: (128, 128, 0), 13: (0, 128, 128),
    14: (255, 128, 0), 15: (128, 255, 0), 16: (0, 128, 255), 17: (255, 0, 128), 18: (128, 0, 255), 19: (0, 255, 128), 20: (255, 128, 128),
    21: (128, 255, 128), 22: (128, 128, 255), 23: (255, 255, 128), 24: (255, 128, 255), 25: (128, 255, 255), 26: (192, 192, 192), 27: (64, 64, 64), 
    28: (192, 64, 64), 29: (64, 192, 64)}

def map_26_classes(segmentation):
    """
    Maps the segmentation mask to 26 classes.
    """
    lut = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 15, 6: 16,
           7: 17, 8: 18, 9: 11, 10: 14, 11: 12, 12: 23, 13: 5,
           14: 6, 15: 13, 16: 5, 17: 9, 18: 10, 19: 21,
           20: 22, 21: 19, 22: 20, 23: 8, 24: 8, 25: 8, 26: 8, 27: 7, 28: 14, 29: 7}
    # unique_classes = np.unique(segmentation)
    # if 16 in unique_classes and 13 in unique_classes:
    #     lut[16] = 5
    #     lut[13] = 7
    mapped = np.copy(segmentation)
    for k, v in lut.items():
        mapped[segmentation == k] = v
    return mapped

def map_13_classes(segmentation):
    """
    Maps the segmentation mask to 13 classes.
    """
    lut = {0: 0, 1: 12, 2: 9, 3: 12, 4: 12, 5: 12,
           6: 12, 7: 12, 8: 8, 9: 8, 10: 8, 11: 8,
            12: 8, 13: 8, 14: 12, 15: 12, 16: 1,
            17: 3, 18: 2, 19: 6, 20: 7, 21: 4,
            22: 5, 23: 10, 24: 10, 25: 10, 26: 10, 27: 11, 28: 11, 29:11, 30:11, 31:12, 32:3, 33:2, 33:2, 34:12, 35:3}
    unique_classes = np.unique(segmentation)

    mapped = np.copy(segmentation)
    for k, v in lut.items():
        mapped[segmentation == k] = v
    return mapped

def create_bitmap(mask, polygon, value, color=True):
    polygon = np.array(polygon, dtype=np.int32)
    cv2.fillPoly(mask, [polygon], color=(map_color_rgb[value]) if color else (value))
    return mask

def create_polygon_mask(mask, polygon):
    polygon = np.array(polygon, dtype=np.int32)
    cv2.polylines(mask, [polygon], isClosed=True, color=(255), thickness=2)
    return mask

dpath = 'D:\\fix_viettech\\cvat\\phase1'

json_data = json.load(open(f'{dpath}/result/all.json'))
enable_viz = True
for data in tqdm.tqdm(json_data):
    # data = json_data[0]
    if not os.path.exists(f'{dpath}/'+data[0]):
        continue

    print(data[0])
    seg = cv2.imread(f'{dpath}/'+data[0])

    if seg is None:
        # raise FileNotFoundError(f"Image file not found: {dpath}/{data[0]}")
        continue

    mask_output = np.zeros((seg.shape[0], seg.shape[1]), dtype=np.uint8)
    for annotation in data[1]:
        print(annotation)
        all_points_x = annotation["shape_attributes"]["all_points_x"]
        all_points_y = annotation["shape_attributes"]["all_points_y"]
        vertices = [[x,y] for x, y in zip(all_points_x, all_points_y)]
        mask_output = create_polygon_mask(mask_output, vertices)
    mask_output = cv2.cvtColor(mask_output, cv2.COLOR_GRAY2BGR)

    mask_output2 = np.zeros((seg.shape[0], seg.shape[1],3), dtype=np.uint8)
    masks_map = {}
    saved_top = None
    for annotation in data[1][::-1]:
        all_points_x = annotation["shape_attributes"]["all_points_x"]
        all_points_y = annotation["shape_attributes"]["all_points_y"]
        vertices = [[x, y] for x, y in zip(all_points_x, all_points_y)]
        label = annotation["region_attributes"]["name"]
        print(label)
        # if label != "top":
        #     continue
        if "top" in label:
            if label.split()[-1].isdigit():
                mask_output2 = create_bitmap(mask_output2, vertices, 29, color=enable_viz)
                if saved_top is not None:
                    mask_output2 = create_bitmap(mask_output2, saved_top, 13, color=enable_viz)
            else:
                mask_output2 = create_bitmap(mask_output2, vertices, 13, color=enable_viz)
                saved_top = vertices

        else:
            label = ' '.join([i for i in label.split() if not i.isdigit()])
            label = label.replace('boots', 'shoes')
            # print(label)
            for i in map_dict:
                if label in map_dict[i]:
                    value = i
                    mask_output2 = create_bitmap(mask_output2, vertices, value, color=enable_viz)

    # # Fill only very small holes (0 regions) completely surrounded by other values in mask_output2
    # mask_gray = cv2.cvtColor(mask_output2, cv2.COLOR_BGR2GRAY)
    # # Find all 0 regions (holes)
    # holes = (mask_gray == 0).astype(np.uint8)
    # # Find connected components in holes
    # num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(holes, connectivity=8)
    # # Set a threshold for "very small" holes (e.g., area < 50 pixels)
    # small_hole_thresh = 50
    # for i in range(1, num_labels):
    #     area = stats[i, cv2.CC_STAT_AREA]
    #     if area < small_hole_thresh:
    #         mask = (labels == i)
    #         # Get the bounding box of the hole
    #         x, y, w, h = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
    #         # Get the border pixels around the hole
    #         border = cv2.dilate(mask.astype(np.uint8), np.ones((3, 3), np.uint8), iterations=1) - mask.astype(np.uint8)
    #         border_vals = mask_output2[y:y+h, x:x+w][border[y:y+h, x:x+w] == 1]
    #         if len(border_vals) > 0:
    #             # Use the most common color on the border to fill the hole
    #             vals, counts = np.unique(border_vals.reshape(-1, 3), axis=0, return_counts=True)
    #             fill_color = vals[np.argmax(counts)]
    #             mask_output2[mask] = fill_color
    # if 30 in np.unique(mask_output2):
    #     continue

    mask_output2 = map_13_classes(mask_output2)
    # print(np.unique(mask_output2))
    # print(f'Data1/val/all/Data1_val_masks/{data[0]}.png')
    # cv2.imwrite(f'Data1/train/all/Data1_train_masks/{data[0]}.png', mask_output2)
    mask_output2 = cv2.hconcat([seg, mask_output2, mask_output])
    # mask_output2[mask_output2 == 18] = 255
    fname = dpath+'/mask/'+data[0]
    cv2.imwrite(fname, mask_output2)