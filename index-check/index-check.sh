#!/usr/bin/env bash

SEARCH=`bin/librecat export search --bag publication to YAML | grep "^_id:" | tr -d _id:\'\ `
BACKUP=`bin/librecat export backup --bag publication to YAML | grep "^_id:" | tr -d _id:\'\ `

echo ${SEARCH[@]} ${BACKUP[@]} | tr ' ' '\n' | sort | uniq -u