
import os
import glob
import shutil
import matlab.engine
eng = matlab.engine.start_matlab()
list_folder = []
# HGG-t1 contains the .nii files of T1 modality
list_folder = glob.glob("/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-t1/*.nii")
for i in list_folder:
	if i.endswith("_t1.nii"):
		eng.nyul_hist_normalization(i)
	else:
		#the normalised .nii ends with _t1_stretched.nii
		filepath = i
		shutil.move(filepath, '/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-t1-normalized')
