#!/bin/bash

echo $X509_USER_PROXY

export X509_USER_PROXY=$X509_USER_PROXY

voms-proxy-init $* 
