import sys
sys.path.append('../../..')

import io
import yaml
import numpy as np
import cv2

from flask import Flask, request, Response

from pnid_recognition_project.inference.inference_engine.inference_engine import InferenceEngine
from pnid_recognition_project.common.xml_data import XMLData

app = Flask(__name__)

# --- Reuse inference configuration
with open('pnid_inference_server_config.yaml') as f:
    options = yaml.load(f, Loader=yaml.FullLoader)
    options = options['pnid_inference']

with open(options['dataset_option_path']) as f:
    dataset_options = yaml.load(f, Loader=yaml.FullLoader)
    if not dataset_options['params']:
        assert False, "wrong dataset option file!"

pnid_inference_engine = InferenceEngine()
pnid_inference_engine.load_model(options['mmrotate_config_path'], options['mmrotate_checkpoint_path'])
pnid_inference_engine.set_dataset_option(dataset_options['params']['patch_size'],
                                  dataset_options['params']['patch_gap'],
                                  dataset_options['params']['img_scale'])

def get_prediction(image_bytes):
    image = np.fromstring(image_bytes, dtype = np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    outputs = pnid_inference_engine.inference_image_from_tensor(image, options['params']['merge_iou_th'])
    xml_data = XMLData().from_inference_result(outputs,
                                               scale=dataset_options['params']['img_scale'],
                                               score_th=options['params']['score_th'])

    if options['params']['quantize_degree']:
        xml_data.quantize_symbol_degree(options['params']['quantize_degree'])

    return xml_data

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        xml_data = get_prediction(image_bytes=img_bytes)
        xml_byte = xml_data.get_xml_byte()

        response = Response(xml_byte, content_type='application/xml')

        return response

if __name__ == '__main__':
    app.run()