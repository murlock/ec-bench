#!/bin/bash


# install dependencies for ubuntu 18.04 (tested with LXC)
# apt install libisal2 liberasurecode-dev build-essential python-dev git python-pip virtualenv

# install dependencies for centos:7 (tested with docker)
# yum install python-devel python-virtualenv git \
#   http://mirror2.openio.io/pub/repo/openio/sds/18.10/el/7/x86_64/liberasurecode-devel-1.5.0-1.el7.oio.x86_64.rpm \
#   http://mirror2.openio.io/pub/repo/openio/sds/18.10/el/7/x86_64/liberasurecode-1.5.0-1.el7.oio.x86_64.rpm \
#   http://mirror2.openio.io/pub/repo/openio/sds/18.10/el/7/x86_64/libisal-2.22.0-1.el7.oio.x86_64.rpm

virtualenv venv-ec-bench

source venv-ec-bench/bin/activate
pip install -U pip wheel setuptools
pip install 'eventlet>=0.18.2,!=0.18.3,!=0.20.1,!=0.21.0,<1.0.0'
pip install pyeclib
pip install git+git://github.com/open-io/oio-sds.git@4.4.3


echo how to launch bench:
echo "./venv-ec-bench/bin/python ec-bench.py"
