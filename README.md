# ansible-egcGalaxy

This ansible playbook deploys a production-grade Galaxy deployment for the Cornell EpiGenomics Core Facility.

## Quickstart

#### Download dependencies
```
cd galaxy/
ansible-galaxy install -r requirements.yml
```

#### Deploy Galaxy
- -k allows for passing of SSH password through commandline
- -K allows for passing of sudo password through commandline

```
ansible-playbook -kK galaxy.yml
```
