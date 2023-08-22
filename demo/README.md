# Environment
- OS: Ubuntu 22.04.3 LTS
- Python: 3.10.12
- Ansible: 2.10.8

# Getting started
## Install Ubuntu
During demo, the ubuntu-22.04.3-live-server-amd64.iso was used. It can be downloaded from [here](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/22.04/ubuntu-22.04.3-live-server-amd64.iso).  

## Install dependent packages
```
sudo apt install ansible python3 python3-pip
```

## Library installation
### 1. Download the library  
Download the [pycw7-ansible](https://github.com/h3copen/pycw7-ansible) library.
```
git clone https://github.com/h3copen/pycw7-ansible.git
```

### 2. Install the library
```
cd pycw7-ansible/
python3 setup.py install
```

## Switch configuration
```
local-user test
 password simple admin123456
 authorization-attribute user-role network-admin
 service-type ssh

netconf ssh server enable
 line vty 0 15
 authentication-mode scheme
 user-role network-admin

ssh server enable
ssh user test service-type all authentication-type password
scp server enable
```
## Add switch dns name into /etc/host file
### /etc/hosts file
Add the dns mapping into /etc/hosts file, i.e.
```
172.17.8.10 test1
172.17.8.12 test2
172.17.8.11 test3
```

## Test reachability
Use Ping to test the reachability, i.e.
```
[admin@demo]# ping test1
PING test1 (172.17.8.10) 56(84) bytes of data.
64 bytes from test1 (172.17.8.10): icmp_seq=1 ttl=255 time=0.585 ms
64 bytes from test1 (172.17.8.10): icmp_seq=2 ttl=255 time=0.455 ms
^C
--- test1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.455/0.520/0.585/0.065 ms
```

## Test connection to switch
```
[root@demo]# python3
Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pycw7.comware import COM7
>>> args = dict(host='test1', username='test', password='test', port=830)
>>> device = COM7(**args)
>>> device.open()
<ncclient.manager.Manager object at 0x7f3ed5953150>
```

## Ansible configuration
### ansible.conf file
Add the path of Ansible library, in order to execute playbooks at anywhere.
1. Create the ansible config file, if it does not exist.
```
vim /etc/ansible/ansible.cfg
```
2. Fill the config file with the library path.
```
[defaults]
library = /root/pycw7-ansible/library
```

## Playbook execution
### 1. Prepare host file [hosts](hosts)
```
[all:vars]
username=test
password=test
ansible_python_interpreter=/usr/bin/python3
[switches]
test1
test2
test3
```

### 2. Prepare playbook
Take the vlans.yml for example:
```
---

  - name: VLAN Automation with Ansible on Com7 Devices
    hosts: test1 test2
    gather_facts: no
    connection: local

    tasks:

      - name: ensure VLAN 10 exists
        comware_vlan: vlanid=10 name=VLAN10_WEB descr=LOCALSEGMENT username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

      - name: ensure VLAN 20 exists
        comware_vlan: vlanid=20 name=VLAN20 state=present username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

      - name: ensure VLAN 10 does not exist
        comware_vlan: vlanid=10 state=absent username={{ username }} password={{ password }} hostname={{ inventory_hostname }}

```

### 3. Execute the playbooks
Run the ansible-playbook command to test the scripts, i.e.
```
ansible-playbook -i hosts vlans.yml 
```
**Note:** 
* Error - ansible-playbook: command not found  
The command below can help to find the correct path. After the path is located, run the command in the directory or create a soft link to the file. 
```
find / -name ansible-playbook
```
* Make sure the hosts file and playbook files in the correct directory.

The result is similar to below.
```
[admin@demo]#ansible-playbook -i hosts vlans.yml 

PLAY [VLAN Automation with Ansible on Com7 Devices] *****************************************************************************

TASK [ensure VLAN 10 exists] *******************************************************************************************************
[WARNING]: Module did not set no_log for password
changed: [test1]
changed: [test2]

TASK [ensure VLAN 20 exists] *******************************************************************************************************
changed: [test1]
changed: [test2]

TASK [ensure VLAN 10 does not exist] ***********************************************************************************************
changed: [test1]
changed: [test2]

PLAY RECAP *************************************************************************************************************************
test1                       : ok=3    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
test2                       : ok=3    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```
 





