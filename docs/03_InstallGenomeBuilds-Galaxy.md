# Install Galaxy genome builds
---
- The official Galaxy recommendation is to use CVMFS for genome builds. However for our purposes, this will not work:
  - PSU ROAR Collab does not allow for CVMFS install
  - EGC clients commonly use non-model organisms that do not exist in the Galaxy-supported CVMFS framework and the time-delay to update the system is currently not practical
- These instructions assume our primary genome build location and file path structure will be mirrored between Galaxy and all Pulsar installations.
  - For convenience sake, we will follow the folder structure established on PSU ROAR Collab


#### Install Data Managers through Ephemeris
  1. Install Ephemeris
    - Follow this [tutorial](https://training.galaxyproject.org/training-material/topics/admin/tutorials/tool-management/tutorial.html) to initialize Ephemeris
    - This can be done either locally on your workstation (recommended) or directly on the Galaxy host machine (in the event of port issues)

    ```
    python3 -m venv ~/ephemeris_venv
    . ~/ephemeris_venv/bin/activate
    pip install ephemeris
    ```

      <details>
      <summary>
      MacOS Note
      </summary>

        - XCode must be installed and licensed accepted

      ```
      sudo xcodebuild -license
      ```
      </details>

  2. Get Galaxy Admin API key
    - Galaxy Admins are defined in galaxy.yml and are set during the ansible deployment.

    1. Login to Galaxy as an Admin user
    2. Go to User -> Preferences in the top menu bar, then click on Manage API key
    3. If there is no current API key available, click on Create a new key to generate it

  3. Run Ephemeris script with API keys
    - Make sure to update the APIKEY and GALAXY URL to reflect your install

    ```
    sh ansible-egcGalaxy/ephemeris_tools/install_data_manager.sh
    ```

#### Configure Galaxy to do genome-based analysis
  1. Install data manager through Galaxy
    - Follow this [tutorial](https://training.galaxyproject.org/training-material/topics/admin/tutorials/reference-genomes/tutorial.html) to generate genome build on host Galaxy instance

  3. Update the tool_data_conf.xml file to reflect the new genome build information

  ```
  # CVMFS
  #tool_data_table_config_path: /cvmfs/data.galaxyproject.org/byhand/location/tool_data_table_conf.xml,/cvmfs/data.galaxyproject.org/managed/location/tool_data_table_conf.xml
  ```

  4. Run the Galaxy playbook to deploy genomebuild changes
  ```
  ansible-playbook -kK galaxy.yml
  ```

#### Configure Pulsar server to do genome-based analysis
1. Establish the genome build folder structure on the Pulsar host

```
sudo su galaxy
mkdir -p /storage/group/bfp2/default/00_pughlab/tool_data
```

2. Download each genome build into the folder

- sacCer3
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O sacCer3.tar.gz https://cornell.box.com/shared/static/pxkkv10lgui49o9khpxgwgxlpzoqvqhx.gz
tar xzvf sacCer3.tar.gz
```

### CVMFSexec
