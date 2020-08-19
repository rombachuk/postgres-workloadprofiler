#!/bin/bash
#set -x
now=`date +%Y%m%d%H%M` 
PGWP_PACKAGE_BASE=../postgres-workloadprofiler
PGWP_INSTALL_BASE=`grep install_base $PGWP_PACKAGE_BASE/resources/configuration/pgwp.conf | awk '{print $2}'`
if [ -d "$PGWP_INSTALL_BASE" ]; then
cp -r $PGWP_INSTALL_BASE $PGWP_INSTALL_BASE-bkp-$now
mkdir $PGWP_INSTALL_BASE-bkp-$now/init.d
rm -rf $PGWP_INSTALL_BASE
fi
mkdir -p $PGWP_INSTALL_BASE
mkdir -p /var/log/pgwp
cp -r $PGWP_PACKAGE_BASE/* $PGWP_INSTALL_BASE
read -p 'Does this server have online access for pip commands (Online install) (y/n): ' confirmonline
if [ "$confirmonline" == "y" ]
then
 python3 -m env $PGWP_INSTALL_BASE/venv
 source $PGWP_INSTALL_BASE/venv/bin/activate
 pip install --upgrade pip
 pip install --upgrade psycopg2-binary
 else
 read -p 'Do you really want to perform offline install (y/n): ' confirmoffline
 if [ "$confirmoffline" == "y" ]
 then
 cp $PGWP_PACKAGE_BASE/offline/postgres-workloadprofiler-wheelhouse.tar.gz $PGWP_INSTALL_BASE
 cd $PGWP_INSTALL_BASE
 /usr/bin/tar xzvf $PGWP_INSTALL_BASE/postgres-workloadprofiler-wheelhouse.tar.gz
 /usr/bin/virtualenv $PGWP_INSTALL_BASE/venv --never-download --extra-search-dir=$PGWP_INSTALL_BASE/wheelhouse
 source $PGWP_INSTALL_BASE/venv/bin/activate
 cd -
 cd $PGWP_INSTALL_BASE/wheelhouse
 pipfile=`ls pip-*`
 setuptoolsfile=`ls setuptools-*`
 $PGWP_INSTALL_BASE/venv/bin/python $pipfile/pip install --no-index $pipfile $setuptoolsfile 
 pip install -r $PGWP_INSTALL_BASE/wheelhouse/requirements.txt --no-index --find-links $PGWP_INSTALL_BASE/wheelhouse
 cd -
 fi
fi

echo 'completed'
