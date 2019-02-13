# Brain Tumor Segmentation

## Brief Overview

Segmentation of tumor regions in brain MRI images using deep learning. A combination of U-net and DeepLabV3+ is used to effectively segment the brain tumor regions.

## Dataset

BRATS 2017 training dataset has been used for the analysis of the proposed methodology. It consists of real patient images as well as synthetic images created by SMIR. Each of these folders are then subdivided into High Grade and Low Grade images. For each patient, four modalities(T1, T1-C, T2 and FLAIR) are provided.

## Data Preprocessing

1.Intensity Normalization: of NIfTI files in matlab based on https://in.mathworks.com/matlabcentral/fileexchange/38836-intensity-normalization-of-brain-volume .

```bash
python3 call_normalize.py
```
call_normalize.py calls the matlab script nyul_hist_normalisation.m

2.Conversion to .png files: The 3D NIfTI files are converted to .png files by slicing along 3 different directions.
The python utility https://github.com/FNNDSC/med2image is used to convert the .nii MRI scan files to 2d .png files.

```bash
med2image -i input.nii -d OutputDirectory -o OutputFileStem.png -s -1 -r
```




