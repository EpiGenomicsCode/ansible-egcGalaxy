# Install Pulsar genome builds
---
- This guide

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
