RDAP 
---

RDAP is small collection of ansible playbooks aimed at seting up a POC/DEMO environment 
of splunk and phantom on EC2. This small project started with the following objectives:
1. Be as standalone as possible. Meaning no specific host OS or minimal installed packages
2. Easy to run and documented (to a certain extent)
3. Provide out of the box Splunk standlone and Phantom environment for demo or POC
4. To learn ansible and Splunk

Tested on:
* Python 2.7.10
* MacOSX
* Splunk 7.2
* Phantom 4.1

What you need
---
* Python environment 2.7.x
* Virtualenv
* EC2 API credentials
* EC2 SSH key pair
* Valid Splunk license (optional)
* Splunk app packages (optional)

Notes:
- Charges will be applied on your running EC2 instances as per amazon policies
- Phantom AMI from marketplace recommends t2.xlarge instance type. The default for this playbook is t2.medium

[Quick Install]
---
1. Complete Steps 01-02
3. ```ansible-playbook -i hosts site.yml ```


Step 01: Setup your ansible environment
----
On your host run the below commands to setup your ansible running environment
```
git clone https://github.com/dlamspl/rdap.git
cd rdap
virtualenv --python=/usr/bin/python2.7 dev
source dev/bin/activate
pip install ansible
```

This will create a virtual python environment for your ansible installation

Step 02: Setup EC2 prerequisites
---

1. Get your EC2 API credentials and select which zone you want the images to be deployed
2. Make sure you have access to your SSH AWS key pair

- Edit the file ```root_vars/ec2_credentials_vars.yml```
- Replace ```aws_secret_key/aws_access_key``` with your EC2 API credentials

- Edit the file ```root_vars/ec2_image_vars.yml```
- Replace the ```region``` with your desired region name (default is ap-south-1)
- Replace ```keypair``` with your key name
- Copy the key file in the ```keys``` directory


Create the images:
```ansible-playbook -i hosts site.yml```

Consult https://docs.aws.amazon.com/general/latest/gr/rande.html for available AWS region names

Step 03: Customize image settings
---
The file ```root_vars/ec2_image_vars.yml``` contains several settings for customizing the creation of Splunk and Phantom image on AWS. The below list only shows the ones of interest for first time customization. 

```
region: ap-south-1 # Change the Region

demo_env: 1 # Set this to 1 if you want full demo environment setup (Work in Progress)
splunk_init: 1 # If this is set to 1 it will create Centos AWS image (to be used for splunk)
phantom_init: 1 # If this is set to 1 it will create the Phantom image from AWS marketplace

splunk_aws:
  instance_type: t2.small
  security_group_name: splunk-servers # Change the security group name here
  security_group_desc: "Security Group for splunk Servers"
  image_ami_id: "ami-1780a878" # This is the linux Centos AMI 
  hosts_group: "splunk_servers"
  instance_name_tag: "RDAPSplunkServer"
  disk_size: "20" # Disk size in GB
  disk_type: "gp2" # If you want high IOPS set this to io1
  iops: 1000 # Set this to IOPS you want if the above setting is io1, otherwise it is ignored
  count_instances: 1 # How many instances with this tag you want to create


phantom_aws:
  instance_type: t2.medium # Recommended is t2.xlarge but works with t2.medium
  security_group_name: phantom-servers # Change the security group name here
  security_group_desc: "Security Group for phantom Servers"
  image_ami_id: "ami-09a93840158ec5b96" # This is the Phantom AMI 
  hosts_group: "phantom_servers"
  instance_name_tag: "RDAPPhantomServer"
  disk_size: "200" # Minimum default disk size for Phantom
  disk_type: "gp2"  # Generic disk will give you 600 IOPS
  count_instances: 1 # How many instances your want to create with this tag

```  

To show deployment information:
```ansible-playbook -i hosts site.yml --tags "info"```

Step 04: Login/Verify your images (Not required if all playbooks are run)
---
To login to Phantom wait for a few minutes (5-10) and then you can access the instance at 
```
https://PUBLIC_IP
Use the below credentials to login to the web interface
username: admin
password: password
```

Please change the default admin password asap.
To login to the Centos or Phantom Image ssh to the public IP with the -i key option and the file name.

Examples:

- Phantom ```https://SOME_PUBLIC_IP/```
- Splunk Centos ```ssh -i "your_key.pem" centos@SOME_PUBLIC_IP```

Check the hosts file and make sure the right IPs are under the correct group. Verify on AWS the settings

