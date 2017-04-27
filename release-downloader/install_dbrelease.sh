#!/bin/bash

PACMAN_DIR=$1
SW_INSTALL_AREA=$2
cd ${PACMAN_DIR}/pacman*
source setup.sh 
cd -

cd $SW_INSTALL_AREA 
pacman -allow trust-all-caches -get http://atlas.web.cern.ch/Atlas/GROUPS/DATABASE/pacman4/DBRelease:DBRelease-current.pacman
