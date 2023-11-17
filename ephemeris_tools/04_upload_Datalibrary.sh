# Activate Ephemeris
. ~/ephemeris_venv/bin/activate

# Variables for each Galaxy instance
GALAXY=https://hyperion.cac.cornell.edu
APIKEY=XXXXX

#LIBRARY=data_library/blacklist.yml
#setup-data-libraries -g $GALAXY -a $APIKEY -i $LIBRARY
LIBRARY=data_library/tss.yml
setup-data-libraries -g $GALAXY -a $APIKEY -i $LIBRARY
