import argparse
import os
import shutil

import yaml

def get_parser(name='PNID Train') -> argparse.ArgumentParser:
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
        if not options['pnid_train']:
            assert False, "wrong option file type!"

    train_options = options['pnid_train']
    if not os.path.exists(train_options['dataset_option_path']):
        assert False, f"dataset option file not exist! {train_options['dataset_option_path']}"
    if not os.path.exists(train_options['data_root']):
        assert False, f"data root not exist! {train_options['data_root']}"

    return train_options


if __name__ == '__main__':
    train_options = parse_options()
    print(train_options)