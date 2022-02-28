# Starting point
---
- This guide assumes a clean build of Ubuntu 20.04 LTS that you have sudo rights on.
- This playbook using LetsEncrypt for SSL security, which assumes you have a properly registered DNS name.

#### Update Ubuntu with latest patches
Get list of updates for system
```
sudo apt update
```
Apply updates
```
sudo apt -y upgrade
```
Reboot system
```
sudo reboot
```

#### Open PORTS required on remote server
- 22 for SSH, this can be a different port or via VPN or similar.
- 80 for HTTP, this needs to be available to the world if you want to follow the LetsEncrypt portion of the tutorial.
- 443 for HTTPs, this needs to be available to the world if you want to follow the LetsEncrypt portion of the tutorial.
- 5671 for AMQP for Pulsar, needed if you plan to setup Pulsar for remote job running.

# Getting started
---
[ansible](https://en.wikipedia.org/wiki/Ansible_(software)) will install all required dependencies on the target server, so this section primarily refers to the dependencies required to run ansible from your local workstation.

## Install dependencies on local workstation
- Recommended to use ansible version >=2.7

#### MacOS instructions
This assumes you are managing software packages through [homebrew](https://brew.sh/)

##### ansible Install
```
brew install ansible
```
##### sshpass Install
- This is required for passing the sudo password to the provisioned machine. Note that Homebrew officially does NOT support the use of sshpass. This command pulls sshpass from a 3rd party source and compiles it locally. Use at your own risk.
- Generally you should be using SSH keys instead of passing your password over the internet.
```
brew install hudochenkov/sshpass/sshpass
```

#### Ubuntu instructions
```
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

```
sudo apt install sshpass -y
```

## Deploy production Galaxy

Download roles for ansible
```
cd galaxy/
ansible-galaxy install -p roles -r requirements.yml
```

<details>
<summary> Error in uchida.miniconda
</summary>
<br>
Miniconda version in uchida.miniconda is out of date and requires a manual update for now.

After downloading the roles, make the following change to
uchida.miniconda/vars/main.yml

> "miniconda_installer: Miniconda{{ "3" if miniconda_python == 3 or miniconda_version not in miniconda_oldversions else "" }}-py39_{{ miniconda_version }}-{{ miniconda_systems[ansible_system] }}-{{ miniconda_architecture[ansible_architecture] }}.sh"

</details>
<br>

Deploy ansible playbook
- -k allows for passing of SSH password through commandline
- -K allows for passing of sudo password through commandline

```
ansible-playbook -kK galaxy.yml
```

Note that Certbot authorization is set to 'production' by default. If you are performing development work on a server, this should be set to 'staging' to avoid hitting your Certbot certificate quota. We **strongly** recommend to keep this parameter in this mode until Galaxy is confirmed to be online and working.


Under `group_vars/galaxyservers.yml`

Staging SSL
```
certbot_environment: staging
#certbot_environment: production
```

Production SSL
```
#certbot_environment: staging
certbot_environment: production
```

#### Converting over to SSL 'production'
If you were previously set to SSL 'staging' and are now ready to move your Galaxy instance into SSL 'production', begin by removing your 'staging' certificates.
```
sudo su -
rm -r /etc/letsencrypt/live/hyperion.cac.cornell.edu/
rm -r /etc/letsencrypt/archive/hyperion.cac.cornell.edu/
```

Update your `group_vars/galaxyservers.yml` to reflect a production SSL environment and then re-run the ansible playbook.
```
ansible-playbook -kK galaxy.yml
```

## Learn More
---
- This guide closely follows this [tutorial](https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible-galaxy/tutorial.html), although differences are expected due to changes over time.
- CVMFS in Galaxy [HERE](https://training.galaxyproject.org/training-material/topics/admin/tutorials/cvmfs/tutorial.html).
- Ansible documentation [HERE](https://docs.ansible.com/)
