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

## Model Arcitecture
The regular U-Net architecture consists of a contracting path or the encoder which extracts the high-level features, and an expansive path or the decoder, which upsamples the features to create a high-resolution output. We place the ASPP layer consisting of paralel Atrous convolutions at the end of the contracting path. The output of the last layer of contracting path is fed to the ASPP layer. The output of ASPP is concatenated and a 1x1 covolution is applied, followed by Batch Normalisation and ReLu activation. This is then fed as input to the enhancing path of the U-Net. All the concatenating operations between convolutuon layers in U-Net model have been maintained as such.

![alt text](https://github.com/JazBern/BrainTumor-Segmentation/blob/master/archi2%20(1).png)

## Tranining
For training, 2D slices with the four modalities as channels are created from four different types of scans. Each patient will have 155 2D slices with 4 channels.The UNet model is trained on the slices generated.

## Validaton
Out of 219 patients, the data of 59 patients are used for validation.

The training and evaluation code is in Unet.ipynb





