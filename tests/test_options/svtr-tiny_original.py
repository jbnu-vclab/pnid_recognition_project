dictionary = dict(
    type='Dictionary',
    dict_file='',                           # <-- override
    with_padding=True,
    with_unknown=False)
model = dict(
    type='SVTR',
    encoder=dict(
        type='SVTREncoder',
        img_size=[32, 248],
        in_channels=3,
        out_channels=192,
        embed_dims=[64, 128, 256],
        depth=[3, 6, 3],
        num_heads=[2, 4, 8],
        mixer_types=[
            'Local', 'Local', 'Local', 'Local', 'Local', 'Local', 'Global',
            'Global', 'Global', 'Global', 'Global', 'Global'
        ],
        window_size=[[7, 11], [7, 11], [7, 11]],
        merging_types='Conv',
        prenorm=False,
        max_seq_len=62),
    decoder=dict(
        type='SVTRDecoder',
        in_channels=192,
        module_loss=dict(
            type='CTCModuleLoss', letter_case='unchanged', zero_infinity=True),
        postprocessor=dict(type='CTCPostProcessor'),
        dictionary=dict(
            type='Dictionary',
            dict_file='',                   # <-- override
            with_padding=True,
            with_unknown=False)),
    data_preprocessor=dict(
        type='TextRecogDataPreprocessor', mean=[127.5], std=[127.5]))
train_pipeline = [
    dict(type='LoadImageFromFile', ignore_empty=False),
    dict(type='LoadOCRAnnotations', with_text=True),
    # dict(
    #     type='RandomApply',
    #     prob=0.5,
    #     transforms=[
    #         dict(
    #             type='RandomChoice',
    #             transforms=[
    #                 dict(type='RandomRotate', max_angle=45),
    #                 dict(
    #                     type='TorchVisionWrapper',
    #                     op='RandomAffine',
    #                     degrees=45,
    #                     translate=(0.3, 0.3),
    #                     scale=(0.5, 2.0),
    #                     shear=(15, 45)),
    #                 dict(
    #                     type='TorchVisionWrapper',
    #                     op='RandomPerspective',
    #                     distortion_scale=0.5,
    #                     p=1)
    #             ])
    #     ]),
    dict(
        type='RandomApply',
        prob=0.25,
        transforms=[
            dict(type='PyramidRescale'),
            dict(
                type='mmdet.Albu',
                transforms=[
                    dict(type='GaussNoise', var_limit=(20, 20), p=0.5),
                    dict(type='MotionBlur', blur_limit=7, p=0.5)
                ])
        ]),
    dict(
        type='RandomApply',
        prob=0.25,
        transforms=[
            dict(
                type='TorchVisionWrapper',
                op='ColorJitter',
                brightness=0.5,
                saturation=0.5,
                contrast=0.5,
                hue=0.1)
        ]),
    dict(
        type='RescaleToHeight',
        height=32,
        min_width=248,
        max_width=248,
        width_divisor=1),
    dict(
        type='PackTextRecogInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'valid_ratio'))
]
val_pipeline = [
    dict(type='LoadImageFromFile', ignore_empty=False),
    dict(type='LoadOCRAnnotations', with_text=True),
    dict(
        type='RescaleToHeight',
        height=32,
        min_width=248,
        max_width=248,
        width_divisor=1),
    dict(
        type='PackTextRecogInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'valid_ratio'))
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadOCRAnnotations', with_text=True),
    dict(
        type='RescaleToHeight',
        height=32,
        min_width=248,
        max_width=248,
        width_divisor=1),
    dict(
        type='PackTextRecogInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'valid_ratio'))
]
default_scope = 'mmocr'
env_cfg = dict(
    cudnn_benchmark=False,
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
    dist_cfg=dict(backend='nccl'))
randomness = dict(seed=1414799024)
default_hooks = dict(
    timer=dict(type='IterTimerHook'),
    logger=dict(type='LoggerHook', interval=50),
    param_scheduler=dict(type='ParamSchedulerHook'),
    checkpoint=dict(type='CheckpointHook', interval=1),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    sync_buffer=dict(type='SyncBuffersHook'),
    visualization=dict(
        type='VisualizationHook',
        interval=1,
        enable=False,
        show=False,
        draw_gt=False,
        draw_pred=False))
log_level = 'INFO'
log_processor = dict(type='LogProcessor', window_size=50, by_epoch=True)
load_from = None
resume = False
val_evaluator = dict(type='WordMetric', mode='exact', prefix=None)
test_evaluator = dict(type='WordMetric', mode='exact', prefix=None)
vis_backends = [dict(type='LocalVisBackend'), dict(type='WandbVisBackend')]
visualizer = dict(
    type='TextRecogLocalVisualizer',
    name='visualizer',
    vis_backends=[dict(type='LocalVisBackend'),
                  dict(type='WandbVisBackend')])
icdar2015_textrecog_data_root = ''              # <-- override
icdar2015_textrecog_train = dict(
    type='OCRDataset',
    data_root='',                               # <-- override
    ann_file='',                                # <-- override
    pipeline=None)
icdar2015_textrecog_val = dict(
    type='OCRDataset',
    data_root='',                               # <-- override
    ann_file='',                                # <-- override
    test_mode=True,
    pipeline=None)
icdar2015_textrecog_test = dict(
    type='OCRDataset',
    data_root='',                               # <-- override
    ann_file='',                                # <-- override
    test_mode=True,
    pipeline=None)
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(
        type='AdamW',
        lr=0.0005,
        betas=(0.9, 0.99),
        eps=8e-08,
        weight_decay=0.05))
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=20, val_interval=21)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=0.5,
        end_factor=1.0,
        end=2,
        verbose=False,
        convert_to_iter_based=True),
    dict(
        type='CosineAnnealingLR',
        T_max=19,
        begin=2,
        end=20,
        verbose=False,
        convert_to_iter_based=True)
]
train_list = []                                 # <-- override
val_list = []                                   # <-- override
test_list = []                                  # <-- override
train_dataloader = dict(
    batch_size=256,
    num_workers=12,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='ConcatDataset',
        datasets=[],                            # <-- override
        pipeline=[
            dict(type='LoadImageFromFile', ignore_empty=False),
            dict(type='LoadOCRAnnotations', with_text=True),
            # dict(
            #     type='RandomApply',
            #     prob=0.5,
            #     transforms=[
            #         dict(
            #             type='RandomChoice',
            #             transforms=[
            #                 dict(type='RandomRotate', max_angle=45),
            #                 dict(
            #                     type='TorchVisionWrapper',
            #                     op='RandomAffine',
            #                     degrees=45,
            #                     translate=(0.3, 0.3),
            #                     scale=(0.5, 2.0),
            #                     shear=(15, 45)),
            #                 dict(
            #                     type='TorchVisionWrapper',
            #                     op='RandomPerspective',
            #                     distortion_scale=0.5,
            #                     p=1)
            #             ])
            #     ]),
            dict(
                type='RandomApply',
                prob=0.25,
                transforms=[
                    dict(type='PyramidRescale'),
                    dict(
                        type='mmdet.Albu',
                        transforms=[
                            dict(type='GaussNoise', var_limit=(20, 20), p=0.5),
                            dict(type='MotionBlur', blur_limit=7, p=0.5)
                        ])
                ]),
            dict(
                type='RandomApply',
                prob=0.25,
                transforms=[
                    dict(
                        type='TorchVisionWrapper',
                        op='ColorJitter',
                        brightness=0.5,
                        saturation=0.5,
                        contrast=0.5,
                        hue=0.1)
                ]),
            dict(
                type='RescaleToHeight',
                height=32,
                min_width=248,
                max_width=248,
                width_divisor=1),
            dict(
                type='PackTextRecogInputs',
                meta_keys=('img_path', 'ori_shape', 'img_shape',
                           'valid_ratio'))
        ]))
val_dataloader = dict(
    batch_size=128,
    num_workers=8,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='ConcatDataset',
        datasets=[],                        # <-- override
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                type='RescaleToHeight',
                height=32,
                min_width=248,
                max_width=248,
                width_divisor=1),
            dict(
                type='PackTextRecogInputs',
                meta_keys=('img_path', 'ori_shape', 'img_shape',
                           'valid_ratio'))
        ]))
test_dataloader = dict(
    batch_size=128,
    num_workers=8,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='ConcatDataset',
        datasets=[],                        # <-- override
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                type='RescaleToHeight',
                height=32,
                min_width=248,
                max_width=248,
                width_divisor=1),
            dict(
                type='PackTextRecogInputs',
                meta_keys=('img_path', 'ori_shape', 'img_shape',
                           'valid_ratio'))
        ]))
launcher = 'pytorch'
work_dir = ''                               # <-- override
