#!/bin/bash

function help(){
	echo "Pilot launcher installer for ORNL Titan"
	echo "Usage: launcher_installer.sh <experiment> <base_directory> <wms_queue> [<experiment_module>] [<panda_server>]"
}

if [[ -z $* ]]; then
	help
	exit 1
fi

if [[ -z $1 ]]; then
	echo No experiment specified
	help
	exit 1
fi

if [[ -z $2 ]]; then
	echo No base directory specified
	help
	exit 1
fi

if [[ ! -w $2 ]]; then
	echo Base directory does not exist
	exit 1
fi

BASE_DIR=$2/$1/titan_utils

echo We will install the toolset into $BASE_DIR

if [[ -e $BASE_DIR ]]; then
	echo Destination directory already exists
	exit 1
fi

if [[ -z $3 ]]; then
	echo No WMS queue specified
	help
	exit 1
fi

EXPERIMENT_MODULE=ATLAS
if [[ ! -z $4 ]]; then
	EXPERIMENT_MODULE=$4
fi

PANDA_SERVER=pandaserver.cern.ch
if [[ ! -z $5 ]]; then
	PANDA_SERVER=$5
fi

mkdir -p $BASE_DIR/pilots_logs_v2_$1 $BASE_DIR/pilots_workdir_$1
#cp -r ~/dev/titan_utils/* $BASE_DIR
cp -r ./titan_utils/* $BASE_DIR
cp -r $BASE_DIR/launcher/nedm $BASE_DIR/launcher/$1
rm -rf $BASE_DIR/launcher/nedm $BASE_DIR/launcher/lsst
mv $BASE_DIR/multijob_pilot_lsst_src $BASE_DIR/multijob_pilot_$1_src

cat << EOF > $BASE_DIR/launcher/$1/core_launcher_settings.py 
experiment = "$1"
base_dir = "$BASE_DIR"
wms_queue = "$3"
experiment_module = "$EXPERIMENT_MODULE"
panda_server = "$PANDA_SERVER"
EOF

cat << EOF 
Now do not forget to create proxy and start the launcher

export LD_LIBRARY_PATH=/lustre/atlas/proj-shared/csc108/app_dir/pilot/grid_env/gfal_rhel7/current/usr/lib64:\$LD_LIBRARY_PATH
export PATH=/lustre/atlas/proj-shared/csc108/app_dir/pilot/grid_env/gfal_rhel7/current/usr/bin:\$PATH
export PATH=~/bin:\$PATH
export X509_CERT_DIR=\$HOME/grid-security2/certificates

voms-proxy-init -voms lsst:/lsst/Role=pilot -valid 48:00 -vomslife 48:00

export $1_LAUNCHER_DIR=$BASE_DIR

cd $1_LAUNCHER_DIR
EOF
