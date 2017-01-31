Database tool
=============

What ist does
-------------

This Docker image sets up a [Hive](https://hive.apache.org/) installation and
then executes some scripts within the context of a running instance of it.
Basically you just need to throw in scripts into the `scripts` directory and use
[Sqoop](http://sqoop.apache.org/) and Hive from there. The scripts will be made
executable and called from within `populatze.sh`. This is called during the
build. They need to have an `*.sh` extension. If you already have some data
dumps put the in the `dumps` directory, the contents there will be copied as
well, just add another script which can handle them. Currently only shell
scripts are supported. But one might try to add some Java stuff (Groovy/Jython)
to the dumps directory and write a wrapper shell script to use it as well.
