ec2_create
=========

Role to create an AWS instance 

Prerequisites
------------

Edit vars/main.yml
```
# vars file for ec2_create
instance_type: t2.medium
security_group_name: splunk-phantom-servers # Change the security group name here
image_ami_id: "ami-1780a878" # This is the linux Centos AMI used when no ami is passed at runtime
disk_size: "20"
keypair: key_name # This is one of my keys that i already have in AWS
region: ap-south-1 # Change the Region
count_instances: 1
aws_secret_key: ""
aws_access_key: ""
hoststring: "ansible_user=centos ansible_ssh_private_key_file=keys/splunk-dlam-mumbai.pem"
hostpath: "hosts"
hosts_group: "splunk_servers"
instance_name_tag: "BOTOServer"
```

Put any private key for ssh connection in files/
Update the private key name in vars/ under hoststring

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

export AWS_ACCESS_KEY_ID="xxx" 
export AWS_SECRET_ACCESS_KEY="xxxx"

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }
ansible-playbook -i hosts roles/server.yaml -vvv         

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
