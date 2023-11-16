# Activate Ephemeris
. ~/ephemeris_venv/bin/activate

# Variables for each Galaxy instance
GALAXY=https://hyperion.cac.cornell.edu
APIKEY=XXXXX

TOOLS=workflow_tools/corepipeline_tools.yml

shed-tools install -g $GALAXY -a $APIKEY -t $TOOLS
