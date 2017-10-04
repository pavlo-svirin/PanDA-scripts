# Script to use for submissions

## Run the following commands:


```bash
git clone https://github.com/PanDAWMS/panda-server.git

export PANDA_URL="http://panda-pilot.ccs.ornl.gov/server/panda"

export PANDA_URL_MAP="CERN,http://panda-pilot.ccs.ornl.gov/server/panda,https://panda-pilot.ccs.ornl.gov/server/panda"

export PANDA_URL_SSL="https://panda-pilot.ccs.ornl.gov/server/panda"

export PYTHONPATH=$PYTHONPATH:/lustre/atlas/proj-shared/proj-shared/nph109/titan-utils/pandaserver

git clone https://github.com/pavlo-svirin/PanDA-scripts.git

cd PanDA-scripts/LQCD
```


**modify the script according to your needs**

The most important items to modify are "transformation" which represents an executable to be run (line 30) and "jobParameters" (line 37).

**now run it:**


python date-panda-lqcd.py



"PandaID=….” lines show PanDA identifiers for the jobs submitted.




## Submission script modification instructions:



TBD




## How to control the progress



Go to : http://panda-pilot.ccs.ornl.gov/latest/job/PanDA_ID_of_the_job/

For now it is only possible to track progress per job.


To access the Monitor:

1) create a tunnel to ORNL Titan:

```bash
ssh -D8080 -N user@dtn.ccs.ornl.gov
```

2) in the configuration for a browser (example for Firefox):

Preferences -> Advanced -> Network -> Settings -> select "Manual proxy configuration", SOCKS host: "localhost", port: "8080"
