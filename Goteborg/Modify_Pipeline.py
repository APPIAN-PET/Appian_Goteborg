## ACTIVATE PYTHON ENVIRONMENT
os.system('source deactivate')
os.system('source /data/reckoner_forsklagr/py_envs/appiandev/bin/activate')

import os
import tkinter as tk
from tkinter import filedialog

def select_file(message):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(parent=root,title=message)

    if file_path == ():
    	raise ValueError('No file selected. Aborting!')

    return file_path

def select_directory(message):
    root = tk.Tk()
    root.withdraw()
    dirname = filedialog.askdirectory(parent=root,title=message)

    if dirname == ():
        raise ValueError('No directory selected. Aborting!')

    return dirname

def retrieve_input(message):
    ans = input(message)
    return ans

def execute_pipeline(mount_dir, appian, input_dir, output_dir ,atlas,
	                 atlas_template, atlas_name, pvc_method, fwhm,
	                pvc_atlas, pvc_template, pvc_name, method,
	                ref_atlas, ref_template, ref_labels, ref_name,
	                other):
    
    
    dir_cmd = '-s %s -t %s '%(input_dir, output_dir)
    output_dir = '/data/reckoner_forsklagr/PET/processed_data/'
    launch_cmd = 'docker run --rm -v %s %s bash -c "python2 /opt/APPIAN/Launcher.py '%(mount_dir,appian)
    extract_cmd = '--results-label-img %s  --results-label-template %s --results-label-name %s '%(atlas,
	                                                                                       atlas_template,
	                                                                                       atlas_name)
    pvc_cmd = '--pvc-method %s --fwhm %s --pvc-label-img %s --pvc-label-template %s --pvc-label-name %s '%(pvc_method,
	                                                                                                   fwhm,
	                                                                                                   pvc_atlas,
	                                                                                                   pvc_template,
	                                                                                                   pvc_name)
    quant_cmd = '--quant-label-img %s --quant-label-template %s --quant-label %s --quant-labels-ones-only --quant-method %s --quant-label-name %s '%(ref_atlas, 
	                                                                                                                                           ref_template,
	                                                                                                                                           ref_labels,
	                                                                                                                                           method,
	                                                                                                                                           ref_name)
    cmd = launch_cmd + dir_cmd + extract_cmd + pvc_cmd + quant_cmd + other + '"'

    print('HERE IS YOUR COMMAND')
    print(cmd)

    hold = True
    while hold:
    	response = input('Execute pipeline? y/n  ')
    	if response not in ('y','n','Y','N','Yes','No','yes','no'):
    	    raise IOError('Response not recognized')
    	if response in ('Yes','yes','y','Y'):
            ans = True
            hold = False
    	else:
            ans = False
            hold = False

    if ans:
    	os.system(cmd)
    


### SET DEFAULTS
mount_dir = '/data/reckoner_forsklagr/PET:/data/reckoner_forsklagr/PET'
appian = 'tffunck/appian:latest'
input_dir = '/data/reckoner_forsklagr/PET/raw_data'
output_dir = '/data/reckoner_forsklagr/PET/processed_data/'
atlas = '/opt/APPIAN/Atlas/MNI152/dka.mnc'
atlas_template = '/opt/APPIAN/Atlas/MNI152/mni_icbm152_t1_tal_nlin_asym_09c.mnc'
atlas_name = 'dkt'
pvc_method = 'GTM'
fwhm = '4 4 4'
pvc_atlas = '/opt/APPIAN/Atlas/MNI152/dka.mnc'
pvc_template = '/opt/APPIAN/Atlas/MNI152/mni_icbm152_t1_tal_nlin_asym_09c.mnc'
pvc_name = 'GTM'
method = 'suvr'
ref_atlas = '/data/reckoner_forsklagr/PET/misc/ref_regions/suit_cerebellum_atlas.mnc'
ref_template = '/data/reckoner_forsklagr/PET/misc/ref_regions/suit_T1_template.mnc'
ref_labels = '6 ' + ''.join(['%s '%x for x in range(8,29)]) +'33 34'
ref_name = 'InfCereb'
other = ''

### QUERY WHICH CATEGORY USER WISHES TO CHANGE
options = ['Inputs/Outputs', 'Extraction Atlas', 'PVC', 'Quantification', 'Appian', 'Other']

print('WHAT DO YOU WANT TO CHANGE? SELECT ALL THAT APPLY')
root = tk.Tk()
l = tk.Listbox(root, width = 15,selectmode=tk.EXTENDED)
l.pack()
[l.insert(tk.END,x) for x in options]
def close():
    global l, root, selection
    selection = [l.get(idx) for idx in l.curselection()]
    root.destroy()
b = tk.Button(root, text = "OK", command = close).pack()
root.mainloop()

### QUERY SPECIFIC CHANGES
if 'Inputs/Outputs' in selection:
    input_dir = select_directory('Please select your desired input directory')
    output_dir = select_directory('Please select your desired output directory')

if 'Extraction Atlas' in selection:
    atlas = select_file('Please select the atlas to be used for ROI values')
    atlas_template = select_file('Select the template space (e.g. MNI) of the atlas')
    msg = 'Please supply a label, like "dkt" (non unique labels will overwrite existing files): '
    atlas_name = retrieve_input(msg)

if 'PVC' in selection:
    pvc_method = retrieve_input('Choose a method from these choices: GTM, VC, idSURF ')
    if pvc_method not in ['GTM','VC','idSURF']:
        print('Input not recognized. Please choose GTM, VC or idSURF')
        pvc_method = retrieve_input('Choose a method from these choices: GTM, VC, idSURF ')
        if pvc_method not in ['GTM','VC','idSURF']:
            raise IOError('PVC choice not recognized')
	pvc_atlas = select_file('Please select atlas to use for PVC')
	pvc_template = select_file('Please select the template space (e.g.) MNI of the atlas')
	msg = 'Please supply a label, like "GTM" (non unique labels will overwrite existing files): '
	pvc_name = retrieve_input(msg)

if 'Quantification' in selection:
    print('NOTE: This script will only give options for suv and suvr')
    print('for other options, please consult APPIAN docs: https://github.com/APPIAN-PET/APPIAN/tree/master/Tracer_Kinetic/methods')
    print('To use these options, restart script, select other, and pass the relevant Appian commands')
    method = retrieve_input('Choose a method from these choices: suv, suvr ')
    if method not in ['suv','suvr']:
        print('Input not recognized. Please choose suv or suvr')
	method = retrieve_input('Choose a method from these choices: suv, suvr ')
	if pvc_method not in ['suv','suvr']:
	    raise IOError('Quant method choice not recognized')
    ref_atlas = select_file('Please select atlas containing reference region(s)')
    ref_template = select_file('Select the template space (e.g. MNI) of the atlas')
    ref_labels = retrieve_input('Please list the label number(s) for your reference region(s), separated by spaces')
    msg = 'Please supply a label, like "InfCereb" (non unique labels will overwrite existing files): '
    ref_name = retrieve_input(msg)

if 'Appian' in selection:
    mount_dir = select_directory('Please select directory to mount (where all your files are) ')
    ansr = retrieve_input('Choose a version from these choices: stable, dev, other')
    if ansr not in ['stable','dev','other']:
        print('Input not recognized. Please choose stable, dev or other')
	method = retrieve_input('Choose a method from these choices: suv, suvr ')
	if method not in ['stable','dev','other']:
	    raise IOError('Appian version choice not recognized')
	if ansr == 'stable':
	    appian = 'tffunck/appian:latest'
	elif ansr == 'dev':
	    appian = 'tffunck/appian:latest-dev'
	else:
	    appian = retrive_input('Please enter full address to appian version (e.g. tffunck/appian:latest' )

if 'other' in selection:
    msg = 'Please enter additional Appian commands as you would enter into the command line'
    other = retrieve_input(msg)
    
execute_pipeline(mount_dir, appian, input_dir, output_dir ,atlas,
	             atlas_template, atlas_name, pvc_method, fwhm,
	             pvc_atlas, pvc_template, pvc_name, method,
	             ref_atlas, ref_template, ref_labels, ref_name,
	             other)



