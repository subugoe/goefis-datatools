#!/bin/bash

node lib/citeServer.js &

nginx #-g daemon 
#varnishd -f /etc/varnish/default.vcl -s malloc,100M -a 0.0.0.0:8085
#varnishlog
