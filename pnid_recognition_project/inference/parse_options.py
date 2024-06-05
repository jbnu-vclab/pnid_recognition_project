import argparse
import os
import shutil

import yaml

def get_parser(name='PNID Inference') -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('options', type=str)

    return parser

def parse_options():
    parser = get_parser()
    args = parser.parse_args()


    with open(args.options) as f:
        options = yaml.load(f, Loader=yaml.FullLoader)
        if not options['pnid_inference']:
            assert False, "wrong option file type!"

    options = options['pnid_inference']
    small_symbol_options = options['small_symbol_inference'] if 'small_symbol_inference' in options else None
    text_recog_options = options['text_recog_inference'] if 'text_recog_inference' in options else None

    if small_symbol_options:
        if not os.path.exists(small_symbol_options['mmrotate_config_path']):
            assert False, f"no dataset option data in {small_symbol_options['mmrotate_config_path']} !"
        if not os.path.exists(small_symbol_options['mmrotate_checkpoint_path']):
            assert False, f"no dataset option data in {small_symbol_options['mmrotate_checkpoint_path']} !"

    if text_recog_options:
        if not os.path.exists(text_recog_options['mmocr_config_path']):
            assert False, f"no dataset option data in {text_recog_options['mmocr_config_path']} !"
        if not os.path.exists(text_recog_options['mmocr_checkpoint_path']):
            assert False, f"no dataset option data in {text_recog_options['mmocr_checkpoint_path']} !"

    if not os.path.exists(options['save_dir']):
        os.mkdir(options['save_dir'])

    return options, small_symbol_options, text_recog_options


if __name__ == '__main__':
    inference_options = parse_options()
    print(inference_options)