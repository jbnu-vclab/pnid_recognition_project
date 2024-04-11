import sys
sys.path.append('../..')

import os
from mmrotate_train_wrapper import train, get_mmrotate_parser

def add_custom_argument(parser):
    parser.add_argument('--data-root', type=str)
    parser.add_argument('--silent', type=bool, default=False)
    parser.add_argument('--use_wandb', type=bool, default=False)

def pnid_train():
    parser = get_mmrotate_parser()
    add_custom_argument(parser)

    args = parser.parse_args()

    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)

    train(args)

if __name__ == '__main__':
    pnid_train()