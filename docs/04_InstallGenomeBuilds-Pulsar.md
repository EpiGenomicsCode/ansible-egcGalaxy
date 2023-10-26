# Initialize Ephemeris for remote tool installation
---
-

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
