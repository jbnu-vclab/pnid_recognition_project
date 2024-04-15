import argparse

def parse_args(base_path):
    parser = argparse.ArgumentParser()
    parser.add_argument('--device',
                        default='cuda:0',
                        help='Device used for inference')

    parser.add_argument('image', help='Image file')
    parser.add_argument('--gt_directory', default=base_path + 'GTxml')

    parser.add_argument('--config',
                        default=base_path +
                        'Config/roi_trans_r50_fpn_1x_dota_le90.py',
                        help='Small Symbol Config file')
    parser.add_argument('--checkpoint',
                        default=base_path + 'Checkpoint/latest.pth',
                        help='Small Symbol Checkpoint file')
    # parser.add_argument('--config_big',
    #                     default=base_path +
    #                     'Config/roi_trans_r50_fpn_1x_dota_le135_big.py',
    #                     help='big Symbol Config file')
    # parser.add_argument('--checkpoint_big',
    #                     default=base_path + 'Checkpoint/latest_big.pth',
    #                     help='big Symbol Checkpoint file')
    # parser.add_argument('--checkpoint_text',
    #                     default=base_path +
    #                     'Checkpoint/best_accuracy_text.pth',
    #                     help='Text Checkpoint file')

    # parser.add_argument('--class_type_map',
    #                     default=base_path + 'SymbolClass_Type.txt',
    #                     help='class_type_file path')

    parser.add_argument('--merge_before_xml_directory',
                        default=base_path + 'text_merge_before'),
    parser.add_argument('--cropped_image_directory',
                        default=base_path + 'cropped_image')

    args = parser.parse_args()

    return args