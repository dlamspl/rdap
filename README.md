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
3. ansible-playbook -i hosts site.yml 



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
- Replace ```keypair``` with your key name
- Copy the key file in the ```keys``` directory

- Edit the file ```root_vars/ec2_image_vars.yml```
- Replace the ```region``` with your desired region name

Consult https://docs.aws.amazon.com/general/latest/gr/rande.html for available AWS region names


Step 03: Login/Verify your images (Not required if all playbooks are run)
---
To login to Phantom wait for a few minutes (5-10) and then you can access the instance at 
https://PUBLIC_IP
Use the below credentials to login to the web interface
username: admin
password: password

Please change the default admin password asap.
To login to the Centos Image ssh to the public IP with the -i key option and the file name.

Examples:
- Phantom ```https://SOME_PUBLIC_IP/```
- Splunk Centos ```ssh -i "your_key.pem" centos@SOME_PUBLIC_IP```

Check the hosts file and make sure the right IPs are under the correct group. Verify on AWS the settings

