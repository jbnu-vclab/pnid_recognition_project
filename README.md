# pnid_recognition_project
P&amp;ID Recognition Project

Each module can be executed using the following command.
`${module_path}` is a module path separated by `'.'` instead of `'/'` and it doesn't include `'.py'` in the path.
```shell
python -m ${module_path} ${yaml_path}

#Example
python -m training.pnid_train.pnid_train ./options_example/pnid_train_example.yaml
```