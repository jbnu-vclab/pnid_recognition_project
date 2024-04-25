# pnid_recognition_project
P&amp;ID Recognition Project

### Training example
```
python ./tools/training/pnid_train.py ./options_example/pnid_train_example.yaml
```

## Installation
Our project depends on [MMRotate](https://github.com/open-mmlab/mmrotate). Please refer to installation guidance below.
For additional, you can refer [MMRotate Install Guide](https://mmrotate.readthedocs.io/en/latest/install.html) for more detailed instruction.  
It requires Python 3.7+, CUDA 9.2+ and PyTorch 1.6+.
### 1. create conda environment
```
conda create --n pnid python=3.8 -y
conda activate pnid
```
### 2. install pytorch ([official page](https://pytorch.org/get-started/previous-versions/))
```
conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=11.1 -c pytorch -c conda-forge
```
### 3. install mmrotate
```
pip install -U openmim
mim install mmcv-full
mim install mmdet<3.0.0

cd mmrotate
pip install -v -e .
```
**(Optional) verify mmrotate installation**
```
mim download mmrotate --config oriented_rcnn_r50_fpn_1x_dota_le90 --dest .
python demo/image_demo.py demo/demo.jpg oriented_rcnn_r50_fpn_1x_dota_le90.py oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth --out-file result.jpg
```
### 4. install our project
```
cd ..
pip install -v -e .
```