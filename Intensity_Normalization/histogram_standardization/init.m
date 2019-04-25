function init()

data_from = '/home/aarya/Documents/project/dataset2';
data_to = '/home/aarya/Documents/project/dataset2_normalized';

ref_seg = '/home/aarya/Documents/project/dataset2/LGG/Brats18_TCIA10_629_1/Brats18_TCIA10_629_1_seg.nii';
ref_flair = '/home/aarya/Documents/project/dataset2/HGG/Brats18_TCIA06_603_1/Brats18_TCIA06_603_1_flair.nii';
ref_t1 = '/home/aarya/Documents/project/dataset2/LGG/Brats18_TCIA09_312_1/Brats18_TCIA09_312_1_t1.nii';
ref_t1ce = '/home/aarya/Documents/project/dataset2/HGG/Brats18_TCIA06_247_1/Brats18_TCIA06_247_1_t1ce.nii';
ref_t2 = '/home/aarya/Documents/project/dataset2/HGG/Brats18_TCIA06_211_1/Brats18_TCIA06_211_1_t2.nii';

% seg
file = '/home/aarya/Documents/project/seg_path';
fid = fopen(file);
txt = fgetl(fid);
while(txt != -1)
    nyul_hist_normalization(ref_seg, txt, data_from, data_to);
    txt = fgetl(fid);
endwhile
fclose(fid);

% t1
file = '/home/aarya/Documents/project/t1_path'
fid = fopen(file);
txt = fgetl(fid);
while(txt != -1)
    nyul_hist_normalization(ref_t1, txt, data_from, data_to);
    txt = fgetl(fid);
endwhile
fclose(fid);

% t1ce
file = '/home/aarya/Documents/project/t1ce_path'
fid = fopen(file);
txt = fgetl(fid);
while(txt != -1)
    nyul_hist_normalization(ref_t1ce, txt, data_from, data_to);
    txt = fgetl(fid);
endwhile
fclose(fid);

% t2
file = '/home/aarya/Documents/project/t2_path'
fid = fopen(file);
txt = fgetl(fid);
while(txt != -1)
    nyul_hist_normalization(ref_t2, txt, data_from, data_to);
    txt = fgetl(fid);
endwhile
fclose(fid);

% flair
file = '/home/aarya/Documents/project/flair_path'
fid = fopen(file);
txt = fgetl(fid);
while(txt != -1)
    nyul_hist_normalization(ref_flair, txt, data_from, data_to);
    txt = fgetl(fid);
endwhile
fclose(fid);

endfunction