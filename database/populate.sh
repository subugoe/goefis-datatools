#!/bin/bash

for cmdfile in scripts/*.sh
do
    chmod +x $cmdfile
    exec $cmdfile
done