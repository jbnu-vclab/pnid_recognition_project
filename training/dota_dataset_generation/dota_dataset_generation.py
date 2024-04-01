from common.xml_data import FourpointXMLData

def convert_xml_to_dota_file(in_xml_path, out_dota_path):
    xml_data = FourpointXMLData()
    xml_data.load_xml_from_file(in_xml_path)

    with open(out_dota_path, "w") as f:
        f.write(xml_data.to_dota_str())


if __name__ == '__main__':
    in_xml = "G:/VCLab_NAS/Project/도면인식/Data/230228_Data/도면이미지/sample/26071-200-M6-052-00001.xml"

    convert_xml_to_dota_file(in_xml, './output_dota.txt')
