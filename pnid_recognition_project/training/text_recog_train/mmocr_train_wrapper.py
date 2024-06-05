import argparse
import logging
import os
import os.path as osp

from mmengine.config import Config, DictAction
from mmengine.logging import print_log
from mmengine.registry import RUNNERS
from mmengine.runner import Runner

def get_mmocr_parser():
    parser = argparse.ArgumentParser(description='Train a model')
    parser.add_argument('train_option', help='train option file path')
    parser.add_argument('--config', help='train config file path')
    parser.add_argument('--work-dir', help='The dir to save logs and models')
    parser.add_argument(
        '--resume', action='store_true', help='Whether to resume checkpoint.')
    parser.add_argument(
        '--amp',
        action='store_true',
        default=False,
        help='Enable automatic-mixed-precision training')
    parser.add_argument(
        '--auto-scale-lr',
        action='store_true',
        help='Whether to scale the learning rate automatically. It requires '
        '`auto_scale_lr` in config, and `base_batch_size` in `auto_scale_lr`')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='Override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    parser.add_argument(
        '--launcher',
        choices=['none', 'pytorch', 'slurm', 'mpi'],
        default='none',
        help='Job launcher')
    # When using PyTorch version >= 2.0.0, the `torch.distributed.launch`
    # will pass the `--local-rank` parameter to `tools/train.py` instead
    # of `--local_rank`.
    parser.add_argument('--local_rank', '--local-rank', type=int, default=0)

    return parser


def override_config(cfg, options):
    cfg.dictionary.dict_file = options['dict_path']
    cfg.model.decoder.dictionary.dict_file = options['dict_path']

    cfg.icdar2015_textrecog_data_root = options['data_root']
    cfg.icdar2015_textrecog_train.data_root = os.path.join(options['data_root'], 'train')
    cfg.icdar2015_textrecog_train.ann_file = 'ann_train.json'
    cfg.icdar2015_textrecog_val.data_root = os.path.join(options['data_root'], 'val')
    cfg.icdar2015_textrecog_val.ann_file = 'ann_val.json'
    cfg.icdar2015_textrecog_test.data_root = os.path.join(options['data_root'], 'test')
    cfg.icdar2015_textrecog_test.ann_file = 'ann_test.json'

    cfg.train_list = [cfg.icdar2015_textrecog_train]
    cfg.val_list = [cfg.icdar2015_textrecog_val]
    cfg.test_list = [cfg.icdar2015_textrecog_test]

    cfg.train_dataloader.dataset.datasets = cfg.train_list
    cfg.val_dataloader.dataset.datasets = cfg.val_list
    cfg.test_dataloader.dataset.datasets = cfg.test_list

    cfg.work_dir = options['work_dir']

    if not options['use_wandb']:
        for h in cfg.vis_backends:
            if h.type == 'WandbVisBackend':
                cfg.vis_backends.remove(h)

def train(options, args):
    cfg = Config.fromfile(options['mmocr_config_path'])
    args.config = options['mmocr_config_path']

    override_config(cfg, options)

    # load config
    cfg.launcher = args.launcher
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    # work_dir is determined in this priority: CLI > segment in file > filename
    if args.work_dir is not None:
        # update configs according to CLI args if args.work_dir is not None
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        # use config filename as default work_dir if cfg.work_dir is None
        cfg.work_dir = osp.join('./work_dirs',
                                osp.splitext(osp.basename(args.config))[0])
    # enable automatic-mixed-precision training
    if args.amp:
        optim_wrapper = cfg.optim_wrapper.type
        if optim_wrapper == 'AmpOptimWrapper':
            print_log(
                'AMP training is already enabled in your config.',
                logger='current',
                level=logging.WARNING)
        else:
            assert optim_wrapper == 'OptimWrapper', (
                '`--amp` is only supported when the optimizer wrapper type is '
                f'`OptimWrapper` but got {optim_wrapper}.')
            cfg.optim_wrapper.type = 'AmpOptimWrapper'
            cfg.optim_wrapper.loss_scale = 'dynamic'

    if args.resume:
        cfg.resume = True

    # enable automatically scaling LR
    if args.auto_scale_lr:
        if 'auto_scale_lr' in cfg and \
                'base_batch_size' in cfg.auto_scale_lr:
            cfg.auto_scale_lr.enable = True
        else:
            raise RuntimeError('Can not find "auto_scale_lr" or '
                               '"auto_scale_lr.base_batch_size" in your'
                               ' configuration file.')

    # build the runner from config
    if 'runner_type' not in cfg:
        # build the default runner
        runner = Runner.from_cfg(cfg)
    else:
        # build customized runner from the registry
        # if 'runner_type' is set in the cfg
        runner = RUNNERS.build(cfg)

    # start training
    runner.train()