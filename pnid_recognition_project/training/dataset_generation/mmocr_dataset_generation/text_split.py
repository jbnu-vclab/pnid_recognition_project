import sys
sys.path.append('../../../..')

import os
import os.path as osp
import cv2
import json
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from pnid_recognition_project.common.xml_data import XMLData

def segment_text_images(img_path, xml_path, out_dir, ann, scale):
    img = cv2.imread(img_path)
    base_filename = osp.basename(xml_path).replace(".xml", "")

    if XMLData.is_twopoint_format(xml_path):
        xml_data = XMLData().from_twopoint_xml(xml_path)
    else:
        xml_data = XMLData().from_fourpoint_xml(xml_path)

    img_index = 0
    for symbol_object in xml_data.symbol_object_list:
        if not symbol_object.is_text:
            continue

        x,y,w,h = symbol_object.get_aabb() # x,y,w,h
        crop_img = img[y:y+h, x:x+w]
        if h <= 0 or w <= 0:
            continue

        if symbol_object.degree != 0: # if rotated, invert the rotation
            (cX, cY) = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D((cX, cY), -symbol_object.degree, 1.0)

            # new image size
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            nW = int((h * sin) + (w * cos))
            nH = int((h * cos) + (w * sin))
            M[0, 2] += (nW / 2) - cX
            M[1, 2] += (nH / 2) - cY

            rotated_img = cv2.warpAffine(crop_img, M, (nW, nH))

            origin_width = (symbol_object.max_point.x - symbol_object.min_point.x)
            origin_height = (symbol_object.max_point.y - symbol_object.min_point.y)
            if origin_height <= 0 or origin_width <= 0:
                continue

            rotated_minx = int((nW//2) - origin_width/2)
            rotated_miny = int((nH//2) - origin_height/2)
            crop_img = rotated_img[rotated_miny:rotated_miny+origin_height, rotated_minx:rotated_minx+origin_width]

        if scale != 1: # if scaled, simple scale the cropped img
            crop_img = cv2.resize(crop_img, dsize=(0,0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        # write cropped image
        out_img_filename = f'{base_filename}_{img_index}.jpg'
        out_img_path = osp.join(out_dir, out_img_filename)
        cv2.imwrite(out_img_path, crop_img)

        # https://github.com/open-mmlab/mmocr/blob/main/mmocr/datasets/recog_text_dataset.py
        ann.append({'filename': out_img_filename, 'text': symbol_object.cls})

        img_index += 1

def do_text_split(img_dir, xml_dir, phase, target_filenames, out_dir, scale):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    textrecog_ann = []
    xml_files = [f for f in os.listdir(xml_dir) if 'xml' in osp.splitext(f)[1] and osp.splitext(f)[0] in target_filenames]
    img_files = [f for f in os.listdir(img_dir) if 'jpg' in osp.splitext(f)[1] or 'png' in osp.splitext(f)[1]]
    img_files = [f for f in img_files if osp.splitext(f)[0] in target_filenames]

    for xml_file in tqdm(xml_files):
        xml_filename = osp.splitext(xml_file)[0]
        corr_img_files = [f for f in img_files if xml_filename in f]

        if len(corr_img_files) == 1:
            img_file = corr_img_files[0]
        else:
            continue

        xml_path = osp.join(xml_dir, xml_file)
        img_path = osp.join(img_dir, img_file)

        segment_text_images(img_path, xml_path, out_dir, textrecog_ann, scale)

    ann_path = osp.join(out_dir, f'ann_{phase}.json')
    with open(ann_path, 'w') as f:
        json.dump(textrecog_ann, f, indent=4)

if __name__ == '__main__':
    img_dir = '/home/diskhkme/Dev/PNID/dataset/text_dataset_test/synthetic'
    xml_dir = img_dir
    out_dir = '/home/diskhkme/Dev/PNID/dataset/text_dataset_test/synthetic/out'
    scale = 1.0
    target_filename = 'AugText_00000.png'

    do_text_split(img_dir, xml_dir, target_filename, out_dir, scale)