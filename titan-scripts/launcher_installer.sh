#!/bin/bash

function help(){
	echo "Pilot launcher installer for ORNL Titan"
	echo "Usage: launcher_installer.sh <experiment> <base_directory> <wms_queue>"
}

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

if [[ -e $2 ]]; then
	echo Base directory already exists
	exit 1
fi

if [[ -z $3 ]]; then
	echo No WMS queue specified
	help
	exit 1
fi

mkdir -p $2/pilots_logs_v2_$1 $2/pilots_workdir_$1
cp -r ~/dev/titan_utils/* $2
cp -r $2/launcher/nedm $2/launcher/$1
rm -rf $2/launcher/nedm $2/launcher/lsst
mv $2/multijob_pilot_lsst_src $2/multijob_pilot_$1_src

cat << EOF > $2/launcher/$1/core_launcher_settings.py 
experiment = "$1"
base_dir = "$2"
wms_queue = "$3"
EOF

cat << EOF 
Now do not forget to create proxy and start the launcher

export LD_LIBRARY_PATH=/lustre/atlas/proj-shared/csc108/app_dir/pilot/grid_env/gfal_rhel7/current/usr/lib64:\$LD_LIBRARY_PATH
export PATH=/lustre/atlas/proj-shared/csc108/app_dir/pilot/grid_env/gfal_rhel7/current/usr/bin:\$PATH
export PATH=~/bin:\$PATH
export X509_CERT_DIR=\$HOME/grid-security2/certificates

voms-proxy-init -voms lsst:/lsst/Role=pilot -valid 48:00 -vomslife 48:00

export $1_LAUNCHER_DIR=$2

cd $1_LAUNCHER_DIR
EOF
