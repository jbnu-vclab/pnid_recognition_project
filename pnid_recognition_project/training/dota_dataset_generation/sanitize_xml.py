import sys
sys.path.append('../../..')

import os
import os.path as osp

from pnid_recognition_project.common.xml_data import XMLData

def write_sanitized_xml(source_xml_path, target_xml_path):
    xml_data = XMLData()
    xml_data.from_fourpoint_xml(source_xml_path, sanitize=True)

    xml_data.tree.write(target_xml_path)
    return True

def convert_xmls_to_sanitized_xmls(in_dir, out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    xml_files = [f for f in os.listdir(in_dir) if 'xml' in osp.splitext(f)[1]]
    for xml_file in xml_files:
        out_path = os.path.join(out_dir, xml_file)
        in_path = os.path.join(in_dir, xml_file)
        write_sanitized_xml(in_path, out_path)

if __name__ == '__main__':
    convert_xmls_to_sanitized_xmls('../test/test_data/2nd_source_full/XML', '../test/test_data/2nd_source_full/XML_Sanitized')
