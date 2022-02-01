# Starting point
---
This guide assumes a clean build of Ubuntu 20.04 LTS that you have sudo rights on. If you are using LetsEncrypt for SSL security, a registered

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
This is required for passing the sudo password to the provisioned machine. Note that Homebrew officially does NOT support the use of sshpass. This command pulls sshpass from a 3rd party source and compiles it locally. Use at your own risk.
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

## Get Galaxy-ansible playbook
