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

    if not os.path.exists(options['dataset_option_path']):
        assert False, f"no dataset option data in {options['dataset_option_path']} !"

    if not os.path.exists(options['save_dir']):
        os.mkdir(options['save_dir'])

    return options


if __name__ == '__main__':
    inference_options = parse_options()
    print(inference_options)