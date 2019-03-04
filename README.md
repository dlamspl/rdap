RDAP 
---

RDAP is small collection of ansible playbooks aimed at seting up a POC/DEMO environment 
of splunk and phantom on EC2 (plus other stuff ;). This small project started with the following objectives:
1. Be as standalone as possible. Meaning no specific host OS or minimal installed packages
2. Easy to run and documented (to a certain extent) so that everyone can use it without being an ansible expert
3. Provide out of the box Splunk standlone and Phantom environment for demo or POC
4. To learn ansible and Splunk ! 

So what does RDAP do ?
---
In high level it does the following:
1. Create as many EC2 instances as required, both standard AMIs and Phantom 
2. Carry out base OS setup (Time, OS packges etc..)
3. Install Splunk software (currently in standalone mode)
4. Install various Splunk apps
5. Configure the Phantom instance on Splunk
6. Install monitoring agent for IT App for Infrastructure on the Splunk machine
7. Setup Phantom 4.1

For more see Appendix - 1 - Advanced usage

Tested on:
* Python 2.7.10
* MacOSX
* Splunk 7.2
* Phantom 4.1

Disclaimer: This is not official Splunk repository or code. Use at your own risk. 

What you need
---
* Python environment 2.7.x
* Virtualenv
* EC2 API credentials
* EC2 SSH key pair
* Valid Splunk license (optional)
* Splunk app packages (optional)

Notes:
- Charges will be applied on your running EC2 instances as per amazon pricing policies
- Phantom AMI from marketplace recommends t2.xlarge instance type. The default for this playbook is t2.large

What you get
---
Well you would have got a lot more, but there are some constraints:
1. Time
2. Some Splunk and Phantom functionality is not available via API or is not documented , therefore it is not straightforward to code the entire setup of the demo environment.

```
   -------         -------
  |       |       |       |
  | Splunk|  ---> |Phantom|
  |       |       |       |
   -------         -------
```
1. Splunk enterpise core with various apps installed and integrated with your Phantom instance
  - Phantom apps
  - IT app for infrastructure and localhost added as entity
  - Other apps
2. Phantom image already setup (or mostly setup)
  - Virustotal
  - AlienvaultOTX
  - Generator
  - Other free apps

![Splunk](https://github.com/dlamspl/rdap/blob/master/docs/images/splunkdefault.png)
![Phantom](https://github.com/dlamspl/rdap/blob/master/docs/images/phantomevents.png)
![SplunkITAppInfrastructure](https://github.com/dlamspl/rdap/blob/master/docs/images/splunkitapp.png)
![SplunkPhantom](https://github.com/dlamspl/rdap/blob/master/docs/images/splunkphantom.png)


[Quick Install]
---
1. Complete Steps 01-02
2. ```ansible-playbook -i hosts site.yml ```
3. Got to Step 04 to login to your hosts.

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
- Replace the ```region``` with your desired region name (default is ap-south-1). Note: If you change the region you also have to select the appropriate region AMI for Phantom from list below.
- Replace ```keypair``` with your key name
- Copy your AWS key file in the ```keys``` directory
- Change the permissions on your keypair ```chmod 700 keys/your-keypair.pem ```


Create the images:
```ansible-playbook -i hosts site.yml```

Consult https://docs.aws.amazon.com/general/latest/gr/rande.html for available AWS region names

Step 03: Customize settings
---
Currently you can use variables to customize the creation of the EC2 instances or the Splunk deployment. 

Settings for EC2
--

The file ```root_vars/ec2_image_vars.yml``` contains several settings for customizing the creation of Splunk and Phantom image on AWS. The below list only shows the ones of interest for first time customization. 

```
region: ap-south-1 # AWS Region
keypair: keypair_name #your aws key pair name

demo_env: 1 # Set this to 1 if you want full demo environment setup (Work in Progress)
splunk_init: 1 # If this is set to 1 it will create Centos AWS image (to be used for splunk)
phantom_init: 1 # If this is set to 1 it will create the Phantom image from AWS marketplace
splunk_setup: 1 # Deploy standalone splunk instance
splunk_phantom_setup: 1 #Set to 1 if you want the phantom instance to be added to splunk server
phantom_setup: 1 # Set to 1 to configure phantom servers with demo settings/data
phantom_auth_token: "This will be changed automatically" #AUTO CHANGED
phantom_default_admin_pass: "This will be changed automatically"

splunk_aws:
  instance_type: t2.small
  security_group_name: splunk-servers # Change the security group name here
  security_group_desc: "Security Group for splunk Servers"
  image_ami_id: "ami-1780a878" # This is the linux Centos AMI 
  hosts_group: "splunk_servers"
  instance_name_tag: "RDAPSplunkServer" # Change this to the name you want 
  disk_size: "20" # Disk size in GB
  disk_type: "gp2" # If you want high IOPS set this to io1 (io1 - default)
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

Settings for Splunk
--
You can change the splunk related variables by editing the file ```root_vars/splunk_deployment_vars.yml``` . All apps should be under files/ directory.
```
delay_num: 100 #Generic delay
splunk_license_included: 0 # If you want to add a license file set this flag to 1. Otherwise 30 day trial is used.
splunk_license_path: "~/Splunk_Enterprise.lic" # Where to copy the Splunk license file on the remote machine (if license = 1)

splunk:
  password: Password1 # Default Splunk instance password
  install_apps: 0 # Install apps from list below. The file must exist under the files/ folder
  apps: ['splunk-app-for-infrastructure_122.tgz','splunk-add-on-for-infrastructure_122.tgz']
  install_es: 0 # Install ES premium app
  phantom_config: 1 # Configure Phantom server on Splunk

```

To show deployment information after installation has finished:
```ansible-playbook -i hosts site.yml --tags "info"```



Step 04: Login/Verify your images (Not required if all playbooks are run)
---
To login to Phantom wait for a few minutes (5-10) and then you can access the instance at 
```
https://PUBLIC_IP
Use the below credentials to login to the web interface
username: admin
password: AWS instance ID (can be found in the root_vars/ec2_image_vars.yml -> phantom_default_admin_pass)
```

To login to Splunk you can access the instance at 
```
http://PUBLIC_IP:8000
Use the below credentials to login to the web interface
username: admin
password: Password1
```

To login to the Centos or Phantom Image ssh to the public IP with the -i key option and the file name.

Examples:

- Phantom ```https://SOME_PUBLIC_IP/```
- Splunk Centos ```ssh -i "your_key.pem" centos@SOME_PUBLIC_IP```

Check the hosts file and make sure the right IPs are under the correct group. Verify on AWS the settings

Notes
---
The phantom AMI depends on the region you want to launch. Below is the list:
```
"Regions": {
                    "ap-south-1": {
                        "AMI": "ami-09a93840158ec5b96"
                    },
                    "eu-west-3": {
                        "AMI": "ami-040cb59393cca4878"
                    },
                    "eu-north-1": {},
                    "eu-west-2": {
                        "AMI": "ami-00b69a9a45c7eaf08"
                    },
                    "eu-west-1": {
                        "AMI": "ami-06208808bbe8ef7c1"
                    },
                    "ap-northeast-3": {},
                    "ap-northeast-2": {
                        "AMI": "ami-0122ca7b405c4c6f2"
                    },
                    "ap-northeast-1": {
                        "AMI": "ami-07912cf8e9bc14f79"
                    },
                    "sa-east-1": {
                        "AMI": "ami-0f13e69e99e9f1e5a"
                    },
                    "ca-central-1": {
                        "AMI": "ami-0e132362946493737"
                    },
                    "ap-east-1": {},
                    "us-gov-west-1": {},
                    "ap-southeast-1": {
                        "AMI": "ami-080372805f70ba8ab"
                    },
                    "ap-southeast-2": {
                        "AMI": "ami-0359bfa90f41e2da3"
                    },
                    "us-iso-east-1": {},
                    "eu-central-1": {
                        "AMI": "ami-01e37b8af6b40feb5"
                    },
                    "us-east-1": {
                        "AMI": "ami-06fd96560236e4999"
                    },
                    "us-east-2": {
                        "AMI": "ami-0bbe4dcad193b8cec"
                    },
                    "us-west-1": {
                        "AMI": "ami-0c423333f915db472"
                    },
                    "us-west-2": {
                        "AMI": "ami-0a110df615e0ca83d"
                    }
                }
            }
```


TODO
---
Features:

- Demo data for security and other use cases
- Setup the underlying system for workload management (systemd)
- Phantom playbook for demo for full cycle with ES notables (from A-Z)
- ES and Phantom notable events
- Phantom ES integration
- Dynamic HEC tokens
- A lot more (if time ever allows)

Ansible:
- Enhance service detection and status
- Make playbooks more atomic (Trust me this will not happen any time soon)

Appendix - 1 - Advanced usage
---


