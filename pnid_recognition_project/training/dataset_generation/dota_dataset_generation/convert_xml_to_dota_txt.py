import sys
sys.path.append('../../../..')

import os
import os.path as osp

from pnid_recognition_project.common.xml_data import XMLData

def write_dota_txt(source_xml_path, target_dota_path, scale):
    if XMLData.is_twopoint_format(source_xml_path):
        xml_data = XMLData().from_twopoint_xml(source_xml_path)
    else:
        xml_data = XMLData().from_fourpoint_xml(source_xml_path)

    if scale != 1.0:
        xml_data.apply_scale(scale)

    with open(target_dota_path, "w") as f:
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
        write_dota_txt(in_path, out_path, scale)

if __name__ == '__main__':
    convert_xml_to_dota_txt('../../test/2nd_source/xml', '../../test/2nd_source/dota')
