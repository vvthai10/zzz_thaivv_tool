from PIL import Image
from pathlib import Path
import pillow_avif
import numpy as np
import glob
import cv2
import os
import json
from pathlib import Path  
import shutil 
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("dpath")
args = parser.parse_args()

if __name__ == "__main__":
    print(">>>>>>>>>>>>>>>>>>>>Count label<<<<<<<<<<<<<<<<<<")
    dpath = args.dpath
    
    cnt_whole_body = 0
    cnt_else = 0
    
        
    
    tmp_1 = ['Mr_P_men_shorts', 
        'Kingsman_men_suits', 
        'Gallery_dept_men_pants', 
        'Gallery_dept_men_jeans', 
        'Incotex_men_pants', 
        'Incotex_men_jeans', 
        'Mr_P_men_pants', 
        'Kapital_men_pants', 
        'lardini_men_pants', 
        'mackintosh_men_trousers_short', 
        'oneofthesedays_men_sweatpants', 
        'guestinresidence_women_bottom', 
        'richard_james_men_hoodies_sweats_t_shirts', 
        'maap_women_shorts', 
        'richard_james_men_suits', 
        'pasnormalstudios_womens_bottoms', 
        'klattermusen_men_pants', 
        'folkclothing_men_Trousers', 
        'klattermusen_men_pant', 
        'klattermusen_women_pants', 
        'rixolondon_women_co_ords', 
        'guestinresidence_men_bottom', 
        'richard_james_men_nightwear', 
        'Pasadena_leisure_club_men_pants', 
        'rapha_men_shorts_trousers', 
        'purdey_men_trousers', 
        'rapha_women_bottoms', 
        'johnsmedley_women_dresses', 
        'neighborhood_men_bottom', 
        'dunhill_men_Trousers', 
        'gfore_women_skorts_dresses', 
        'klattermusen_women_shorts',
        'johnsmedley_men_loungewear',
        'dunhill_men_Suits',
        'klattermusen_men_shorts',
        'oakley_men_bottom',
        'rockyourbaby_girls_bottoms',
        'ysl_men_jacket_pants',
        'rmwilliams_men_jeans',
        'woolworths_men_Sleepwear',
        'twothirds_kids_one_pieces',
        'rockyourbaby_girls_swimwear',
        'twothirds_men_trousers',
        'twothirds_women_jumpsuits',
        'rockyourbaby_boys_bottoms',
        'rockyourbaby_girls_rompers_jumpsuits',
        'rockyourbaby_boys_swimwear',
        'rockyourbaby_boys_swimwear',
        'rixolondon_women_skirts'
        ]

    tmp_2 = ['ELISABETTAFRANCHI_WOMEN_TAILORING', 'DELCORE_WOMEN_TAILORING', 'ELISABETTAFRANCHI_WOMEN_SKIRTS', 'ELISABETTAFRANCHI_WOMEN_TROUSERS', 'FUZZYMORE_WOMEN_PANTS', 'EPHEMERA_WOMEN_RESORTWEARS', 'BUFFALODAVIDBITTON_WOMEN_SKIRTS_SHORTS', 'FUZZYMORE_WOMEN_JUMPSUITS', 'FUZZYMORE_WOMEN_JUMPSUITS', 'GOLDENGOOSE_BOY_CLOTHING', 'DELCORE_WOMEN_SHORTS_TROUSER', 'Blind_no_plan_Men_Bottoms', 'FUZZYMORE_WOMEN_SKIRTS', 'CIAOLUCIA_WOMEN_BOTTOMS', 'GOLDENGOOSE_GIRL_CLOTHING', 'CIAOLUCIA_WOMEN_DRESS', 'DELCORE_WOMEN_DRESS_JUMPSUITS', 'GOLDENGOOSE_MEN_JEANS_PANTS', 'DELCORE_WOMEN_SKIRTS', 'INDUSTRIEAFRICA_WOMEN_DRESS', 'GOLDENGOOSE_WOMEN_DRESS_JUMPSUITS', 'GOLDENGOOSE_WOMEN_JEANS_PANTS', 'gender_women_pants_shorts', 'INDUSTRIEAFRICA_WOMEN_PANTS', 'INDUSTRIEAFRICA_WOMEN_SWIMWEAR', 'INDUSTRIEAFRICA_WOMEN_SWIMWEAR', 'NORSEPROJECTS_MEN_SHORTS', 'NORSEPROJECTS_MEN_TROUSER', 'OAS_MEN_PANTS', 'OAS_MEN_SHORTS', 'OAS_WOMEN_SHORTS', 'ONEOFTHESEDAYS_MEN_PANTS', 'ONEOFTHESEDAYS_MEN_SWEATPANTS', 'gender_women_dresses_skirts', 'Ariadna_Women_Bottoms', 'Ariadna_Women_Dresses', 'Anno_mundi_Women_Bottoms', 'Anno_mundi_Women_Bottoms', '2THELITTLESTORE_WOMEN_DRESS', '2THELITTLESTORE_WOMEN_JUMPSUITS', '2THELITTLESTORE_WOMEN_TROUSERS', 'AHLUWALIA_MEN_SHORTS', 'AHLUWALIA_MEN_TROUSERS', 'AHLUWALIA_WOMEN_SWEATPANTS', 'AHLUWALIA_WOMEN_TRACKSUITS', 'AHLUWALIA_WOMEN_TROUSERS', 'APPLIEDARTFORMS_MEN_SHORTS_TROUSERS', 'Alinnv_Women_Bottoms', 'Alinnv_Women_Bottoms', 'Alinnv_Women_Dresses', 'Alinshouse_Women_Bottoms', 'Anno_mundi_Women_Dresses', 'Anyfood_Universe_Women_Bottoms', 'BUFFALODAVIDBITTON_MEN_JEANS', 'BUFFALODAVIDBITTON_MEN_SHORTS', 'BUFFALODAVIDBITTON_WOMEN_JEANS', 'BUFFALODAVIDBITTON_WOMEN_JUMPSUITS_DRESS', 'BUFFALODAVIDBITTON_WOMEN_JUMPSUITS_DRESS']


    
    
    print(set(tmp_1) & set(tmp_2))
    
    
    json_file_list = glob.glob(os.path.join(dpath, "**/*.json"), recursive=True)
    tmp = []
    cnt = 0
    # print(len(json_file_list))
    # print(json_file_list)
    for json_file in tqdm(json_file_list):
        
            
        # name = json_file.split("\\")[-3]
        # if "special" in json_file:
        #     name = json_file.split("\\")[-4]
            
        # if name not in tmp_1:
        #     continue
        # cnt += 1
        
        # if "special" in json_file:
        #     tmp.append(json_file.split("\\")[-4:])
        # else:
        #     tmp.append(json_file.split("\\")[-3:])
        
        with open(json_file,'r', encoding="utf8") as f:
            data = json.load(f)
        for name in data:
            labels = json.dumps(data[name]['labels'])
            if "whole-body" in labels:
                cnt_whole_body += 1
            if "top" in labels or "bottom" in labels:
                cnt_else += 1
    
    print(f"whole_body_{cnt_whole_body}_else_{cnt_else}")
    with open(f"{dpath}/whole_body_{cnt_whole_body}_else_{cnt_else}.txt", "w") as f:
        pass
    