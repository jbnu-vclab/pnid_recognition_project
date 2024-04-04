# Training
Training related modules

* [xml_dota_converter](./xml_dota_converter)
  * Convert training XML file to DOTA txt file
* [dota_dataset_generation](./dota_dataset_generation)
  * Generate patch-segmented image files and patch-segmented DOTA txt files
  * (NOTE) Used [img_split](./dota_dataset_generation/external/img_split.py) from MMRotate without modification
  * Check [options](./dota_dataset_generation/options.py) for arguments
    ```bash 
    <save_dir>
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
            ├── dota (optional)      # if convert-from-xml is true (if false, you should run xml_dota_converter to prepare DOTA txt files)
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