import sys
sys.path.append('../..')

import difflib
import math
from pnid_recognition_project.common.symbol_object import SymbolObject
from pnid_recognition_project.common.vector2 import Vector2
from pnid_recognition_project.global_settings.symbol_class_def import get_symbol_class_def

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
        self.tree = None
        self.root = None
        self.scale = None

        self.fuzz_matching_cache = {}

    def to_dota_str(self):
        str = ""
        for symbol_object in self.symbol_object_list:
            str += symbol_object.to_dota_str() + "\n"

        return str

    def quantize_symbol_degree(self, quantize_degree):
        for symbol_object in self.symbol_object_list:
            symbol_object.degree = round((round(symbol_object.degree) / quantize_degree)) * quantize_degree

    def _is_sane(self, symbol_object, fuzz_thr=0.8):
        classes, _ = get_symbol_class_def()

        # check class definition
        if not symbol_object.is_text:
            if symbol_object.cls not in classes:
                if symbol_object.cls in self.fuzz_matching_cache:
                    symbol_object.cls = self.fuzz_matching_cache[symbol_object.cls]

                # try fuzzy matching
                matches = list(filter(lambda c: difflib.SequenceMatcher(None, c, symbol_object.cls).ratio() > fuzz_thr, classes))
                if len(matches) > 0:
                    r = sorted(matches, key=lambda c: difflib.SequenceMatcher(None, c, symbol_object.cls).ratio(), reverse=True)
                    self.fuzz_matching_cache[symbol_object.cls] = r[0]
                    symbol_object.cls = self.fuzz_matching_cache[symbol_object.cls]
                else:
                    return False  # failed matching

        # TODO: range check is involved to image scaling
        # # check range
        # if self.image_metadata:
        #     if self._check_range(symbol_object):
        #         return True
        #     else:
        #         return False

        return True

    def apply_scale(self, scale):
        for symbol_object in self.symbol_object_list:
            symbol_object.apply_scale(scale)

    @staticmethod
    def is_twopoint_format(filepath):
        tree = parse(filepath)
        root = tree.getroot()

        for sym in root.findall("symbol_object"):
            bndbox = sym.find("bndbox")
            xmin = bndbox.find('xmin')
            if xmin is not None:
                return True

            x1 = bndbox.find('x1')
            if x1 is None:
                assert False, "xml format check failed!"
            else:
                return False

    def from_xml(self, filepath, sanitize=True):
        if XMLData.is_twopoint_format(filepath):
            return self.from_twopoint_xml(filepath, sanitize)
        else:
            return self.from_fourpoint_xml(filepath, sanitize)


    def from_fourpoint_xml(self, filepath, sanitize=True):
        self.filepath = filepath
        self.tree = parse(filepath)
        self.root = self.tree.getroot()

        try:
            filename = self.root.findtext("filename")
            width = int(self.root.find("size").findtext("width"))
            height = int(self.root.find("size").findtext("height"))
            depth = int(self.root.find("size").findtext("depth"))
            self.image_metadata = ImageMetadata(filename, width, height, depth)
        except:
            #print("no img file metadata")
            pass

        for i, obj in enumerate(self.root.iter("symbol_object")):
            bndbox = obj.find("bndbox")

            x1 = int(bndbox.findtext("x1"))
            y1 = int(bndbox.findtext("y1"))
            x2 = int(bndbox.findtext("x2"))
            y2 = int(bndbox.findtext("y2"))
            x3 = int(bndbox.findtext("x3"))
            y3 = int(bndbox.findtext("y3"))
            x4 = int(bndbox.findtext("x4"))
            y4 = int(bndbox.findtext("y4"))

            type = obj.findtext('type')
            cls = obj.findtext('class')
            degree = float(obj.findtext('degree'))
            flip = True if obj.findtext('flip') == "y" else False

            symbol_object = SymbolObject.from_fourpoint(type, cls, x1, y1, x2, y2, x3, y3, x4, y4, degree, flip)
            if sanitize:
                if self._is_sane(symbol_object):
                    self.symbol_object_list.append(symbol_object)
                else:
                    self.root.remove(obj)
                    print('class does not exist in symbol_class_def in global_settings')
            else:
                self.symbol_object_list.append(symbol_object)

        return self

    def from_twopoint_xml(self, filepath, sanitize=True):
        self.filepath = filepath
        self.tree = parse(filepath)
        self.root = self.tree.getroot()

        try:
            filename = self.root.findtext("filename")
            width = int(self.root.find("size").findtext("width"))
            height = int(self.root.find("size").findtext("height"))
            depth = int(self.root.find("size").findtext("depth"))
            self.image_metadata = ImageMetadata(filename, width, height, depth)
        except:
            # print("no img file metadata")
            pass

        for i, obj in enumerate(self.root.iter("symbol_object")):
            bndbox = obj.find("bndbox")

            x1 = int(bndbox.findtext("xmin"))
            y1 = int(bndbox.findtext("ymin"))
            x2 = int(bndbox.findtext("xmax"))
            y2 = int(bndbox.findtext("ymax"))

            min_point = Vector2(x1, y1)
            max_point = Vector2(x2, y2)

            type = obj.findtext('type')
            cls = obj.findtext('class')
            degree = float(obj.findtext('degree'))
            flip = True if obj.findtext('flip') == "y" else False
            is_large = True if obj.findtext('isLarge') == "y" else False

            symbol_object = SymbolObject.from_twopoint(type, cls, min_point, max_point, degree, flip, is_large)
            if sanitize:
                if self._is_sane(symbol_object):
                    self.symbol_object_list.append(symbol_object)
                else:
                    self.root.remove(obj)
                    print('class does not exist in symbol_class_def in global_settings')
            else:
                self.symbol_object_list.append(symbol_object)

        return self

    def from_inference_result(self, result, scale, score_th):
        classes, class_type_def = get_symbol_class_def()

        for i, class_list in enumerate(result):
            for symbol in class_list:
                class_name = classes[i]
                score = symbol[5]
                if score > score_th:
                    xmin = int((float(symbol[0]) - float(symbol[2]) * 0.5)/scale)
                    ymin = int((float(symbol[1]) - float(symbol[3]) * 0.5)/scale)
                    xmax = int((float(symbol[0]) + float(symbol[2]) * 0.5)/scale)
                    ymax = int((float(symbol[1]) + float(symbol[3]) * 0.5)/scale)
                    degree = float(symbol[4]) * (180 / math.pi) * -1

                    if class_name == 'text':
                        type_name = 'text'
                    else:
                        type_name = class_type_def[class_name]

                    symbol_object = SymbolObject.from_twopoint(type_name, class_name, Vector2(xmin, ymin),
                                                               Vector2(xmax, ymax), degree)
                    self.symbol_object_list.append(symbol_object)

        return self

    def _check_range(self, symbol_object):
        if self.image_metadata:
            width = self.image_metadata.width
            height = self.image_metadata.height

            if 0 <= symbol_object.min_point.x < width and 0 <= symbol_object.max_point.x < width and \
                    0 <= symbol_object.min_point.y < height and 0 <= symbol_object.max_point.y < height:
                return True
            return False
        else:
            return True

    def write_xml(self, filepath):
        self._construct_xml_tree()
        self.tree.write(filepath)

    def get_xml_byte(self):
        self._construct_xml_tree()
        return ET.tostring(self.root, encoding='utf-8', method='xml')

    def _construct_xml_tree(self):
        self.root = ET.Element("annotation")

        for symbol_object in self.symbol_object_list:
            elementSymbol = ET.Element("symbol_object")
            elementType = ET.Element("type")
            elementType.text = symbol_object.type
            elementClass = ET.Element("class")
            elementClass.text = symbol_object.cls

            elementBndbox = ET.Element("bndbox")
            elementXmin = ET.Element("xmin")
            elementXmin.text = str(symbol_object.min_point.x)
            elementYmin = ET.Element("ymin")
            elementYmin.text = str(symbol_object.min_point.y)
            elementXmax = ET.Element("xmax")
            elementXmax.text = str(symbol_object.max_point.x)
            elementYmax = ET.Element("ymax")
            elementYmax.text = str(symbol_object.max_point.y)

            elementBndbox.append(elementXmin)
            elementBndbox.append(elementYmin)
            elementBndbox.append(elementXmax)
            elementBndbox.append(elementYmax)

            elementIsLarge = ET.Element("isLarge")
            elementIsLarge.text = symbol_object.is_large

            elementDegree = ET.Element("degree")
            elementDegree.text = str(symbol_object.degree)

            elementFlip = ET.Element("flip")
            elementFlip.text = "n"

            elementEtc = ET.Element("etc")

            elementSymbol.append(elementType)
            elementSymbol.append(elementClass)
            elementSymbol.append(elementBndbox)
            elementSymbol.append(elementIsLarge)
            elementSymbol.append(elementDegree)
            elementSymbol.append(elementFlip)
            elementSymbol.append(elementEtc)

            self.root.append(elementSymbol)

        self._indent(self.root)
        self.tree = ET.ElementTree(self.root)

    def _indent(self, elem, level=0):  # 자료 출처 https://goo.gl/J8VoDK
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def __repr__(self):
        return "file: {}, num symbols: {}".format(self.filepath, len(self.symbol_object_list))


if __name__ == "__main__":
    fourpoint_sample_path = "../../tests/data/xml/fourpoint/Test1_Fourpoint.xml"
    xml_data = XMLData().from_fourpoint_xml(fourpoint_sample_path)
    print(xml_data)
    # for symbol_object in xml_data.symbol_object_list:
    #     print(symbol_object)
    print(xml_data.to_dota_str())

    twopoint_sample_path = "../../tests/data/xml/twopoint/Test1_Twopoint.xml"
    xml_data2 = XMLData().from_twopoint_xml(twopoint_sample_path)
    print(xml_data2)
    # for symbol_object in xml_data2.symbol_object_list:
    #     print(symbol_object)
    print(xml_data.to_dota_str())
