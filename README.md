# Brain Tumor Segmentation

## Brief Overview

Segmentation of tumor regions in brain MRI images using deep learning. A  combination of U-net and DeepLabV3+ is used to effectively segment the brain tumor regions.

## Data Preprocessing

1.Intensity Normalization : of NIfTI files in matlab based on https://in.mathworks.com/matlabcentral/fileexchange/38836-intensity-normalization-of-brain-volume .

```bash
python3 call_normalize.py
```
call_normalize.py calls the matlab script nyul_hist_normalisation.m

2.Conversion to .png files: The 3D NIfTI files are converted to .png files by slicing along 3 different directions.
The python utility https://github.com/FNNDSC/med2image is used to convert the .nii MRI scan files to 2d .png files.

```bash
med2image -i input.nii -d OutputDirectory -o OutputFileStem.png -s -1 -r
```




