import torch
import mmcv
import cv2
import yaml
import os
from mmcv.runner import load_checkpoint
from mmrotate.models import build_detector
from mmrotate.apis import inference_detector_by_patches


class SymbolInferenceEngine:
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

    def set_dataset_option(self, patch_size, patch_gap, img_scale):
        self.patch_size = patch_size
        self.patch_gap = patch_gap
        self.img_scale = img_scale

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

    def inference_image_from_tensor(self, img_tensor, merge_iou_th):
        result = inference_detector_by_patches(self.model, img_tensor, [self.patch_size],
                                               [self.patch_gap], [1.0], merge_iou_th)
        return result
