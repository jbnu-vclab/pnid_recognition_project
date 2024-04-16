import sys
sys.path.append('../..')

import os
import os.path as osp
import shutil
import yaml
import cv2

from training.dota_dataset_generation.parse_options import parse_options
from training.dota_dataset_generation.img_split_wrapper import call_img_split, ImgSplitArgs
from training.dota_dataset_generation.xml_dota_converter.convert_xml_to_dota_txt import convert_xml_to_dota_txt
from training.dota_dataset_generation.sanitize_xml.sanitize_xml import convert_xmls_to_sanitized_xmls
from global_settings.validation_test_split import val_drawings, test_drawings

phase = ['train', 'test', 'val']

def copy_files_to_tmp_dir(filenames, source_dir, dest_dir):
    dota_files = [f for f in os.listdir(source_dir) if osp.splitext(f)[0] in filenames]
    for dota_file in dota_files:
        source_path = os.path.join(source_dir, dota_file)
        target_path = os.path.join(dest_dir, dota_file)
        shutil.copyfile(source_path, target_path)


def copy_scaled_img_files_to_tmp_dir(filenames, source_dir, dest_dir, scale):
    img_files = [f for f in os.listdir(source_dir) if osp.splitext(f)[0] in filenames]
    for img_file in img_files:
        source_path = os.path.join(source_dir, img_file)
        target_path = os.path.join(dest_dir, img_file)

        src = cv2.imread(source_path, cv2.IMREAD_COLOR)
        dst = cv2.resize(src, dsize=(0,0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(target_path, dst)


def copy_dota_files(source_dir, dest_dir):
    # 1) generate tmp dir and copy dota txt
    for p in phase:
        if p == "test":
            copy_files_to_tmp_dir(test_drawings, source_dir, dest_dir[p])
        elif p == "val":
            copy_files_to_tmp_dir(val_drawings, source_dir, dest_dir[p])
        else:
            train_drawings = [osp.splitext(f)[0] for f in os.listdir(source_dir) if osp.splitext(f)[0] not in test_drawings and osp.splitext(f)[0] not in val_drawings]
            copy_files_to_tmp_dir(train_drawings, source_dir, dest_dir[p])

def copy_img_files(source_dir, dest_dir, scale):
    # 1) generate tmp dir and copy dota txt
    for p in phase:
        if p == "test":
            copy_files_to_tmp_dir(test_drawings, source_dir, dest_dir[p])
        elif p == "val":
            copy_files_to_tmp_dir(val_drawings, source_dir, dest_dir[p])
        else:
            train_drawings = [osp.splitext(f)[0] for f in os.listdir(source_dir) if osp.splitext(f)[0] not in test_drawings and osp.splitext(f)[0] not in val_drawings]
            if scale != 1.0:
                copy_scaled_img_files_to_tmp_dir(train_drawings, source_dir, dest_dir[p], scale)
            else:
                copy_files_to_tmp_dir(train_drawings, source_dir, dest_dir[p])

def generate_dota_dataset():
    import warnings
    warnings.filterwarnings('ignore')

    dataset_options = parse_options()

    # 0) generate required dirs
    save_dir = dataset_options['save_dir']
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    data_dir = dataset_options['data_dir']
    temp_dir = osp.join(dataset_options['save_dir'], 'temp')
    dota_dir = osp.join(temp_dir, 'dota')

    os.mkdir(save_dir)
    os.mkdir(temp_dir)
    os.mkdir(dota_dir)

    img_phase_temp_dirs = {}
    ann_phase_temp_dirs = {}
    phase_save_dirs = {}
    for p in phase:
        parent_dir = osp.join(temp_dir, p)
        img_phase_temp_dirs[p] = osp.join(parent_dir, "img")
        ann_phase_temp_dirs[p] = osp.join(parent_dir, "ann")
        phase_save_dirs[p] = osp.join(save_dir, p)
        os.mkdir(parent_dir)
        os.mkdir(img_phase_temp_dirs[p])
        os.mkdir(ann_phase_temp_dirs[p])
        os.mkdir(os.path.join(save_dir, p))


    # 1) if true, sanitize first
    if dataset_options['preprocess']['sanitize_xml']:
        convert_xmls_to_sanitized_xmls(dataset_options['data_dir'], dataset_options['preprocess']['sanitized_xml_out_dir'])
        data_dir = dataset_options['preprocess']['sanitized_xml_out_dir']

    # 2) convert xml files to dota txt files (for each img)
    print("Converting XML to DOTA txt...")
    convert_xml_to_dota_txt(data_dir, dota_dir, dataset_options['params']['img_scale'])

    # 2) generate [train,test,val] subdir and copy files
    print("Copying temp files...")
    copy_dota_files(source_dir=dota_dir, dest_dir=ann_phase_temp_dirs)
    copy_img_files(source_dir=dataset_options['img_dir'], dest_dir=img_phase_temp_dirs, scale=dataset_options['params']['img_scale'])

    # 3) call_img_split
    for p in ann_phase_temp_dirs:
        print(f"Splitting {p} ...")
        call_arg = ImgSplitArgs(dataset_options,img_phase_temp_dirs[p],ann_phase_temp_dirs[p],phase_save_dirs[p])
        call_img_split(call_arg)

    # 4) dump yaml for reference
    with open(os.path.join(dataset_options['save_dir'],'dataset_gen_options.yaml'), 'w') as file:
        yaml.dump(dataset_options, file, default_flow_style=False)

    # 5) (optional) remove tmp dir
    if dataset_options['remove_tmp_files']:
        shutil.rmtree(temp_dir)




if __name__ == '__main__':
    generate_dota_dataset()
