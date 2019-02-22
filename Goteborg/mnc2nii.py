import os
import nibabel as nib
import tkinter as tk
from tkinter import filedialog
from glob import glob

### PROMPT USER FOR DIRECTORY
root = tk.Tk()
root.withdraw()
dirname = filedialog.askdirectory(parent=root,title='Please select directory you want to convert')

if dirname == ():
    raise ValueError('No directory selected. Aborting!')

print(dirname)
### PROMPT USER FOR RECURSIVE OR NOT
response = input('Do you want to recursively convert every .mnc file in the tree? ')
if response not in ('y','n','Y','N','Yes','No','yes','no'):
    raise IOError('Response not recognized')
else:
    if response in ('Yes','yes','y','Y'):
        ans = True
        hold = False
    else:
        ans = False
        hold = False

### COLLECT ALL MNCs
if ans:
    all_fls = []
    for dirs, things, fls in os.walk(dirname):
        if len(fls) > 0:
            for fl in fls:
                all_fls.append(os.path.join(dirs,fl))
else:
    all_fls = sorted(glob(os.path.join(dirname,'*')))

all_mncs = [x for x in all_fls if '.mnc' in x]

print('%s .mnc and .mnc.gz files found'%(len(all_mncs)))

### SEARCH TO SEE IF NIFTI VERSIONS ALREADY EXIST
already_done = []
for mnc in all_mncs:
    flnm = mnc.split('.')[0]
    ni = glob('%s.ni*'%flnm)
    if len(ni) > 0:
    	already_done.append(mnc)

print('%s mncs already have a nifti version. Skipping these files...'%(len(already_done)))
[all_mncs.remove(x) for x in already_done]

print('the following files will be converted:')
[print(x) for x in all_mncs]

### PROMPT USER ABOUT DELETION
response = input('Do you want to delete the mnc files? Not recommended unless low on space... ')
if response not in ('y','n','Y','N','Yes','No','yes','no'):
    raise IOError('Response not recognized')
else:        
    if response in ('Yes','yes','y','Y'):
       ans = True
       hold = False
    else:
        ans = False
        hold = False

### TRANSFORM FILES
for mnc in all_mncs:
    flnm = mnc.split('.')[0]
    if mnc[-1] == 'z':
        new_nm = '%s.nii.gz'%flnm
    else:
        new_nm = '%s.nii'%flnm
    img = nib.load(mnc)
    nifti = nib.Nifti1Image(img.get_data(), img.affine).to_filename(new_nm)
    print('converted %s to %s'%(mnc,new_nm))
    if ans:
        os.remove(mnc)

