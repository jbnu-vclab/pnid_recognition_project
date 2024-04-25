import argparse
import os
import shutil

import yaml

def get_parser(name='PNID Eval') -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('options', type=str)

    return parser

def parse_options():
    parser = get_parser()
    args = parser.parse_args()

    with open(args.options) as f:
        options = yaml.load(f, Loader=yaml.FullLoader)
        if not options['pnid_eval']:
            assert False, "wrong option file type!"
        options = options['pnid_eval']

        save_dir = os.path.dirname(options['save_path'])
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

    return options


if __name__ == '__main__':
    eval_options = parse_options()
    print(eval_options)