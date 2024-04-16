import os
import sys
import yaml
from eval_engine import EvalEngine

def do_eval():
    with open(sys.argv[1]) as f:
        options = yaml.load(f, Loader=yaml.FullLoader)
        if not options['pnid_eval']:
            assert False, "wrong option file type!"

        options = options['pnid_eval']

    eval_engine = EvalEngine()

    for dt_file in os.listdir(options['dt_path']):
        filename = dt_file.split(".")[0]
        dt_path = os.path.join(options['dt_path'], dt_file)
        for gt_file in os.listdir(options['gt_path']):
            if filename in gt_file:
                gt_path = os.path.join(options['gt_path'], gt_file)
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
