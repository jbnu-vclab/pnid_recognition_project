import argparse
import os.path
import yaml
from pnid_recognition_project.common.xml_data import XMLData
from pnid_recognition_project.inference.inference_engine.inference_engine import InferenceEngine
from pnid_recognition_project.inference.parse_options import parse_options

def do_inference():
    options = parse_options()

    with open(options['dataset_option_path']) as f:
        dataset_options = yaml.load(f, Loader=yaml.FullLoader)
        if not dataset_options['params']:
            assert False, "wrong dataset option file!"

    # prepare engine (load model & checkpoint)
    pnid_inference = InferenceEngine()
    pnid_inference.load_model(options['mmrotate_config_path'], options['mmrotate_checkpoint_path'])
    pnid_inference.set_dataset_option(dataset_options['params']['patch_size'],
                                      dataset_options['params']['patch_gap'],
                                      dataset_options['params']['img_scale'])

    # prepare target images to inference
    target_img_paths = []
    for file in os.listdir(options['img_dir']):
        if options['img_files'] is None or len(options['img_files']) == 0:
            target_img_paths.append(os.path.join(options['img_dir'], file))
        else:
            if file.split(".")[0] in options['img_files']:
                target_img_paths.append(os.path.join(options['img_dir'], file))

    # run inference
    for img_path in target_img_paths:
        inference_result = pnid_inference.inference_image(img_path, options['params']['merge_iou_th'])

        xml_data = XMLData().from_inference_result(inference_result,
                                                   scale=dataset_options['params']['img_scale'],
                                                   score_th=options['params']['score_th'])
        if options['params']["quantize_degree"]:
            xml_data.quantize_symbol_degree(options['params']["quantize_degree"])

        filename = os.path.basename(img_path).split(".")[0]
        outpath = os.path.join(options['save_dir'], filename + ".xml")
        xml_data.write_xml(outpath)


if __name__ == '__main__':
    do_inference()