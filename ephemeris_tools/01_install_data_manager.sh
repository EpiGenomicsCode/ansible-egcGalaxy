# Activate Ephemeris
. ~/ephemeris_venv/bin/activate

# Variables for each Galaxy instance
GALAXY=https://hyperion.cac.cornell.edu
APIKEY=XXXXX

# Install data managers
## dbKey and FASTA file
shed-tools install -g $GALAXY -a $APIKEY --name data_manager_fetch_genome_dbkeys_all_fasta --owner devteam
## BWA index file builder
shed-tools install -g $GALAXY -a $APIKEY --name data_manager_bwa_mem_index_builder --owner devteam
## Twobit builder
shed-tools install -g $GALAXY -a $APIKEY --name data_manager_twobit_builder --owner devteam
## SAM FASTA index builder
shed-tools install -g $GALAXY -a $APIKEY --name data_manager_sam_fasta_index_builder --owner devteam
