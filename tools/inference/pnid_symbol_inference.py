import argparse
import os.path
import yaml
from pnid_recognition_project.common.xml_data import XMLData
from pnid_recognition_project.inference.inference_engine.symbol_inference_engine import SymbolInferenceEngine
from pnid_recognition_project.inference.parse_options import parse_options

def inference_small_symbol(options, engine, scale, img_path):
    inference_result = engine.inference_image(img_path, options['params']['merge_iou_th'])

    xml_data = XMLData().from_inference_result(inference_result,
                                               scale=scale,
                                               score_th=options['params']['score_th'])
    if options['params']["quantize_degree"]:
        xml_data.quantize_symbol_degree(options['params']["quantize_degree"])

    return xml_data

def do_inference():
    options, small_symbol_options, text_recog_options = parse_options()

    # prepare target images to inference
    target_img_paths = []
    for file in os.listdir(options['img_dir']):
        if options['img_files'] is None or len(options['img_files']) == 0:
            target_img_paths.append(os.path.join(options['img_dir'], file))
        else:
            if file.split(".")[0] in options['img_files']:
                target_img_paths.append(os.path.join(options['img_dir'], file))

    # prepare inference engines
    if small_symbol_options:
        with open(small_symbol_options['dataset_option_path']) as f:
            symbol_dataset_options = yaml.load(f, Loader=yaml.FullLoader)
            symbol_dataset_options = symbol_dataset_options['dota_dataset_generation']
            if not symbol_dataset_options['params']:
                assert False, "wrong dataset option file!"
        symbol_inference_engine = SymbolInferenceEngine()
        symbol_inference_engine.load_model(small_symbol_options['mmrotate_config_path'],
                                           small_symbol_options['mmrotate_checkpoint_path'])
        symbol_inference_engine.set_dataset_option(symbol_dataset_options['params']['patch_size'],
                                          symbol_dataset_options['params']['patch_gap'],
                                          symbol_dataset_options['params']['img_scale'])

    # run inference
    for img_path in target_img_paths:
        if small_symbol_options:
            result_xml = inference_small_symbol(small_symbol_options, symbol_inference_engine, symbol_dataset_options['params']['img_scale'], img_path)

        filename = os.path.basename(img_path).split(".")[0]
        outpath = os.path.join(options['save_dir'], filename + ".xml")
        result_xml.write_xml(outpath)


if __name__ == '__main__':
    do_inference()