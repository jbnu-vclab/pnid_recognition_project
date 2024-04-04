import argparse
import os.path as osp
import os
import time
from functools import partial, reduce
from multiprocessing import Pool, Manager
import training.dota_dataset_generation.external.img_split as imgsplit
import common.util as util
from tqdm import tqdm

def convert_args(args, img_dir, ann_dir, save_dir):
    parser = argparse.ArgumentParser(description='Splitting images')
    imgsplit.add_parser(parser)
    call_arg = parser.parse_args()

    call_arg.nproc = 10
    call_arg.sizes = [args.size]
    call_arg.gaps = [args.gap]
    call_arg.rates = [1.0]
    call_arg.img_rate_thr = args.img_rate_thr
    call_arg.iof_thr = args.iof_thr
    call_arg.no_padding = False
    call_arg.padding_value = [104, 116, 124]
    call_arg.save_ext = ".png"
    call_arg.save_dir = save_dir

    call_arg.img_dirs = [img_dir]
    call_arg.ann_dirs = [ann_dir]
    call_arg.save_dir = save_dir

    return call_arg

def call_img_split(args):
    if args.ann_dirs is None:
        args.ann_dirs = [None for _ in range(len(args.img_dirs))]
    padding_value = args.padding_value[0] \
        if len(args.padding_value) == 1 else args.padding_value
    sizes, gaps = [], []
    for rate in args.rates:
        sizes += [int(size / rate) for size in args.sizes]
        gaps += [int(gap / rate) for gap in args.gaps]
    save_imgs = osp.join(args.save_dir, 'images')
    save_files = osp.join(args.save_dir, 'annfiles')

    # remove files and recreate
    if os.path.exists(save_imgs):
        util.remove_files_in_dir(save_imgs)
    else:
        os.makedirs(save_imgs)

    if os.path.exists(save_files):
        util.remove_files_in_dir(save_files)
    else:
        os.makedirs(save_files)
    logger = imgsplit.setup_logger(args.save_dir)

    print('Loading original data!!!')
    infos, img_dirs = [], []
    for img_dir, ann_dir in zip(args.img_dirs, args.ann_dirs):
        _infos = imgsplit.load_dota(img_dir=img_dir, ann_dir=ann_dir, nproc=args.nproc)
        _img_dirs = [img_dir for _ in range(len(_infos))]
        infos.extend(_infos)
        img_dirs.extend(_img_dirs)

    print('Start splitting images!!!')
    start = time.time()
    manager = Manager()
    worker = partial(
        imgsplit.single_split,
        sizes=sizes,
        gaps=gaps,
        img_rate_thr=args.img_rate_thr,
        iof_thr=args.iof_thr,
        no_padding=args.no_padding,
        padding_value=padding_value,
        save_dir=save_imgs,
        anno_dir=save_files,
        img_ext=args.save_ext,
        lock=manager.Lock(),
        prog=manager.Value('i', 0),
        total=len(infos),
        logger=logger)

    if args.nproc > 1:
        pool = Pool(args.nproc)
        patch_infos = pool.map(worker, zip(infos, img_dirs))
        pool.close()
    else:
        patch_infos = list(map(worker, zip(infos, img_dirs)))

    patch_infos = reduce(lambda x, y: x + y, patch_infos)
    stop = time.time()
    print(f'Finish splitting images in {int(stop - start)} second!!!')
    print(f'Total images number: {len(patch_infos)}')