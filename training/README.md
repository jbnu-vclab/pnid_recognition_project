# Training
Training related modules

## How to 
1. Run `sanitize_xml` to convert source xml to sanitized version
2. (Optional) Run `xml_dota_converter` to generate dota txt files
3. Run `dota_dataset_generation` to generate patch-segmented training data
   * if you didn't run step 2, set `convert_from_xml = true` option
   * else, set `data_dir` to folders of dota txt files and set `convert_from_xml = false`
4. run `pnid_train`

## Modules

* [sanitize_xml](./sanitize_xml)
  * Sanitize xml for possible error in annotation
  * e.g. typo of class name, out of image symbol, etc...
* [pnid_train](./pnid_train)
  * Train P&ID detection using [MMRotate](../mmrotate)
  * Follow the instruction of [MMRotate Installation](https://github.com/open-mmlab/mmrotate?tab=readme-ov-file#installation) to prepare the environment
  * Tested on MMRotate 0.3.4
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