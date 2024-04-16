import sys
sys.path.append('../..')

import os
from tqdm import tqdm
from common.xml_data import XMLData

class EvalEngine:
    def __init__(self):
        self.xml_paths = [] # (gt_path, dt_path) pair tuple

    def add_gt_dt_pair(self, gt_path, dt_path):
        self.xml_paths.append((gt_path, dt_path))

    def get_short_name(self, pair):
        return os.path.basename(pair).split(".")[0]

    def check_file_exist(self, path):
        return os.path.exists(path)

    def to_str(self, precision, recall, false_detect, iou_th):
        result_str = ""
        mean = {}
        mean['tp'] = 0
        mean['dt'] = 0
        mean['gt'] = 0

        result_str += f"[IoU Threshold: {iou_th}]\n"

        for pair in tqdm(self.xml_paths):
            diagram_name = self.get_short_name(pair[0])
            result_str += f"\n"
            result_str += f'test drawing: {diagram_name}----------------------------------\n'

            score = "precision"
            tp = precision[diagram_name]['total']['tp']
            dt = precision[diagram_name]['total']['dt']
            pr = tp / dt if dt != 0 else 0
            result_str += f"total {score}: {tp} / {dt} = {pr:.4f}\n"

            score = "recall"
            tp = recall[diagram_name]['total']['tp']
            gt = recall[diagram_name]['total']['gt']
            rc = tp / gt if gt != 0 else 0
            result_str += f"total {score}: {tp} / {gt} = {rc:.4f}\n"

            mean['tp'] += tp
            mean['dt'] += dt
            mean['gt'] += gt

            for cls in recall[diagram_name].keys():
                if 'gt' in recall[diagram_name][cls]: # cls is in GT
                    gt = recall[diagram_name][cls]['gt']
                    tp = recall[diagram_name][cls]['tp']
                    result_str += f"class {cls}: {tp} / {gt}\n"

            result_str += f"false detect: {len(false_detect[diagram_name])}\n"
            false_cls = set(false_detect[diagram_name])
            for cls in false_cls:
                count = false_detect[diagram_name].count(cls)
                result_str += f"    false detect {cls}({count})\n"


        mean['precision'] = mean['tp'] / mean['dt'] if mean['dt'] != 0 else 0
        mean['recall'] = mean['tp'] / mean['gt'] if mean['gt'] != 0 else 0
        average = (mean['precision'] + mean['recall']) / 2
        f1 = 2 * (mean['precision'] * mean['recall']) / (mean['precision'] + mean['recall'])

        result_str += f"(mean precision, mean recall, (p+r)/2, f-score) = ({mean['precision']:.4f}, {mean['recall']:.4f}, {average:.4f}, {f1:.4f}) \n\n"
        print(result_str)

        return result_str

    def cal_iou(self, gt_symbol, dt_symbol):
        """ IoU 계산 (바운딩 박스가 회전되어 있으므로 shapely.Polygon 사용)

        """
        try:
            gt_rect = gt_symbol.get_fourpoint_polygon()
            dt_rect = dt_symbol.get_fourpoint_polygon()
        except:
            pass

        iou = 0
        if gt_rect.intersects(dt_rect):
            intersection = gt_rect.intersection(dt_rect).area
            union = gt_rect.union(dt_rect).area
            iou = intersection / union
        return iou

    def evaluate(self, iou_th):
        if len(self.xml_paths) == 0:
            print("XML paths are not set!")
            return

        precision = {}
        recall = {}
        false_detect = {}
        for pair in tqdm(self.xml_paths):
            diagram_name =self.get_short_name(pair[0])
            precision[diagram_name] = {}
            precision[diagram_name]['total'] = {}
            precision[diagram_name]['total']['tp'] = 0
            precision[diagram_name]['total']['dt'] = 0
            recall[diagram_name] = {}
            recall[diagram_name]['total'] = {}
            recall[diagram_name]['total']['tp'] = 0
            recall[diagram_name]['total']['gt'] = 0
            false_detect[diagram_name] = []

            gt_path = pair[0]
            dt_path = pair[1]
            if not self.check_file_exist(gt_path):
                print(f'{gt_path} is skipped. (GT not exist)\n')
                continue
            if not self.check_file_exist(dt_path):
                print(f'{dt_path} is skipped. (DT not exist)\n')
                continue

            gt_xml_data = XMLData().from_fourpoint_xml(gt_path, False)
            dt_xml_data = XMLData().from_twopoint_xml(dt_path, False)

            # Counting tp, dt, gt for each classes
            tp = {}
            dt = {}
            gt = {}

            gt_matched = [False] * len(gt_xml_data.symbol_object_list)
            dt_matched = [False] * len(dt_xml_data.symbol_object_list)
            for gt_idx, gt_symbol in enumerate(gt_xml_data.symbol_object_list):
                for dt_idx, dt_symbol in enumerate(dt_xml_data.symbol_object_list):
                    if gt_matched[gt_idx] or dt_matched[dt_idx]:
                        continue

                    if gt_symbol.get_class_name() == dt_symbol.get_class_name():
                        cls = gt_symbol.get_class_name()
                        if cls not in tp:
                            tp[cls] = 0

                        iou = self.cal_iou(gt_symbol, dt_symbol)
                        if iou > iou_th:
                            tp[cls] += 1
                            gt_matched[gt_idx] = True
                            dt_matched[dt_idx] = True

            for dt_idx, dt_symbol in enumerate(dt_xml_data.symbol_object_list):
                cls = dt_symbol.get_class_name()
                if cls not in dt:
                    dt[cls] = 0
                dt[cls] += 1

            for gt_idx, gt_symbol in enumerate(gt_xml_data.symbol_object_list):
                cls = gt_symbol.get_class_name()
                if cls not in gt:
                    gt[cls] = 0
                gt[cls] += 1

            # Mapping precision
            for cls, cnt in tp.items():
                if cls not in precision[diagram_name]:
                    precision[diagram_name][cls] = {}
                precision[diagram_name][cls]['tp'] = cnt
                precision[diagram_name]['total']['tp'] += cnt
            for cls, cnt in dt.items():
                if cls not in precision[diagram_name]:
                    precision[diagram_name][cls] = {}
                precision[diagram_name][cls]['dt'] = cnt
                precision[diagram_name]['total']['dt'] += cnt
                if 'tp' not in precision[diagram_name][cls]:
                    precision[diagram_name][cls]['tp'] = 0

            # Mapping recall
            for cls, cnt in tp.items():
                if cls not in recall[diagram_name]:
                    recall[diagram_name][cls] = {}
                recall[diagram_name][cls]['tp'] = cnt
                recall[diagram_name]['total']['tp'] += cnt
            for cls, cnt in gt.items():
                if cls not in recall[diagram_name]:
                    recall[diagram_name][cls] = {}
                recall[diagram_name][cls]['gt'] = cnt
                recall[diagram_name]['total']['gt'] += cnt
                if 'tp' not in recall[diagram_name][cls]:
                    recall[diagram_name][cls]['tp'] = 0

            # Mapping false detection
            for ind, matched in enumerate(dt_matched):
                if matched == False:
                    cls = dt_xml_data.symbol_object_list[ind].get_class_name()
                    false_detect[diagram_name].append(cls)

        result = self.to_str(precision, recall, false_detect, iou_th)

        return result