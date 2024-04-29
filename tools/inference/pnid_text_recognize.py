import argparse
import os.path
import yaml
from pnid_recognition_project.common.xml_data import XMLData
from pnid_recognition_project.inference.inference_engine.text_recog_inference_engine import TextRecogEngine
from pnid_recognition_project.inference.parse_options import parse_options

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
    if text_recog_options:
        with open(text_recog_options['dataset_option_path']) as f:
            text_dataset_options = yaml.load(f, Loader=yaml.FullLoader)
            if not text_dataset_options['params']:
                assert False, "wrong dataset option file!"

        text_recog_engine = TextRecogEngine()
        text_recog_engine.load_model(text_recog_options['mmocr_config_path'],
                                     text_recog_options['mmocr_checkpoint_path'])
        text_recog_engine.set_dataset_option(text_dataset_options['params']['img_scale'])


    # run inference
    for img_path in target_img_paths:
        if text_recog_options:
            if text_recog_options['reference_xml_dir']:
                reference_xml = os.path.join(text_recog_options['reference_xml_dir'], os.path.splitext(os.path.basename(img_path))[0] + ".xml")
                if not os.path.exists(reference_xml):
                    assert False, f"Can't find corresponding xml to {img_path} in {text_recog_options['reference_xml_dir']}"

                ref_xml_data = XMLData().from_xml(reference_xml, sanitize=False)
            # else: # TODO: connect with symbol detect result
            #     ref_xml_data = result_xml

            result_xml = text_recog_engine.recognize_texts_in_pnid(img_path, ref_xml_data)

        filename = os.path.basename(img_path).split(".")[0]
        outpath = os.path.join(options['save_dir'], filename + ".xml")
        result_xml.write_xml(outpath)


if __name__ == '__main__':
    do_inference()