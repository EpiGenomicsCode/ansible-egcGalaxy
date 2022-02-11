
# Tool and workflow configuration

## Install Ephemeris
- This is optimally done on your local workstation, but can be run anywhere assuming you have a valid API key

#### Install through Conda
```
conda config --add channels bioconda
conda install ephemeris
```

#### Install through virtualenv on Ubuntu
Install virtualenv
```
sudo apt install virtualenv
```

Install Ephemeris into a virtual environment
```
virtualenv -p python3 ~/ephemeris_venv
. ~/ephemeris_venv/bin/activate
pip install ephemeris
```

## Get API key from galaxy
- **Must be an admin**

1. Navigate to your Galaxy homepage
2. Log in as an Admin user account
3. Go to `User -> Preferences` in the top menu bar  
4. Click on `Manage API key`
5. Click `Create a new Key` to generate a API if none currently exists
6. Copy your API key

## Auto install of tools and workflows with Ephemeris

Command for installing an individual tool
```
shed-tools install -g https://hyperion.cac.cornell.edu/ -a <API-KEY> --name bwa --owner devteam --section_label Mapping
```

Command for installing tools in batch
```
shed-tools install -g https://hyperion.cac.cornell.edu/ -a <API-KEY> -t workflow_tools.yml
```

## Organize local tools

Local tool organization is handled by the 'local_tool_conf.xml' located:
'/srv/galaxy/config'

Sample for de-barcoding:
```
<?xml version='1.0' encoding='utf-8'?>
<toolbox monitor="true" tool_path="/srv/galaxy/local_tools">
    <section id="single-cell_analysis" name="Single-cell Analysis" version="">
        <tool file="scATAC_debarcode.xml" />
    </section>
</toolbox>
```

## Learn More
---
- Ephemeris documentation [HERE](https://ephemeris.readthedocs.io/en/latest/index.html)
- Ephemeris tutorial [HERE](https://training.galaxyproject.org/training-material/topics/admin/tutorials/tool-management/tutorial.html)
