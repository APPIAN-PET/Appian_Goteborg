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


