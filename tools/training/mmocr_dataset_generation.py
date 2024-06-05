import random
import sys
sys.path.append('../..')

import os
import os.path as osp
import shutil
import yaml
import cv2

from pnid_recognition_project.training.dataset_generation.mmocr_dataset_generation.parse_options import parse_options
from pnid_recognition_project.training.dataset_generation.mmocr_dataset_generation.text_split import do_text_split
from pnid_recognition_project.training.dataset_generation.sanitize_xml import convert_xmls_to_sanitized_xmls
from pnid_recognition_project.global_settings.validation_test_split import val_drawings, test_drawings

# TODO: move logics to pnid_recognition_project/training/dataset_generation/mmocr_dataset_generation

phase = ['train', 'val', 'test']

def generate_mmocr_dataset():
    import warnings
    warnings.filterwarnings('ignore')

    dataset_options = parse_options()

    if dataset_options['params']['seed']:
        random.seed(dataset_options['params']['seed'])

    # 0) generate required dirs
    save_dir = dataset_options['save_dir']
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    os.mkdir(save_dir)

    data_dir = dataset_options['data_dir']
    img_dir =  dataset_options['img_dir']

    phase_save_dirs = {}
    for p in phase:
        phase_save_dirs[p] = os.path.join(save_dir, p)
        os.mkdir(phase_save_dirs[p])

    # 1) if true, sanitize first
    if dataset_options['preprocess']['sanitize_xml']:
        convert_xmls_to_sanitized_xmls(dataset_options['data_dir'], dataset_options['preprocess']['sanitized_xml_out_dir'])
        data_dir = dataset_options['preprocess']['sanitized_xml_out_dir']

    # 2) gather train/val/test filenames
    phase_filenames = {}
    if dataset_options['use_global_split']:
        for p in phase:
            if p == 'test':
                phase_filenames[p] = test_drawings
            elif p == 'val':
                phase_filenames[p] = val_drawings
            else:
                phase_filenames[p] = [osp.splitext(f)[0] for f in os.listdir(data_dir) if osp.splitext(f)[0] not in test_drawings and osp.splitext(f)[0] not in val_drawings]
    else:
        all_files = [osp.splitext(f)[0] for f in os.listdir(data_dir) if "xml" in osp.splitext(f)[1]]
        train_ratio = dataset_options['train_val_ratio'][0]
        train_count = int(len(all_files) * train_ratio)
        val_ratio = dataset_options['train_val_ratio'][1]
        val_count = int(len(all_files) * val_ratio)
        test_count = len(all_files) - train_count - val_count
        for p in phase:
            if p == 'train':
                phase_filenames[p] = random.sample(all_files, train_count)
            elif p == 'val':
                rem_files = [f for f in all_files if f not in phase_filenames['train']]
                phase_filenames[p] = random.sample(rem_files, val_count)
            elif p == 'test':
                phase_filenames[p] = [f for f in all_files if f not in phase_filenames['train'] and f not in phase_filenames['val']]

    # sort filenames for debugging easiness
    for p in phase:
        phase_filenames[p].sort()


    # 3) call do_text_split
    for p in phase:
    # p = 'val'
        do_text_split(img_dir, data_dir, p, phase_filenames[p], phase_save_dirs[p],
                      dataset_options['params']['img_scale'], dataset_options['params']['ignore_newline_char'])

    # 4) dump yaml for reference
    with open(os.path.join(dataset_options['save_dir'],'textrecog_dataset_gen_options.yaml'), 'w') as file:
        yaml.dump(dataset_options, file, default_flow_style=False)

if __name__ == '__main__':
    generate_mmocr_dataset()
