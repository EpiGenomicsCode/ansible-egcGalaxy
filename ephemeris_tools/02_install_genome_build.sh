# Activate Ephemeris
. ~/ephemeris_venv/bin/activate

# Variables for each Galaxy instance
GALAXY=https://hyperion.cac.cornell.edu
APIKEY=XXXXX

# Fetch UCSC genome builds
run-data-managers -g $GALAXY -a $APIKEY --config genomes/build_UCSC-genome.yml

## Generate genome build from URL
#run-data-managers -g $GALAXY -a $APIKEY --config genomes/build_custom-genome.yml
