import argparse
import os.path

import torch
import mmcv
import cv2
import yaml
from mmcv.runner import load_checkpoint
from mmrotate.models import build_detector
from mmrotate.apis import inference_detector_by_patches
from common.xml_data import XMLData

class PNIDInference:
    def __init__(self):
        self.model = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.patch_size = None
        self.patch_gap = None
        self.img_scale = None
        self.iou_th = None

    def load_model(self, config_path, checkpoint_path):
        self.config_path = config_path
        self.checkpoint_path = checkpoint_path

        config = mmcv.Config.fromfile(config_path)
        model = build_detector(config.model)
        checkpoint = load_checkpoint(model, checkpoint_path, map_location=self.device)

        model.CLASSES = checkpoint['meta']['CLASSES']
        model.cfg = config

        model.to(self.device)
        model.eval()

        self.model = model

    def set_dataset_option(self, dataset_option_path):
        if not os.path.exists(dataset_option_path):
            print("wrong dataset option path!")
            return

        with open(dataset_option_path) as f:
            options = yaml.load(f, Loader=yaml.FullLoader)
            if not options['params']:
                print("wrong dataset option file!")
                return

            self.patch_size = options['params']['patch_size']
            self.patch_gap = options['params']['patch_gap']
            self.img_scale = options['params']['img_scale']

    def inference_image(self, img_path, merge_iou_th):
        if not self.model:
            print("Model is not loaded!")
            return
        if not self.img_scale:
            print("dataset option is not set!")
            return

        src = cv2.imread(img_path)
        dst = cv2.resize(src, dsize=(0, 0), fx=self.img_scale, fy=self.img_scale, interpolation=cv2.INTER_LINEAR)
        result = inference_detector_by_patches(self.model, dst, [self.patch_size],
                                      [self.patch_gap], [1.0], merge_iou_th)
        return result

def get_parser(name='PNID Inference') -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('options', type=str)

    return parser

def do_inference():
    parser = get_parser()
    args = parser.parse_args()

    with open(args.options) as f:
        options = yaml.load(f, Loader=yaml.FullLoader)
        if not options['pnid_inference']:
            assert False, "wrong option file type!"
        options = options['pnid_inference']

        if not os.path.exists(options['save_dir']):
            os.mkdir(options['save_dir'])

    pnid_inference = PNIDInference()
    pnid_inference.load_model(options['mmrotate_config_path'], options['mmrotate_checkpoint_path'])
    pnid_inference.set_dataset_option(options['dataset_option_path'])
    img_scale = pnid_inference.img_scale

    target_img_paths = []
    for file in os.listdir(options['img_dir']):
        if options['img_files'] is None or len(options['img_files']) == 0:
            target_img_paths.append(os.path.join(options['img_dir'], file))
        else:
            if file.split(".")[0] in options['img_files']:
                target_img_paths.append(os.path.join(options['img_dir'], file))

    for img_path in target_img_paths:
        inference_result = pnid_inference.inference_image(img_path, options['params']['merge_iou_th'])

        xml_data = XMLData()
        xml_data.from_inference_result(inference_result, scale=img_scale, score_th=options['params']['score_th'])

        filename = os.path.basename(img_path).split(".")[0]
        outpath = os.path.join(options['save_dir'], filename + ".xml")
        xml_data.write_xml(outpath)


if __name__ == '__main__':
    do_inference()