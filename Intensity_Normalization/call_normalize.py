import glob
import os
import shutil
import matlab.engine
eng = matlab.engine.start_matlab()
list_folder = []
list_folder = glob.glob("/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-t1/*.nii")
for i in list_folder:
	if i.endswith("_t1.nii"):
		eng.nyul_hist_normalization(i)
	else:
		filepath = i
		shutil.move(filepath, '/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-t1-normalized')