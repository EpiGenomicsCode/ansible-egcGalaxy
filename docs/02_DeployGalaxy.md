# Deploy production Galaxy
---
- This guide assumes you have followed the steps detailed in 01_ServerConfig
- This playbook using LetsEncrypt for SSL security, which assumes you have a properly registered DNS name.

1. Download roles for ansible
```
cd galaxy/
ansible-galaxy install -r requirements.yml
```

  <details>
  Updates to ansible.cfg allow for direct pathing of the requirements download to be set without explicitly calling it.
  </details>
  <br>

2. Deploy ansible playbook
- -k allows for passing of SSH password through commandline
- -K allows for passing of sudo password through commandline

  ```
  ansible-playbook -kK galaxy.yml
  ```

  Note that Certbot authorization is set to 'production' by default. If you are performing development work on a server, this should be set to 'staging' to avoid hitting your Certbot certificate quota. We **strongly** recommend to keep this parameter in this mode until Galaxy is confirmed to be online and working.

#### Converting over to SSL 'production'
Follow these instructions if you were previously set to SSL 'staging' and are now ready to move your Galaxy instance into SSL 'production'.

1. Remove your existing 'staging' certificates.
```
sudo su -
rm /etc/letsencrypt/renewal/hyperion.cac.cornell.edu.conf
rm -r /etc/letsencrypt/live/hyperion.cac.cornell.edu/
rm -r /etc/letsencrypt/archive/hyperion.cac.cornell.edu/
```

2. Update your `group_vars/galaxyservers.yml` to reflect a production SSL environment.

- Staging SSL
```
certbot_environment: staging
#certbot_environment: production
```

- Production SSL
```
#certbot_environment: staging
certbot_environment: production
```

3. Run the ansible playbook.
```
ansible-playbook -kK galaxy.yml
```

## Learn More
---
- This guide closely follows this [tutorial](https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible-galaxy/tutorial.html), although differences are expected due to changes over time.
- CVMFS in Galaxy [HERE](https://training.galaxyproject.org/training-material/topics/admin/tutorials/cvmfs/tutorial.html).
- Ansible documentation [HERE](https://docs.ansible.com/)
