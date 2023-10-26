# Configuring the Galaxy host machine
---
- This guide assumes you have a clean build of Ubuntu 22.04 LTS with sudo rights on that will be the host of the Galaxy instance.
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

#### Development - simulate CephFS filesystem
- Ansible playbook is setup to install assuming a CephFS filesystem mount
- This must be created ahead of time in a dev-setting otherwise the postgres playbook will create the folder and lock out the galaxy service account

```
sudo su
mkdir /cephfs
chmod 755 /cephfs
```

#### Production - mount CephFS filesystem

1. Install ceph-common package:
  - Ubuntu:
      ```
      sudo apt -y install ceph-common
      ```
  - Rocky/CentOS/RHEL:
      ```
      sudo yum -y install centos-release-ceph-nautilus
      sudo yum -y install ceph-common
      ```

2. Copy the ceph.conf file and the ceph.keyring file to /etc/ceph on the client.
  - To put files in /etc/ceph you must sudo as root!

  ```
  cp ceph.client.cephfs.gdk44_0001.keyring /etc/cephfs
  cp ceph.conf /etc/cephfs
  ```

3. Make the keyring file readable only to root (mode 0400) as it contains credentials for accessing your CephFS file system.
    ```
    chmod 400 etc/cephfs/ceph.client.cephfs.gdk44_0001.keyring
    ```

4. Mount the CephFS file system on the client like this:
    ```
    mkdir /cephfs
    mount -t ceph prod-mon1.cac.cornell.edu,prod-mon2.cac.cornell.edu:/gdk44_0001 /cephfs/ -o name=cephfs.gdk44_0001
    ```

5. Verify the file system is mounted successfully
  ```
  df /cephfs
  ```

  <details>

  ```
  root@hyperion:/etc/ceph# df /cephfs
  Filesystem                           1K-blocks       Used  Available Use% Mounted on
  128.84.10.1,128.84.10.2:/gdk44_0001 4882808832 1997578240 2885230592  41% /cephfs
  ```

  </details>


# Configuring your workstation (Optional)
---
[ansible](https://en.wikipedia.org/wiki/Ansible_(software)) will install all required dependencies on the target server, so this section primarily refers to the dependencies required to run ansible from your local workstation.

You can also run ansible directly on the host machine assuming you set your host file to 'localhost'
```
localhost ansible_connection=local ansible_user=<USERID>
```

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
