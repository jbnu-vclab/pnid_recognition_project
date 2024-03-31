from common.xml_data import FourpointXMLData

def get_dota_txt_from_xml_data(xml_data) -> str:
    assert type(xml_data) is FourpointXMLData, "only support dota convert from four point xml data"
    difficulty = 0

    buffer = ""
    for symbol_object in xml_data.symbol_object_list:
        category = symbol_object.get_class_name()

        buffer += (f'{symbol_object.raw_points[0].x} {symbol_object.raw_points[0].y} '
                f'{symbol_object.raw_points[1].x} {symbol_object.raw_points[1].y} '
                f'{symbol_object.raw_points[2].x} {symbol_object.raw_points[2].y} '
                f'{symbol_object.raw_points[3].x} {symbol_object.raw_points[3].y} '
                f'{category} {difficulty}\n')

    return buffer

def convert_xml_to_dota_file(in_xml_path, out_dota_path):
    xml_data = FourpointXMLData()
    xml_data.load_xml_from_file(in_xml_path)

    buffer = get_dota_txt_from_xml_data(xml_data)
    with open(out_dota_path, "w") as f:
        f.write(buffer)


if __name__ == '__main__':
    in_xml = "D:/VClab/도면인식/Data/230228_Data/도면이미지/sample/26071-200-M6-052-00001.xml"

    convert_xml_to_dota_file(in_xml, './output_dota.txt')
