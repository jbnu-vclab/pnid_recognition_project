import torch
import cv2
import copy
from mmocr.apis import MMOCRInferencer
import matplotlib.pyplot as plt

from pnid_recognition_project.common.image_util import get_symbol_cropped_image

class TextRecogEngine:
    def __init__(self):
        self.model = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.img_scale = None

    def load_model(self, config_path, checkpoint_path):
        self.model = MMOCRInferencer(rec=config_path, rec_weights=checkpoint_path)
        self.config_path = config_path
        self.checkpoint_path = checkpoint_path


    def set_dataset_option(self, img_scale):
        self.img_scale = img_scale

    def recognize_texts_in_pnid(self, pnid_img_path, xml_data):
        if not self.model:
            print("Model is not loaded!")
            return

        # TODO: image scale handling
        img = cv2.imread(pnid_img_path)
        ret_xml = copy.deepcopy(xml_data)

        corr = 0
        total = 0
        incorr = []

        for i, symbol_object in enumerate(ret_xml.symbol_object_list):
            if symbol_object.is_text:
                crop_img = get_symbol_cropped_image(img, symbol_object)
                if crop_img is not None:
                    recognized_text = self.model(crop_img)
                    if ret_xml.symbol_object_list[i].cls == recognized_text['predictions'][0]['rec_texts'][0]:
                        corr += 1
                    else:
                        incorr.append((ret_xml.symbol_object_list[i].cls, recognized_text['predictions'][0]['rec_texts'][0]))

                    # TODO: consider handle remaining results and scores
                    ret_xml.symbol_object_list[i].cls = recognized_text['predictions'][0]['rec_texts'][0]

                    total += 1

        print(f"WEM: {corr}/{total} = {corr/total:.4f}")
        print(incorr)


        return ret_xml

