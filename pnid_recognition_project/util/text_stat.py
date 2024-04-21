import os
import re
from collections import Counter

from pnid_recognition_project.common.xml_data import XMLData
from pnid_recognition_project.common.fileutil import dict_to_csv
from tqdm import tqdm

def get_special_characters(xml_dir, is_twopoint_xml):
    special_chars = set([])
    for file in tqdm(os.listdir(xml_dir)):
        xml_path = os.path.join(xml_dir, file)

        xml_data = XMLData()
        if is_twopoint_xml:
            xml_data.from_twopoint_xml(xml_path, sanitize=True)
        else:
            xml_data.from_fourpoint_xml(xml_path, sanitize=True)

        text_strs = [s.cls for s in xml_data.symbol_object_list if s.is_text]
        regex_pattern = r'[^a-zA-Z0-9]'
        text_special_chars = [set(re.findall(regex_pattern, s)) for s in text_strs if len(re.findall(regex_pattern, s)) != 0]
        text_special_chars = [x for xs in text_special_chars for x in xs]  # flatten

        text_special_chars = set(text_special_chars)
        special_chars.update(text_special_chars)

    print(special_chars)


def count_char_occurence(xml_dir, is_twopoint_xml):
    counter = Counter()
    for file in tqdm(os.listdir(xml_dir)):
        xml_path = os.path.join(xml_dir, file)

        xml_data = XMLData()
        if is_twopoint_xml:
            xml_data.from_twopoint_xml(xml_path, sanitize=True)
        else:
            xml_data.from_fourpoint_xml(xml_path, sanitize=True)

        text_strs = [s.cls for s in xml_data.symbol_object_list if s.is_text]
        text_flat_str = "".join(text_strs)

        counter.update(text_flat_str)

    chars = sorted(list(counter.keys()))
    occur = {}
    for ch in chars:
        if ch == "" or ch == " ":
            continue
            
        occur[ch] = counter[ch]

    return occur


def text_stat(xml_dir, is_twopoint_xml, separate_multiline=True, strip=True):
    text_dict = {}

    for file in tqdm(os.listdir(xml_dir)):
        xml_path = os.path.join(xml_dir, file)

        xml_data = XMLData()
        if is_twopoint_xml:
            xml_data.from_twopoint_xml(xml_path, sanitize=True)
        else:
            xml_data.from_fourpoint_xml(xml_path, sanitize=True)

        if separate_multiline:
            text_strs = [s.cls.split("\n") for s in xml_data.symbol_object_list if s.is_text]
            text_strs = [x for xs in text_strs for x in xs] # flatten
        else:
            text_strs = [s.cls for s in xml_data.symbol_object_list if s.is_text]

        if strip:
            text_strs = [s.strip() for s in text_strs]

        text_strs_set = set(text_strs)

        for text_str in text_strs_set:
            if text_str in text_dict:
                text_dict[text_str] += text_strs.count(text_str)
            else:
                text_dict[text_str] = text_strs.count(text_str)

    return text_dict # key: unique texts, value: occurence



if __name__ == "__main__":
    xml_dir = '/home/diskhkme/Dev/PNID/dataset/2nd_source/XML_Sanitized'
    # text_dict = text_stat(xml_dir, is_twopoint_xml=False, separate_multiline=True, strip=True)
    # print(text_dict)

    #special_chars = get_special_characters(xml_dir, is_twopoint_xml=False)

    occur = count_char_occurence(xml_dir, is_twopoint_xml=False)
    print(occur)

    occur_csv = dict_to_csv(occur)
    with open('./char_occur.csv', 'w') as f:
        f.write(occur_csv)