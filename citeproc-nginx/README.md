Cached CSL Server
=================

This Docker image creates a instance of CSL which is enforced with an instance
of [Nginx](https://www.nginx.com/). The Idea is to speed up the repeated
generation of citations.
 

Usage
-----
Build the Dockerfile:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker build --tag csl-nginx .
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the Container:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker run -p 8085:8085 csl-nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nginx will listen on Port 8085.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
curl -v -D --header "Content-type: application/json" \
    --data @sampledata.json -X POST  \
    http://127.0.0.1:8085?responat=html\&style=modern-language-association
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use `-D`you can see the HTTP headers and check for cache hits and misses.

Advanced Usage
--------------
You can even use Docker to have the whole cache in memory, by setting the cache
path (`/www/cache`) as a `tmpfs` file system.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker run -p 8085:8085 --tmpfs /www/cache:rw,size=256m,mode=1777 csl-nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

