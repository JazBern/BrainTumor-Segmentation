import os
import numpy as np
from scipy import stats
import nibabel as nib
from math import *
import random

data_from = '/home/aarya/Documents/project/a'
data_to = '/home/aarya/Documents/project/dataset_normalized'
nii_files_seg = []
nii_files_flair = []
nii_files_t1 = []
nii_files_t2 = []
# nii_files_t1ce = [['Brats18_2013_19_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_19_1', 0, 548, 1711], ['Brats18_2013_4_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_4_1', 0, 46, 246], ['Brats18_2013_7_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_7_1', 0, 301, 1367], ['Brats18_2013_12_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_12_1', 0, 360, 1490], ['Brats18_2013_13_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_13_1', 0, 567, 1348], ['Brats18_2013_10_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_10_1', 0, 592, 1515], ['Brats18_2013_5_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_5_1', 0, 513, 1783], ['Brats18_2013_17_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_17_1', 0, 647, 2100], ['Brats18_2013_3_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_3_1', 0, 54, 279], ['Brats18_2013_20_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_20_1', 0, 404, 1206], ['Brats18_2013_2_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_2_1', 0, 324, 1546], ['Brats18_2013_18_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_18_1', 0, 275, 1295], ['Brats18_2013_14_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_14_1', 0, 353, 1724], ['Brats18_2013_21_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_21_1', 0, 626, 1770], ['Brats18_2013_11_1_t1ce.nii.gz', '/home/aarya/Documents/project/a/HGG/Brats18_2013_11_1', 0, 56, 211]]
nii_files_t1ce = []

k = 10 # no of training samples to get the standard landmarks

def get_sample(nii_files):
    return random.sample(nii_files, k)

def init():
    global data_to
    os.chdir(data_from)
    ti = ''
    while os.path.exists(data_to+str(ti)):
        if ti == '':
            ti = 1
            data_to += '_'
        else:
            ti += 1

    data_to += str(ti)
    get_same_struc(data_from, data_to)
    

def get_same_struc(data_from, data_to):
    global nii_files_seg, nii_files_flair, nii_files_t1, nii_files_t2, nii_files_t1ce
    os.makedirs(data_to)
    l = os.listdir(data_from)
    for i in l:
        if i[0] != '.':
            if os.path.isdir(os.path.join(data_from, i)):
                get_same_struc(os.path.join(data_from, i), os.path.join(data_to, i))
            else:
                if 'seg' in i:
                    nii_files_seg += [[i, data_from]]
                if 't1ce' in i:
                    nii_files_t1ce += [[i, data_from] + get_landmarks(i, data_from)]
                    # print(nii_files_t1ce[len(nii_files_t1ce)-1])
                elif 't1' in i:
                    nii_files_t1 += [[i, data_from] + get_landmarks(i, data_from)]
                elif 't2' in i:
                    nii_files_t2 += [[i, data_from] + get_landmarks(i, data_from)]
                elif 'flair' in i:
                    nii_files_flair += [[i, data_from] + get_landmarks(i, data_from)]

def get_landmarks(nii, data_from):
    img = nib.load(os.path.join(data_from, nii))
    val = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            val += list(img.get_data()[i][j])
    
    threshold = np.mean(val)
    foreground = list(filter((threshold).__lt__, val))     # foreground values
    med = stats.mode(foreground)[0][0]
    val = list(set(val))
    val.sort()
    tmp = len(val)
    i = min(tmp-1, floor(0.998 * tmp) + 1)
    return [int(val[0]), int(med), int(val[i])]

def get_stnd_landmarks(nii_files):
    sample = get_sample(nii_files)

    val = []
    
    stnd_med = 0

    for [nii, data_from, low, med, high] in sample:
        img = nib.load(os.path.join(data_from, nii))
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                val += set(img.get_data()[i][j])
                val = list(set(val))
        stnd_med += med*(high-low)
    
    val.sort()
    
    i = min(len(val)-1, floor(0.998 * (len(val))) + 1)
    stnd_med //= (val[i] - val[0])
    # print(len(nii_files))

    # f = open(f,'w')
    # f.write(str(val))
    # f.close()

    # print(val[0], stnd_med, val[i])
    return (val[0], stnd_med, val[i])

def process_nii(nii, data_from, prop, st):
    low, med, high = prop
    st_low, st_med, st_high = st
    scale_low = (st_med - st_low) / (med - low)
    scale_high = (st_high - st_med) / (high - med)
    img = nib.load(os.path.join(data_from, nii))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                if img.get_data()[i][j][k] < med:
                    img.get_data()[i][j][k] *= scale_low
                else:
                    img.get_data()[i][j][k] *= scale_high
    return img

def transform(nii_files, st):
    for [nii, data_f, low, med, high] in nii_files:
        nii_norm = process_nii(nii, data_f, [low, med, high], st)
        dest = data_f.replace(data_from, data_to)
        print(os.path.join(dest, nii))
        nib.save(nii_norm, os.path.join(dest, nii))

def normalize():
    st = get_stnd_landmarks(nii_files_t1ce)
    # print(st)
    transform(nii_files_t1ce, st)

    st = get_stnd_landmarks(nii_files_t1)
    transform(nii_files_t1, st)

    st = get_stnd_landmarks(nii_files_t2)
    transform(nii_files_t2, st)

    st = get_stnd_landmarks(nii_files_flair)
    transform(nii_files_flair, st)

    for [nii, data_f] in nii_files_seg:
        img = nib.load(os.path.join(data_f, nii))
        dest = data_f.replace(data_from, data_to)
        print(os.path.join(dest, nii))
        nib.save(img, os.path.join(dest, nii))

init()
# print("done")
# with open('/home/aarya/Documents/project/t1ce', 'w') as f:
    # f.write(str(nii_files_t1ce))
# with open('/home/aarya/Documents/project/t1ce') as f:
    # nii_files_t1ce = eval(f.read())
normalize()
# print(nii_files_seg)
