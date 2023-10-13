# Instructions to install RepeatMasker on a remote Pulsar server

## On Ubuntu 22.04 with perl 5.26.3 and python 3.6.8

### Install python dependency
```
pip install --user h5py
```


## Install RMBlast dependency
```
wget https://www.repeatmasker.org/rmblast/rmblast-2.14.1+-x64-linux.tar.gz
tar xzvf rmblast-2.14.1+-x64-linux.tar.gz
```

## Install TRF dependency
```
wget https://github.com/Benson-Genomics-Lab/TRF/releases/download/v4.09.1/trf409.linux64
# Make TRF executable by everyone
chmod 555 trf409.linux64
````

## Download DFAM library
### Full database
```
wget https://www.dfam.org/releases/Dfam_3.7/families/Dfam.h5.gz
```
### Curated only
  - Note that this comes with RepeatMasker and does not need to be downloaded unless you want to update
  
```
wget https://www.dfam.org/releases/Dfam_3.7/families/Dfam_curatedonly.h5.gz
```

## Download RepeatMasker 4.1.5
```
https://www.repeatmasker.org/RepeatMasker/RepeatMasker-4.1.5.tar.gz
tar xzvf RepeatMasker-4.1.5.tar.gz
```

## Configure RepeatMasker
```
cd RepeatMasker
perl ./configure
```

Path to TRF:
/home/testUser/trf409.linux64

Search Engine:
2

Path to RMBlast:
/home/testUser/rmblast-2.14.1/bin

- RMBlast should now be listed as configured and Default
5. Done
