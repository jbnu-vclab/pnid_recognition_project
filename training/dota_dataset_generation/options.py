import argparse
import os
import json

def args_to_str(args):
    d = args.__dict__
    txt = ''
    for k in d.keys():
        txt += f'{k}: {d[k]}\n'
    return txt.strip('\n')

def get_parser(name='DOTA Dataset Generation') -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument('--base-json', type=str)
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--data-dir', type=str)
    parser.add_argument('--save-dir', type=str)
    parser.add_argument('--size', default=800, type=int)
    parser.add_argument('--gap', default=500, type=int)
    parser.add_argument('--img-rate-thr', default=0.6, type=float)
    parser.add_argument('--iof-thr', default=0.7, type=float)
    parser.add_argument('--convert-from-xml', default=True, type=bool)
    parser.add_argument('--remove-tmp-files', default=True, type=bool)
    parser.add_argument('--silent', default=True, type=bool)

    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()

    if args.base_json is not None:
        with open(args.base_json, 'r') as f:
            prior_config = json.load(f)

        for action in parser._actions:
            if action.dest not in prior_config or \
                    not hasattr(action, 'default'):
                continue
            action.default = prior_config[action.dest]
        args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
        if args.use_split_def:
            os.mkdir(os.path.join(args.save_dir,'train'))
            os.mkdir(os.path.join(args.save_dir,'test'))
            os.mkdir(os.path.join(args.save_dir,'val'))

    with open(os.path.join(args.save_dir,'args.txt'), 'w+') as file:
        file.write(args_to_str(args))

    return args


if __name__ == '__main__':
    # python .\training\dota_dataset_generation\options.py --data-dir=./ --xml-dir=./ --save-dir=./ --size 500
    # python .\training\dota_dataset_generation\options.py --base-json=./dataset_generation.json
    args = parse_args()
    print(args.size)