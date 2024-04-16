# Evaluation
Evaluation related modules

## How to 
- Run `pnid_evaluate` to calculate precision and recall of the result
   * Check [option yaml](../options_example/pnid_eval_example.yaml)
- (TODO) Run `pnid_inference.exe` to inference drawing based on learned model

## Modules

* [pnid_evaluate](./pnid_evaluate)
  * Evaluate detection result based on xml files in `dt_path`
    * Corresponding GT xmls are automatically found from `gt_path`
  * Make sure to use sanitized xml 