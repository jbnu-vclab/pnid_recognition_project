import argparse
import torch
import mmcv
import cv2
from mmcv.runner import load_checkpoint
from mmrotate.models import build_detector
from mmrotate.apis import inference_detector_by_patches
from common.xml_data import XMLData

class PNIDInference:
    def __init__(self):
        self.model = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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

    def inference_image(self, img_path, patch_size, patch_step, patch_scale, iou_th):
        if not self.model:
            print("Model is not loaded")
            return

        src = cv2.imread(img_path)
        dst = cv2.resize(src, dsize=(0, 0), fx=patch_scale, fy=patch_scale, interpolation=cv2.INTER_LINEAR)
        result = inference_detector_by_patches(self.model, dst, [patch_size],
                                      [patch_step], [patch_scale], iou_th)
        return result



if __name__ == '__main__':
    img_path = "/home/diskhkme/Dev/PNID/dataset/test_img_123/26071-200-M6-052-00001.jpg"
    config_path =  "/home/diskhkme/Dev/PNID/train_test_half/roi_trans_r50_fpn_1x_dota_le90.py"
    checkpoint_path = "/home/diskhkme/Dev/PNID/train_test_half/epoch_1.pth"

    pnid_inference = PNIDInference()
    pnid_inference.load_model(config_path, checkpoint_path)
    inference_result = pnid_inference.inference_image(img_path, 800, 500, 0.5, 0.1)

    print(inference_result)

    xml_data = XMLData()
    xml_data.from_inference_result(inference_result, scale=0.5, score_th=0.1)
    xml_data.write_xml("/home/diskhkme/Dev/PNID/train_test_half/26071-200-M6-052-00001_DT.xml")