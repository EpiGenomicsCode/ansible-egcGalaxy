# Activate Ephemeris
. ~/ephemeris_venv/bin/activate

# Variables for each Galaxy instance
GALAXY=https://hyperion.cac.cornell.edu
APIKEY=XXXXX

# Fetch genome builds
run-data-managers -g $GALAXY -a $APIKEY --config fetch-sacCer3.yml
# Generate BWA index file
run-data-managers -g $GALAXY -a $APIKEY --config build-sacCer3-bwa.yml
