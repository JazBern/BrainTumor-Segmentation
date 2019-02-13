"""...........................................................................................
Dividing the HGG folder containing the .nii.gz files of 3 different modalities  into repective
folders.
Also extracts the .nii.gz files to .nii
"""...........................................................................................
import os
import glob
import gzip
import shutil


list_folder = []
list_folder = glob.glob("/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG/*/")
for i in list_folder:
	list_file = []
	list_file = glob.glob(i+"*.gz")
	for j in list_file:
		if j.endswith("_flair.nii.gz"):
			source_filepath = j
			dest_filepath = j[0:-3];
			with gzip.open(source_filepath, 'rb') as f_in:
				with open(dest_filepath, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
		shutil.move(dest_filepath, '/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-flair')
		if j.endswith("_t1.nii.gz"):
			source_filepath = j
			dest_filepath = j[0:-3];
			with gzip.open(source_filepath, 'rb') as f_in:
				with open(dest_filepath, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
		shutil.move(dest_filepath, '/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-t1')
		if j.endswith("_t2.nii.gz"):
			source_filepath = j
			dest_filepath = j[0:-3];
			with gzip.open(source_filepath, 'rb') as f_in:
				with open(dest_filepath, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
		shutil.move(dest_filepath, '/Users/apple/Documents/ProjectS8/MICCAI_BraTS17_Data_Training/HGG-t2')
		

			
			
