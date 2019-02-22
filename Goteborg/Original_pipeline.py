import os

## MOUNTING INFORMATION
mount_dir = '/data/reckoner_forsklagr/PET:/data/reckoner_forsklagr/PET'
appian = 'tffunck/appian:latest'
launch_cmd = 'docker run --rm -v %s %s bash -c "python2 /opt/APPIAN/Launcher.py '%(mount_dir,appian)

# DIRECTORIES
input_dir = '/data/reckoner_forsklagr/PET/raw_data'
output_dir = '/data/reckoner_forsklagr/PET/processed_data/'
launch_cmd += '-s %s -t %s '%(input_dir, output_dir)

# EXTRACTION
atlas = '/opt/APPIAN/Atlas/MNI152/dka.mnc'
atlas_template = '/opt/APPIAN/Atlas/MNI152/mni_icbm152_t1_tal_nlin_asym_09c.mnc'
atlas_name = 'dkt'
launch_cmd += '--results-label-img %s  --results-label-template %s --results-label-name %s '%(atlas,
	                                                                                       atlas_template,
	                                                                                       atlas_name)

# PVE
pvc_method = 'GTM'
fwhm = '5 5 5'
pvc_atlas = '/opt/APPIAN/Atlas/MNI152/dka.mnc'
pvc_template = '/opt/APPIAN/Atlas/MNI152/mni_icbm152_t1_tal_nlin_asym_09c.mnc'
pvc_name = 'GTM'
launch_cmd += '--pvc-method %s --fwhm %s --pvc-label-img %s --pvc-label-template %s --pvc-label-name %s '%(pvc_method,
	                                                                                                   fwhm,
	                                                                                                   pvc_atlas,
	                                                                                                   pvc_template,
	                                                                                                   pvc_name)


## INFERIOR CEREBELLUM
IC_cmd = launch_cmd
# QUANTIFICATION
method = 'suvr'
ref_atlas = '/data/reckoner_forsklagr/PET/misc/ref_regions/suit_cerebellum_atlas.mnc'
ref_template = '/data/reckoner_forsklagr/PET/misc/ref_regions/suit_T1_template.mnc'
ref_labels = '6 ' + ''.join(['%s '%x for x in range(8,29)]) +'33 34'
ref_name = 'InfCereb'
IC_cmd += '--quant-label-img %s --quant-label-template %s --quant-label %s --quant-labels-ones-only --quant-method %s --quant-label-name %s '%(ref_atlas, 
	                                                                                                                                           ref_template,
	                                                                                                                                           ref_labels,
	                                                                                                                                           method,
	                                                                                                                                           ref_name)
IC_cmd += '"'

### RUN PIPELINE
os.system(IC_cmd)

## WHOLE CEREBELLUM PIPELINE
WCB_cmd = launch_cmd
method = 'suvr'
ref_atlas = '/data/reckoner_forsklagr/PET/misc/ref_regions/suit_cerebellum_atlas.mnc'
ref_template = '/data/reckoner_forsklagr/PET/misc/ref_regions/suit_T1_template.mnc'
ref_labels = ''.join(['%s '%x for x in range(1,35)])
ref_name = 'WHOLECereb'
WCB_cmd += '--quant-label-img %s --quant-label-template %s --quant-label %s --quant-labels-ones-only --quant-method %s --quant-label-name %s '%(ref_atlas, 
	                                                                                                                                            ref_template,
	                                                                                                                                            ref_labels,
	                                                                                                                                            method,
	                                                                                                                                            ref_name)
### RUN PIPELINE
WCB_cmd += '"'
os.system(WBC_cmd)

## WHITE MATTER PIPELINE

WM_cmd = launch_cmd
method = 'suvr'
ref_labels = '3'
erosion = '5'
ref_name = 'ErodedWM'
WM_cmd += '%s --quant-label %s --quant-labels-ones-only --quant-method %s --quant-label-name %s --quant-label-erosion %s '%(ref_labels,
	                                                                                                                        method,
	                                                                                                                        ref_name,
	                                                                                                                        erosion)
WM_cmd += '"'
os.system(WM_cmd)