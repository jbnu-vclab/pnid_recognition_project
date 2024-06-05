import sys
sys.path.append('../..')

import os
from pnid_recognition_project.training.text_recog_train.mmocr_train_wrapper import train, get_mmocr_parser
from pnid_recognition_project.training.text_recog_train.parse_options import parse_options

def text_recog_train():
    train_options = parse_options()

    parser = get_mmocr_parser()
    args = parser.parse_args()

    train(train_options, args)

if __name__ == '__main__':
    text_recog_train()