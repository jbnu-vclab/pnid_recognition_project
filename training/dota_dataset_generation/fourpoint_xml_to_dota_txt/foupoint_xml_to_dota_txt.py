# import os
# import cv2
# from tqdm import tqdm
# import xml.etree.ElementTree as ET
# from xml.etree.ElementTree import parse
#
#
#
# def read_symbol_txt(filename, include_text_as_class):
#     class_index = 0
#     class_name_to_index_dict = {}
#     class_index_to_name_dict = {}
#
#     with open(filename, 'r') as f:
#         for l in f.readlines():
#             _, class_name = l.rstrip().split("|")
#             class_name_to_index_dict[class_name] = class_index
#             class_index_to_name_dict[class_index] = class_name
#
#             class_index += 1
#
#     if include_text_as_class == True:
#         class_name_to_index_dict["text"] = len(class_name_to_index_dict.items())
#
#     return class_name_to_index_dict
#
#
# def generate_dota_data(xml_list, drawing_dir, out_dir, prefix):
#     '''분할하지 않은 정보를 리스트로 저장
#     '''
#     if os.path.exists(os.path.join(out_dir, prefix)) == False:
#         os.mkdir(os.path.join(out_dir, prefix))
#
#     if os.path.exists(os.path.join(out_dir, prefix, 'annfiles')) == False:
#         os.mkdir(os.path.join(out_dir, prefix, 'annfiles'))
#
#     if os.path.exists(os.path.join(out_dir, prefix, 'images')) == False:
#         os.mkdir(os.path.join(out_dir, prefix, 'images'))
#
#     out_file_dir = os.path.join(out_dir, prefix, 'annfiles')
#     out_img_dir = os.path.join(out_dir, prefix, 'images')
#
#     for xmlPath in tqdm(xml_list):
#         fname, ext = os.path.splitext(xmlPath)
#         if ext.lower() != ".xml":
#             continue
#
#         xmlReader = xml_reader(xmlPath)
#         img_filename, width, height, depth, object_list = xmlReader.getInfo()
#         img_file_path = os.path.join(drawing_dir, img_filename)
#
#         out_filename = img_filename.replace('.jpg', '.txt')
#         out_file_path = os.path.join(out_file_dir, out_filename)
#         out_img_path = os.path.join(out_img_dir, img_filename)
#
#         img = cv2.imread(img_file_path)
#         cv2.imwrite(out_img_path, img)
#
#         with open(out_file_path, 'w') as f:
#             for box in object_list:
#                 category = 'text' if box[0] == 'text' else box[1]
#                 difficulty = 0
#                 f.write(
#                     f'{box[2]} {box[3]} {box[4]} {box[5]} {box[6]} {box[7]} {box[8]} {box[9]} {category} {difficulty}\n')
#
#
# base_dir = r"E:\PNID_Data\2023_0228"  # * Root 경로
# drawing_dir = base_dir + r"\Drawing"  # * 원본 이미지 폴더
# xml_dir = base_dir + r"\XML"  # * 원본 XML 폴더
# out_dir = base_dir + r"\pnid"  # * 출력 폴더
#
# val_drawings = ['26071-200-M6-052-00025', '26071-200-M6-052-00039', '26071-200-M6-052-00046', '26071-200-M6-052-00073',
#                 '26071-200-M6-052-00091', '26071-200-M6-052-00097', '26071-200-M6-052-00543', '26071-200-M6-052-00904',
#                 '26071-200-M6-052-02002', '26071-200-M6-062-00013', '26071-200-M6-063-00020', '26071-203-M6-060-00010',
#                 '26071-203-M6-064-00010', '26071-203-M6-064-00012', '26071-203-M6-079-00011', '26071-203-M6-160-00211',
#                 '26071-203-M6-167-00009', '26071-203-M6-167-00202', '26071-203-M6-315-00002', '26071-203-M6-315-00006',
#                 '26071-203-M6-315-00012', '26071-203-M6-320-00015', '26071-203-M6-320-00020', '26071-203-M6-320-00049',
#                 '26071-203-M6-320-00051', '26071-203-M6-321-00202', '26071-203-M6-321-00502', '26071-203-M6-321-00517',
#                 '26071-203-M6-321-00522', '26071-203-M6-321-00608', '26071-203-M6-323-30024', '26071-203-M6-325-00005',
#                 '26071-203-M6-325-00009', '26071-203-M6-331-00002', '26071-203-M6-331-00025', '26071-203-M6-331-00035',
#                 '26071-203-M6-337-00018', '26071-203-M6-337-00035', '26071-203-M6-337-00042', '26071-300-M6-053-00006',
#                 '26071-300-M6-053-00009', '26071-300-M6-053-00017', '26071-300-M6-053-00023', '26071-300-M6-053-00271',
#                 '26071-300-M6-053-00307', '26071-450-M6-082-00010', '26071-450-M6-082-00231', '26071-500-M6-059-00018',
#                 '26071-500-M6-059-00056', '26071-500-M6-059-00108', '26071-500-M6-059-00235', '26071-550-M6-084-00001',
#                 '26071-550-M6-084-00015', '26071-550-M6-084-00263', '26071-600-M6-065-00028', '26071-600-M6-065-00042',
#                 '26071-600-M6-065-00260', '26071-625-M6-169-00231', '26071-675-M6-068-00025', '26071-675-M6-068-00031',
#                 '26071-675-M6-068-00043', '26071-700-M6-054-00051', '26071-700-M6-054-00055', '26071-700-M6-054-00261',
#                 '26071-750-M6-085-00221', '26071-750-M6-085-00305', '26071-750-M6-085-00316']
# test_drawings = ['26071-200-M6-052-00001', '26071-200-M6-052-00002', '26071-200-M6-052-00003', '26071-200-M6-052-00080',
#                  '26071-200-M6-052-00090', '26071-200-M6-052-00093', '26071-200-M6-052-00150', '26071-200-M6-052-00539',
#                  '26071-200-M6-052-00540', '26071-200-M6-052-00544', '26071-200-M6-052-00552', '26071-200-M6-062-00276',
#                  '26071-200-M6-062-00277', '26071-200-M6-063-00010', '26071-203-M6-060-00001', '26071-203-M6-060-00006',
#                  '26071-203-M6-064-00271', '26071-203-M6-079-00001', '26071-203-M6-160-00291', '26071-203-M6-320-00008',
#                  '26071-203-M6-320-00042', '26071-203-M6-320-00044', '26071-203-M6-320-00060', '26071-203-M6-320-00061',
#                  '26071-203-M6-321-00225', '26071-203-M6-321-00604', '26071-203-M6-325-00012', '26071-203-M6-325-00013',
#                  '26071-203-M6-332-00001', '26071-203-M6-332-00008', '26071-203-M6-333-00010', '26071-203-M6-337-00007',
#                  '26071-203-M6-337-00031', '26071-300-M6-053-00008', '26071-300-M6-053-00010', '26071-300-M6-053-00012',
#                  '26071-300-M6-053-00309', '26071-450-M6-082-00009', '26071-450-M6-082-00031', '26071-450-M6-082-00221',
#                  '26071-500-M6-059-00011', '26071-500-M6-059-00013', '26071-500-M6-059-00017', '26071-500-M6-059-00040',
#                  '26071-500-M6-059-00044', '26071-500-M6-059-00071', '26071-500-M6-059-00116', '26071-500-M6-059-00248',
#                  '26071-550-M6-084-00026', '26071-550-M6-084-00248', '26071-600-M6-065-00021', '26071-600-M6-065-00037',
#                  '26071-600-M6-065-00231', '26071-600-M6-065-00259', '26071-600-M6-066-00002', '26071-600-M6-066-00003',
#                  '26071-600-M6-066-00012', '26071-675-M6-068-00034', '26071-675-M6-068-00041', '26071-675-M6-068-10002',
#                  '26071-700-M6-054-00013', '26071-700-M6-054-00036', '26071-700-M6-054-00246', '26071-750-M6-085-00007',
#                  '26071-750-M6-085-00012', '26071-750-M6-085-00286', '26071-750-M6-085-00309']
# ignore_drawing = []
# train_drawings = [x.split(".")[0] for x in os.listdir(xml_dir)
#                   if x.split(".")[0] not in test_drawings and
#                   x.split(".")[0] not in val_drawings and
#                   x.split(".")[0] not in ignore_drawing]
#
# symbol_txt_path = base_dir + "\SymbolClass_Class.txt"
#
# include_text_as_class = True  # Text를 별도의 클래스로 포함할 것인지 {"text"}
#
# symbol_dict = read_symbol_txt(symbol_txt_path, include_text_as_class)
#
# train_xmls = [os.path.join(xml_dir, f"{x}.xml") for x in train_drawings]
# val_xmls = [os.path.join(xml_dir, f"{x}.xml") for x in val_drawings]
# test_xmls = [os.path.join(xml_dir, f"{x}.xml") for x in test_drawings]
#
# if __name__ == '__main__':
#     generate_dota_data(train_xmls, drawing_dir, out_dir, 'train')
#     generate_dota_data(val_xmls, drawing_dir, out_dir, 'val')
#     generate_dota_data(test_xmls, drawing_dir, out_dir, 'test')