import argparse
import os
import shutil

import yaml

def get_parser(name='DOTA Dataset Generation') -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('options', type=str)

    return parser

def parse_options():
    parser = get_parser()
    args = parser.parse_args()

    if args.options is None:
        assert False, "options file is missing!"

    with open(args.options) as f:
        options = yaml.load(f, Loader=yaml.FullLoader)
        if not options['dota_dataset_generation']:
            assert False, "wrong option file type!"

    dataset_options = options['dota_dataset_generation']
    if not os.path.exists(dataset_options['img_dir']):
        assert False, f"img dir not exist! {dataset_options['img_dir']}"
    if not os.path.exists(dataset_options['data_dir']):
        assert False, f"data dir not exist! {dataset_options['data_dir']}"

    return dataset_options


if __name__ == '__main__':
    dataset_options = parse_options()
    print(dataset_options)