import sys
sys.path.append('../..')

import os
from mmrotate_train_wrapper import train, get_mmrotate_parser
from parse_options import parse_options

def pnid_train():
    train_options = parse_options()

    parser = get_mmrotate_parser()
    args = parser.parse_args()

    train(train_options, args)

if __name__ == '__main__':
    pnid_train()