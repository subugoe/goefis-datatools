#!/bin/bash

# Better start Hive in here
$HIVE_HOME/bin/hive --service hiveserver2 &
sleep 30

for cmdfile in scripts/*.sh
do
    chmod +x $cmdfile
    exec $cmdfile
done