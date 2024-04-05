import sys
sys.path.append('../..')

import os
import os.path as osp
import shutil

from training.dota_dataset_generation.options import parse_args
from training.dota_dataset_generation.img_split_wrapper import call_img_split, convert_args
from training.xml_dota_converter.convert_xml_to_dota_txt import convert_xml_to_dota_txt
from global_settings.validation_test_split import val_drawings, test_drawings

phase = ['train', 'test', 'val']

def convert_xml(args, temp_dir):
    # 0) if convert_xml = True, first convert xml to dota txt in save_dir
    if args.convert_from_xml:
        dota_dir = osp.join(temp_dir,'dota')
        os.mkdir(dota_dir)
        convert_xml_to_dota_txt(args.data_dir, dota_dir)
    else: # else, data dir should be dota dir
        files = os.listdir(args.data_dir)
        txt_files = [f for f in files if osp.splitext(f)[1].find('txt') != -1]
        assert len(txt_files) > 0, "no dota files in data-dir"
        dota_dir = args.data_dir

    return dota_dir

def copy_files_to_tmp_dir(filenames, source_dir, dest_dir):
    dota_files = [f for f in os.listdir(source_dir) if osp.splitext(f)[0] in filenames]
    for dota_file in dota_files:
        source_path = os.path.join(source_dir, dota_file)
        target_path = os.path.join(dest_dir, dota_file)
        shutil.copyfile(source_path, target_path)


def generate_tmp_dir_files(args, source_dir, temp_dir, type):
    # 1) generate tmp dir and copy dota txt
    tmp_dirs = {}
    for p in phase:
        parent_dir = osp.join(temp_dir,p)
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)

        tmp_dirs[p] = osp.join(parent_dir, type)
        os.mkdir(tmp_dirs[p])

        if p == "test":
            copy_files_to_tmp_dir(test_drawings, source_dir, tmp_dirs[p])
        elif p == "val":
            copy_files_to_tmp_dir(val_drawings, source_dir, tmp_dirs[p])
        else:
            train_drawings = [osp.splitext(f)[0] for f in os.listdir(source_dir) if osp.splitext(f)[0] not in test_drawings and osp.splitext(f)[0] not in val_drawings]
            copy_files_to_tmp_dir(train_drawings, source_dir, tmp_dirs[p])

    return tmp_dirs


def generate_dota_dataset():
    import warnings
    warnings.filterwarnings('ignore')

    args = parse_args()

    # check required and existing dirs
    if osp.exists(args.save_dir):
        shutil.rmtree(args.save_dir)

    os.mkdir(args.save_dir)
    # temp/[train,test,val]/img/ (=tmp_img_dirs), temp/[train,test,val]/ann/ (=tmp_dota_dirs), temp/dota(optional for data-dir is dota dir)
    temp_dir = osp.join(args.save_dir, "temp")
    os.mkdir(temp_dir)

    # 0) if convert_xml = True, first convert xml to dota txt
    if not args.silent:
        print("Converting XML to DOTA txt...")
    dota_dir = convert_xml(args, temp_dir)

    # 1) generate [train,test,val] subdir and copy files
    if not args.silent:
        print("Copying temp files...")
    tmp_dota_dirs = generate_tmp_dir_files(args, source_dir=dota_dir, temp_dir=temp_dir, type="ann")
    tmp_img_dirs = generate_tmp_dir_files(args, source_dir=args.img_dir, temp_dir=temp_dir, type="img")

    # 3) call_img_split
    for p in tmp_dota_dirs:
        save_dir = osp.join(args.save_dir, p)
        if not osp.exists(save_dir):
            os.mkdir(save_dir)

        call_arg = convert_args(args,tmp_img_dirs[p],tmp_dota_dirs[p],save_dir)
        call_img_split(call_arg)

    # 4) (optional) remove tmp dir
    if args.remove_tmp_files:
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    generate_dota_dataset()
