# Tools
Dataset generation/training/inferernce/evaluation tools

## How to 

### Dataset Generation
Run `training/dataset_generation` to generate patch-segmented training data
   * Check [option yaml](../options_example/dota_dataset_generation_example.yaml)
   * Example
        ```shell
        python ./training/dota_dataset_generation.py ../options_example/dota_dataset_generation_example.yaml
        ```
### Training
Run `training/pnid_train` to train the model
   * Check [option yaml](../options_example/pnid_train_example.yaml)
   * Example
        ```shell
        python ./training/pnid_train.py ../options_example/pnid_train_example.yaml
        ```
     
### Inference
Run `inference/pnid_inference` to inference images using trained model
   * Check [option yaml](../options_example/pnid_inference_example.yaml)
   * Example
        ```shell
        python ./inference/pnid_inference ../options_example/pnid_inference_example.yaml
        ```
     
### Evaluate
Run `eval/pnid_evaluate` to evaluate the inference result
   * Check [option yaml](../options_example/pnid_eval_example.yaml)
   * Example
        ```shell
        python ./eval/pnid_evaluate.py ../options_example/pnid_train_example.yaml
        ```