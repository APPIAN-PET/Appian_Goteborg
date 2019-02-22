# Installing & Running APPIAN 

For information about APPIAN (including user guide), please refer to https://github.com/APPIAN-PET/APPIAN.

For questions and comments about using APPIAN, please post to the APPIAN-user mailing list : https://groups.google.com/forum/#!forum/appian-users. For other inquiries, you can contact me at either thomas.funck@mail.mcgill.ca or tffunck@gmail.com.

## Installing Docker on Redhat
### Update Yum repositories
 ``sudo yum update -y``
### Add the yum repo:
```sudo vim /etc/yum.repos.d/docker.repo```
Enter `:set paste`
Copy and paste (ctrl+shift+v) the following to the end of the file:
```
 [dockerrepo]
 name=Docker Repository
 baseurl=https://yum.dockerproject.org/repo/main/centos/7/
 enabled=1
 gpgcheck=1
 gpgkey=https://yum.dockerproject.org/gpg
```

## Start Docker
### Add user to “docker” group. This allows you to run docker without having to explicitly use “sudo”
 ```sudo usermod -g docker $USER```
Log out and log back in
Run test docker command : 
```docker run hello-world```
## Installing APPIAN
### Pull APPIAN image from Docker Hub
 ```docker pull tffunck/appian:latest```

### If docker pull gives you the error “No Space Left on Device”, use this work-around:
  1. ```sudo vim /lib/systemd/system/docker.service```
  2. Add ```-g /path/to/docker/``` at the end of ExecStart. The line should look like this: ```ExecStart=/usr/bin/dockerd -g ~pwd/docker”```. Save and exit.
 3. ```systemctl daemon-reload```
 4. ```systemctl restart docker```
 5. Execute command to check docker directory: ```docker info | grep "loop file\|Dir"```

### (Optional) Run APPIAN Test 
```docker run --rm tffunck/appian:latest bash -c "/opt/APPIAN/Test/validate_appian.sh"```

# Running APPIAN on your data
The following section will explain how to run your data with Appian

## Prepare your data for Appian
Your files need to be named and organized in an extremely specific way in order for Appian to read them properly. The directory structure should look like this (CAPITALS INDICATE USER INPUT):

sub-SUBJECT

    --> ses-SESSION
    
        --> anat
        
            --> sub-SUBJECT_ses-SESSION_T1w.nii (or .mnc; or .mnc/nii.gz)
            
        --> pet
        
            --> sub-SUBJECT_ses-SESSION_pet.nii (or .mnc; or .mnc/nii.gz)
            
            --> sub-SUBJECT_ses-SESSION_pet.json

The data must be organized exactly like this, with these naming conventions. An example can be found in /data/reckoner_forsklagr/PET/raw_data.

The json file can be created using any text editor and saving the data with a .json extension.
You can probably use the same jsom for every subject, as the time of the frames should not vary.
However, if you are missing a frame, you will need to change the variable Time:FrameTimes:Values.
For example, a value of [[70,75],[75,80],[80,85],[85,90]] would indicate the frame times are:
* 70-75 minutes
* 75-80 minutes
* 80-85 minutes
* 85-90 muntes

So, if you were missing the third frame, the value should be changed to [[70,75],[75,80],[85,90]]
Example jsons can be found in /data/reckoner_forsklagr/PET/raw_data

## Run Appian
You can always run appian manually from the command line. Refer to the Appian git for tutorials and examples.

Two scripts have been created to help you run Appian easily. Both can be found here:

/data/reckoner_forsklagr/PET/scripts/

We may periodically change these scripts for you. You can get the updated versions by navigating to:

/data/reckoner_forsklagr/PET/scripts/Appian_Wrappers/Goteborg

and typing ```git pull```

To run either script, you type ```python 3.6 SCRIPTNAME.py

### Original_pipeline.py
This script will immediately run Appian using all of the defauts we set up with Michael. This includes the following:

* Files living in /data/reckoner_forsklagr/PET/raw_data
* Default MR processing
* SUVR qunatification method
* Inferior cerebellum, whole cerebellum and eroded white matter reference regions, separately
* No PVC and GTM PVC using the DKT (freesurfer) atlas
* Extraction of ROI level information using the DKT atlas 

These assume all of your inputs are in /data/reckoner_forsklagr/PET/raw_data
Whenever you add a new subject (or subjects) to your input directory, you can run this script and the new subject(s) will be automatically processed.

### Modify_Pipeline.py
If you would like to change or add any of the above options, you can run the Modify_Pipeline script. This will produce a series of dialog boxes to walk you through which changes you want to make. 

Upon running the script, you will be presented with several categories. Select all categories you wish to change. Follow along with the instructions.

Afterwards, it will produce the commandline command to run the entire pipeline based on your changes. You can copy and store this if you want. You will then be asked if you want to run the pipeline.

# MR Options
As of now, the MR processing of Appian remains in a suboptimal state. In the future, Appian will use ANTs, which will surmount all of these issues. For now, you have two options.

### Option 1: Use default MR processing
We have tried to update the registration algorithms for Appian. Hopefully these will be sufficient to allow for satifactory PET processing

### Option 2: Provide your own MR files
If you are unsatisfied with the default MR procesing (e.g. many subjects are failing MR->Template, reference region->MR or atlas->MR), you can run your own MR processing pipeline, and feed the results to Appian.

Appian needs two things:
1) Reference region(s) in native space
2) ROI extraction atlas(es) in native space (this would be for both PVC, and for ROI value extraction)

Both of these files would be placed in the anat dir of each subject. The reference region(s) would be labeled:

sub-SUBJECT_ses-SESSION_REFLABEL.nii (or .mnc; or .mnc/nii.gz)

Where label is a consistent label for the reference region across all subject, like "Cerebellum". The atlas(es) would be labeled similarly:

sub-SUBJECT_ses-SESSION_ATLASLABEL.nii (or .mnc; or .mnc/nii.gz)

This time, the label should be something related to the atlas, like DKT, and again, should be consistent across subjects.

Once you do this, you can run the Modify_Pipeline.py script, and indicate you want to change options related the reference_region, PVC and roi_extraction. When prompted, indicate Yes you will be providing your own images. next, when prompted, give the REFLABEL or ATLASLABEL you chose in the filenames above. 

# QC
Appian ships with a high-tech dashboard to aid qualitative and quantitative QC. More on how to implement this is coming soon.

For now, it is very important you check how well Appian processed your data. Check the following:
* Are my SUVR values within the expected range? If not, there may have been a problem with the reference region normalization, or the MR->template registration
* Do my images look right? If not, there is likely an issue with the brainmasking or MR -> template registation

<MORE COMING SOON>

# Troubleshooting
At this point, if you can't figure out an issue and you're doubly sure you've encoded all the correctly, contact Thomas or Jake for help.
