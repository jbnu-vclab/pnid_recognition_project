# Training (TBU)
Training related modules

## How to 

1. Run `dota_dataset_generation` to generate patch-segmented training data
   * Check [option yaml](../../options_example/dota_dataset_generation_example.yaml)
   * Example
        ```shell
        python -m training.dota_dataset_generation.dataset_generation ./options_example/dota_dataset_generation_example.yaml
        ```
2. Run `pnid_train` to train the model
   * Check [option yaml](../../options_example/pnid_train_example.yaml)
   * Example
        ```shell
        python -m training.pnid_train.pnid_train ./options_example/pnid_train_example.yaml
        ```

## Modules

* [pnid_train](symbol_train)
  * Train P&ID detection using [MMRotate](../../mmrotate)
  * Follow the instruction of [MMRotate Installation](https://github.com/open-mmlab/mmrotate?tab=readme-ov-file#installation) to prepare the environment
* [dota_dataset_generation](dataset_generation/dota_dataset_generation)
  * Generate patch-segmented image files and patch-segmented DOTA txt files
  * (NOTE) Used [img_split](dataset_generation/dota_dataset_generation/external/img_split.py) from MMRotate without modification
  * Resulting training dataset directory structure
    ```bash 
    <save_dir>
        ├── dataset_gen_options.yaml
        ├── test
        │   ├── annfiles
        │   └── images
        ├── train
        │   ├── annfiles
        │   └── images
        ├── val
        │   ├── annfiles
        │   └── images
        └── temp                     # automatically removed after running if remove-tmp-files is true
            ├── dota
            ├── test
            │   ├── ann              # full dota txt (not patch-segmented)
            │   └── img              # full image (not patch-segmented)
            ├── train
            │   ├── ann              # full dota txt (not patch-segmented)
            │   └── img              # full image (not patch-segmented)
            └── val
                ├── ann              # full dota txt (not patch-segmented)
                └── img              # full image (not patch-segmented)
    ```