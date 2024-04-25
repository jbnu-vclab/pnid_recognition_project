import sys
sys.path.append('../..')

import os
<<<<<<< HEAD:training/pnid_train/pnid_train.py
from training.pnid_train.mmrotate_train_wrapper import train, get_mmrotate_parser
from training.pnid_train.parse_options import parse_options
=======
from pnid_recognition_project.training.pnid_train.mmrotate_train_wrapper import train, get_mmrotate_parser
from pnid_recognition_project.training.pnid_train.parse_options import parse_options
>>>>>>> 3fe7db3a80befda51c6d451c28ae87196f4e1e57:tools/training/pnid_train.py

def pnid_train():
    train_options = parse_options()

    parser = get_mmrotate_parser()
    args = parser.parse_args()

    train(train_options, args)

if __name__ == '__main__':
    pnid_train()