import os
import sys
import yaml
from pnid_recognition_project.eval.eval_engine.eval_engine import EvalEngine
from pnid_recognition_project.eval.parse_options import parse_options

def find_corresponding_gt_path(filename, gt_dir):
    for gt_file in os.listdir(gt_dir):
        if filename in gt_file:
            gt_path = os.path.join(gt_dir, gt_file)

    return gt_path

def do_eval():
    options = parse_options()

    eval_engine = EvalEngine()

    for dt_file in os.listdir(options['dt_dir']):
        filename = dt_file.split(".")[0]
        dt_path = os.path.join(options['dt_dir'], dt_file)
        if not options['dt_files'] or len(options['dt_files']) != 0: # files specified
            if filename not in options['dt_files']:
                continue

        gt_path = find_corresponding_gt_path(filename, options['gt_dir'])
        eval_engine.add_gt_dt_pair(gt_path, dt_path)

    result = ""
    if isinstance(options['params']['iou_th'], list):
        for iou_th in options['params']['iou_th']:
            result += eval_engine.evaluate(iou_th)
    else:
        result = eval_engine.evaluate(options['params']['iou_th'])

    with open(options['save_path'], 'w') as f:
        f.write(result)


if __name__ == "__main__":
    do_eval()
