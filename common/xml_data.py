from common.symbol_object import SymbolObject, Vector2

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

class ImageMetadata:
    def __init__(self, filename, width, height, depth):
        self.filename = filename
        self.width = width
        self.height = height
        self.depth = depth

class XMLData:
    def __init__(self):
        self.image_metadata = None
        self.symbol_object_list = []
        self.error_list = []

    def getErrorInfo(self):
        return self.error_list

    def to_dota_str(self):
        str = ""
        for symbol_object in self.symbol_object_list:
            str += symbol_object.to_dota_str() + "\n"

        return str


    def __repr__(self):
        return "file: {}, num symbols: {}".format(self.filepath, len(self.symbol_object_list))


class FourpointXMLData(XMLData):
    def __init__(self):
        super().__init__()
        self.symbol_object_list = []

    def load_xml_from_file(self, filepath):
        self.filepath = filepath
        tree = parse(filepath)
        root = tree.getroot()

        try:
            filename = root.findtext("filename")
            width = int(root.find("size").findtext("width"))
            height = int(root.find("size").findtext("height"))
            depth = int(root.find("size").findtext("depth"))
            self.image_metadata = ImageMetadata(filename, width, height, depth)
        except:
            print("no img file metadata")

        for i, obj in enumerate(root.iter("symbol_object")):
            bndbox = obj.find("bndbox")
            try:
                x1 = int(bndbox.findtext("x1"))
                y1 = int(bndbox.findtext("y1"))
                x2 = int(bndbox.findtext("x2"))
                y2 = int(bndbox.findtext("y2"))
                x3 = int(bndbox.findtext("x3"))
                y3 = int(bndbox.findtext("y3"))
                x4 = int(bndbox.findtext("x4"))
                y4 = int(bndbox.findtext("y4"))

                if not self.check_range(x1, y1, x2, y2, x3, y3, x4, y4):
                    raise Exception('out of range')

                type = obj.findtext('type')
                cls = obj.findtext('class')
                degree = float(obj.findtext('degree'))
                flip = True if obj.findtext('flip') == "y" else False

                self.symbol_object_list.append(SymbolObject.from_fourpoint(type,cls,x1,y1,x2,y2,x3,y3,x4,y4,degree,flip))

            except Exception as e:
                self.error_list.append(
                    {
                        'index': i,
                        'obj_info': ET.tostring(obj, encoding='unicode'),
                        'error_message': str(e)
                    }
                )

    def check_range(self, x1, y1, x2, y2, x3, y3, x4, y4):
        if self.image_metadata:
            width = self.image_metadata.width
            height = self.image_metadata.height

            if 0 <= x1 < width and 0 <= x2 < width and 0 <= x3 < width and 0 <= x4 < width and \
                0 <= y1 < height and 0 <= y2 < height and 0 <= y3 < height and 0 <= y4 < height:
                return True
            return False
        else:
            return True

class TwopointXMLData(XMLData):
    def __init__(self):
        super().__init__()

    def load_xml_from_file(self, filepath):
        self.filepath = filepath
        tree = parse(filepath)
        root = tree.getroot()

        try:
            filename = root.findtext("filename")
            width = int(root.find("size").findtext("width"))
            height = int(root.find("size").findtext("height"))
            depth = int(root.find("size").findtext("depth"))
            self.image_metadata = ImageMetadata(filename, width, height, depth)
        except:
            print("no img file metadata")

        for i, obj in enumerate(root.iter("symbol_object")):
            bndbox = obj.find("bndbox")
            try:
                x1 = int(bndbox.findtext("xmin"))
                y1 = int(bndbox.findtext("ymin"))
                x2 = int(bndbox.findtext("xmax"))
                y2 = int(bndbox.findtext("ymax"))

                min_point = Vector2(x1, y1)
                max_point = Vector2(x2, y2)

                if not self.check_range(min_point, max_point):
                    raise Exception('min is greater than max')

                type = obj.findtext('type')
                cls = obj.findtext('class')
                degree = float(obj.findtext('degree'))
                flip = True if obj.findtext('flip') == "y" else False
                is_large = True if obj.findtext('isLarge') == "y" else False

                self.symbol_object_list.append(SymbolObject.from_twopoint(type,cls,min_point,max_point,degree,flip,is_large))

            except Exception as e:
                self.error_list.append(
                    {
                        'index': i,
                        'obj_info': ET.tostring(obj, encoding='unicode'),
                        'error_message': str(e)
                    }
                )

    def check_range(self, min_point, max_point):
        if min_point.x <= max_point.x and min_point.y <= max_point.y:
            return True
        return False


if __name__ == "__main__":
    fourpoint_sample_path = "G:/VCLab_NAS/Project/도면인식/Data/230228_Data/도면이미지/sample/26071-200-M6-052-00001.xml"
    xml_data = FourpointXMLData()
    xml_data.load_xml_from_file(fourpoint_sample_path)
    print(xml_data)
    # for symbol_object in xml_data.symbol_object_list:
    #     print(symbol_object)
    print(xml_data.to_dota_str())

    twopoint_sample_path = "G:/VCLab_NAS/Project/도면인식/Experiment/230318_2차년도실험/_2차년도_최종결과/26071-200-M6-052-00001_GT.xml"
    xml_data2 = TwopointXMLData()
    xml_data2.load_xml_from_file(twopoint_sample_path)
    print(xml_data2)
    # for symbol_object in xml_data2.symbol_object_list:
    #     print(symbol_object)
    print(xml_data.to_dota_str())
