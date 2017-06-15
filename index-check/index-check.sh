#!/usr/bin/env bash

#Get the IDs
SEARCH=`bin/librecat export search --bag publication to YAML | grep "^_id:" | tr -d _id:\'\ `
BACKUP=`bin/librecat export backup --bag publication to YAML | grep "^_id:" | tr -d _id:\'\ `

mkdir -p ./tmp
# Remove IDs from list that are in both stores
echo ${SEARCH[@]} ${BACKUP[@]} | tr ' ' '\n' | sort | uniq -u > ./tmp/id-list.txt
# Count
LINES=`wc -l ./tmp/id-list.txt`
# Get YAML entries for IDs, that are missing in one store
echo "Got ${LINES} IDs differenc, this might take some time"
xargs -n 1 -a ./tmp/id-list.txt bin/librecat publication get > ./tmp/not-indexed.yaml
rm ./tmp/id-list.txt
