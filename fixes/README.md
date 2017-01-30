Catmandu Fixes for the GoeFIS project
=====================================


This directory contains some [Catmandu](http://librecat.org/) fixes for the
GoeFIS project. If you want to change these files look at the
[documentation](http://librecat.org/Catmandu/#fix-language) of fixes or consult
the [cheat sheet](http://librecat.org/Catmandu/#fixes-cheat-sheet).


ldap.fix
--------

This fix can help to filter out unneeded attributes from a LDAP export. One
might need this to create a LibreCat user base from an existing directory
server. You could even apply the fix during the export process itself.

Note that the examples either use ´catmandui´ or ´perl -MCatmandu::CLI -e
"Catmandu::CLI-\>run()“´ which should both work.


### Step 1: Getting the users from the directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
perl -MCatmandu::CLI -e "Catmandu::CLI-\>run()" convert LDAP \\  
     --host "ldaps://ldaps.ugent.be:636" --password \*\*\*\*\*  \\  
     --search_filter \\(objectClass=GWDGuser\\) \\  
     --search_base 'ou=people,dc=ugent,dc=be' \\  
     --base ugentID=XXXXXXX,XXXXX,dc=ugent,dc=be \\  
     --search_filter '(objectclass=iNetOrgPerson)"' to YAML \> users.yml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 

Step 2: Convert the data using the fix

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
catmandu convert YAML --fix ldap.fix < users.yml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
