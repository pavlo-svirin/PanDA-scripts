#!/bin/bash

DIR=`readlink -f $(dirname $0)`

perl -pi.bak -e "s!reposdir=.*!reposdir=${DIR}/etc/yum.repos.d!" yum.conf
