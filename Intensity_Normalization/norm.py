import os
import numpy as np
import nibabel as nib
from statistics import *
from math import *

data_from = '/home/aarya/Documents/project/dataset1'
data_to = '/home/aarya/Documents/project/dataset_normalized'
nii_files_seg = []
nii_files_flair = []
nii_files_t1 = []
nii_files_t2 = []
nii_files_t1ce= []

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
                elif 't1ce' in i:
                    nii_files_t1ce += [[i, data_from] + get_landmarks(i, data_from)]
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
    
    threshold = mean(val)
    tmp = len(val)
    foreground = list(filter((threshold).__lt__, val))     # foreground values
    med = mode(foreground)
    val = list(set(val))
    val.sort()
    i = min(len(val)-1, floor(0.998 * (len(val))) + 1)
    # print(0, med, val[i])
    return [int(val[0]), int(med), int(val[i])]

def get_stnd_landmarks(nii_files):
    val = []
    
    stnd_med = 0

    for [nii, data_from, low, med, high] in nii_files:
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
# with open('/home/aarya/Documents/project/t1ce', 'w') as f:
    # f.write(str(nii_files_t1ce))
# with open('/home/aarya/Documents/project/t1ce') as f:
    # nii_files_t1ce = eval(f.read())
normalize()
# print(nii_files_seg)