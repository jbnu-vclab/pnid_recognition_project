import sys
sys.path.append('../../..')

import os
import os.path as osp

from common.xml_data import XMLData

def convert_xml_to_dota_single(xml_path, dota_path, scale):
    xml_data = XMLData()
    xml_data.from_fourpoint_xml(xml_path)

    if scale != 1.0:
        xml_data.apply_scale(scale)

    with open(dota_path, "w") as f:
        f.write(xml_data.to_dota_str())

    return True

def convert_xml_to_dota_txt(in_dir, out_dir, scale):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    xml_files = [f for f in os.listdir(in_dir) if 'xml' in osp.splitext(f)[1]]
    for xml_file in xml_files:
        out_name = os.path.basename(xml_file).replace('xml', 'txt')
        out_path = os.path.join(out_dir, out_name)

        in_path = os.path.join(in_dir, xml_file)
        convert_xml_to_dota_single(in_path, out_path, scale)

if __name__ == '__main__':
    convert_xml_to_dota_txt('../../test/2nd_source/xml', '../../test/2nd_source/dota')
