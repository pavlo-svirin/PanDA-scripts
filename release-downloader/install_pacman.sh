#!/bin/bash

PACMAN_INSTALL_DIR=$1

mkdir $PACMAN_INSTALL_DIR && cd $_
wget http://atlas.bu.edu/~youssef/pacman/sample_cache/tarballs/pacman-latest.tar.gz
tar -zxf pacman-latest.tar.gz
