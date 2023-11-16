# Install Pulsar genome builds
---
- This guide provides the links required to install the RC-hardcoded genome build paths for a pulsar server

#### Configure Pulsar server to do genome-based analysis
1. Establish the genome build folder structure on the Pulsar host

```
mkdir -p /storage/group/bfp2/default/00_pughlab/tool_data
```

2. Download each genome build into the folder

- sacCer3
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O sacCer3.tar.gz https://cornell.box.com/shared/static/pxkkv10lgui49o9khpxgwgxlpzoqvqhx.gz
tar xzvf sacCer3.tar.gz
```

- hg38
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O hg38.tar.gz https://cornell.box.com/shared/static/pfav6d12alo9mwv4n5gfe5ptscs2nypn.gz
tar xzvf hg38.tar.gz
```

- hg19
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O hg19.tar.gz https://cornell.box.com/shared/static/zhgnec7fhd8x5gtn3l42eqwd69vhu5tj.gz
tar xzvf hg19.tar.gz
```

- mm10
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O mm10.tar.gz https://cornell.box.com/shared/static/3sk4jk0ubrkyu8p3g5oadlezupbnijs3.gz
tar xzvf mm10.tar.gz
```

- dm6
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O dm6.tar.gz https://cornell.box.com/shared/static/4v921mem56v3z6qyocko8xmosoznokht.gz
tar xzvf dm6.tar.gz
```

- ce10
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O ce10.tar.gz https://cornell.box.com/shared/static/xn6bm6fevokf1lx7s8wcj6sk126fiooj.gz
tar xzvf ce10.tar.gz
```

- ce11
```
cd /storage/group/bfp2/default/00_pughlab/tool_data
wget -O dm6.tar.gz https://cornell.box.com/shared/static/q6prtrstmwclyh9wh8qew8ztrif666an.gz
tar xzvf dm6.tar.gz
```
