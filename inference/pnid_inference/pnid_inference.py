import argparse
import os.path
import yaml
from common.xml_data import XMLData
from inference_engine import InferenceEngine

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

    pnid_inference = InferenceEngine()
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