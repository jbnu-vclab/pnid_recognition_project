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
from pnid_recognition_project.common.image_util import get_symbol_cropped_image

def segment_text_images(img_path, xml_path, out_dir, ann, scale, ignore_newline):
    img = cv2.imread(img_path)
    base_filename = osp.basename(xml_path).replace(".xml", "")

    # TODO: change xml reading to use from_xml fct
    if XMLData.is_twopoint_format(xml_path):
        xml_data = XMLData().from_twopoint_xml(xml_path)
    else:
        xml_data = XMLData().from_fourpoint_xml(xml_path)

    img_index = 0
    for symbol_object in xml_data.symbol_object_list:
        if not symbol_object.is_text:
            continue

        if ignore_newline and '\n' in symbol_object.cls:
            continue

        crop_img = get_symbol_cropped_image(img, symbol_object)

        if scale != 1: # if scaled, simple scale the cropped img
            crop_img = cv2.resize(crop_img, dsize=(0,0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        # write cropped image
        out_img_filename = f'{base_filename}_{img_index}.jpg'
        out_img_path = osp.join(out_dir, out_img_filename)
        cv2.imwrite(out_img_path, crop_img)

        # https://github.com/open-mmlab/mmocr/blob/main/mmocr/datasets/recog_text_dataset.py
        text_instance = [{"text": symbol_object.cls}]
        ann.append({'instances': text_instance, 'img_path': out_img_filename})

        img_index += 1

def do_text_split(img_dir, xml_dir, phase, target_filenames, out_dir, scale, ignore_newline):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    textrecog_ann = {}
    textrecog_ann['metainfo'] = {"dataset_type": "TextRecogDataset", "task_name": "textrecog"}
    textrecog_ann['data_list'] = []

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

        segment_text_images(img_path, xml_path, out_dir, textrecog_ann['data_list'], scale, ignore_newline)

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