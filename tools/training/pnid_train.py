import sys
sys.path.append('../..')

import os
from pnid_recognition_project.training.pnid_train.mmrotate_train_wrapper import train, get_mmrotate_parser
from pnid_recognition_project.training.pnid_train.parse_options import parse_options

def pnid_train():
    train_options = parse_options()

    parser = get_mmrotate_parser()
    args = parser.parse_args()

    train(train_options, args)

if __name__ == '__main__':
    pnid_train()