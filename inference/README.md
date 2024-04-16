# Inference
Inference related modules

## How to 
- Run `pnid_inference` to inference drawing based on learned model
   * Check [option yaml](../options_example/pnid_inference_example.yaml)
- (TODO) Run `pnid_inference.exe` to inference drawing based on learned model

## Modules

* [pnid_inference](./pnid_inference)
  * Load learned mmrotate model using config & checkpoint
    * Config file is automatically saved to `work_dir` during `pnid_train`
  * Perform inference of designated drawing image
    * To perform proper pre-processing, dataset option path should be given
    * dataset option file is automatically saved to `save_dir` during `dota_dataset_generation`