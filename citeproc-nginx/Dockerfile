FROM citeac/citeproc-node

# I tried Varnish first, even had parts of the documentation written, until I noticed the
# old version shipped, doesn't do this.
# https://info.varnish-software.com/blog/caching-post-requests-with-varnish
# But I've found something similar on top of Nginx.
# https://medium.com/programming-articles/caching-post-responses-with-nginx-1c0c064bb6b0#.o7dkth3o9

MAINTAINER Christian Mahnke (mahnke@sub.uni-goettingen.de)

ENV REQ_BUILD nginx-full

ENV BUILD_DIR /tmp
  
RUN apt update \
    && apt upgrade -y \
    && apt dist-upgrade -y \
    && apt install --assume-yes --no-install-recommends ${REQ_BUILD}

COPY nginx.conf /etc/nginx/nginx.conf

COPY docker-entrypoint.sh .
RUN mkdir -p /www/root && \
    mkdir -p /www/chche && \
    chown -R www-data /www && \
    chmod +x /src/docker-entrypoint.sh 

EXPOSE 8085

CMD /src/docker-entrypoint.sh
