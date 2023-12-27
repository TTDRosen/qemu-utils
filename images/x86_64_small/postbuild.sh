#!/bin/bash

set -e
set -x

cp ../../../images/x86_64_small/sshd_config ${TARGET_DIR}/etc/ssh/sshd_config

pwd

cd ${TARGET_DIR}/lib/modules/*/
ln -s ../../../usr/src/linux-headers build
cd -
