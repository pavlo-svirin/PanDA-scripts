#!/bin/bash

DSTDIR="./panda-submission2"

set -e

/usr/local/bin/python2 -m virtualenv ${DSTDIR}
cd ${DSTDIR}
. bin/activate
pip install -U setuptools wheel pip
pip install pyyaml termcolor2

mkdir tmp
cd tmp
git clone https://github.com/PanDAWMS/panda-common.git
cd panda-common
cp setup.py setup_mod.py
# vim +'normal /data_files=[' +'normal $' +'normal vi[d' + 'wq'  setup_mod.py
vim  +'/data_files=' +'normal $' +'normal di[' +'wq'  setup_mod.py
python setup_mod.py install

cd ..
git clone https://github.com/PanDAWMS/panda-server.git
cd panda-server
# edit setup.py for user/group
cp setup.py setup_mod.py
#vim +'/data_files=[' +'normal $' +'normal di[' +'0' +'/packages=[' +'normal $' +"normal di[A'pandaserver', 'pandaserver.userinterface', 'pandaserver.taskbuffer'"  +'/install_data' +'normal dd' +'wq'  setup_mod.py
vim +'/data_files=[' +'normal $' +'normal di[' +'0' +'/packages=[' +'normal $' +"normal di[A'pandaserver', 'pandaserver.userinterface', 'pandaserver.taskbuffer'"  +'/install_data' +'normal DA}' +'wq' setup_mod.py
python setup_mod.py install

cd ../..
# installing variables
cat >> bin/activate << EOF
export PANDA_URL=http://pandawms.org:25080/server/panda #set the HTTP URL to server
export PANDA_URL_SSL=https://pandawms.org:25443/server/panda #set the HTTPS URL to server
export PYTHONPATH=${VIRTUAL_ENV}/lib/python2.7/site-packages/pandacommon:${VIRTUAL_ENV}/lib/python2.7/site-packages/pandaserver/

echo 'import os; from termcolor2 import c; print "Your CA directory is: %s" % c(os.environ["X509_CERT_DIR"]).magenta;' | python -
echo 'import os; from termcolor2 import c; print "Your PanDA Server is: %s , you can change it by setting PANDA_URL_SSL variable" % c(os.environ["PANDA_URL_SSL"]).magenta;' | python -
EOF

# offer set PANDA_SERVER/PANDA_SERVER_SSL/X509_USER_PROXY/X509_CERT_DIR variables


# install submitter

# create kill job

# create job status
