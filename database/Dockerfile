FROM bde2020/hive:latest
MAINTAINER mahnke@sub.uni-goettingen.de

ENV SQOOP_VERSION 1.99.7
ENV SQOOP_SERVER_EXTRA_LIB /var/lib/sqoop2/
ENV DATA_DIR /opt/data
ENV SQOOP_HOME /opt/sqoop

ENV PATH $SQOOP_HOME/bin:$PATH
ENV HADOOP_HOME /opt/hadoop-$HADOOP_VERSION
ENV REQ_BUILD wget maven

RUN apt-get update && apt-get install -y $REQ_BUILD

# Get Sqoop
RUN wget http://www-eu.apache.org/dist/sqoop/$SQOOP_VERSION/sqoop-$SQOOP_VERSION-bin-hadoop200.tar.gz && \
	tar -xzvf sqoop-$SQOOP_VERSION-bin-hadoop200.tar.gz && \
	mv sqoop-$SQOOP_VERSION-bin-hadoop200 sqoop && mkdir -p $SQOOP_SERVER_EXTRA_LIB

WORKDIR $DATA_DIR

# Get some Database connectors
RUN mvn org.apache.maven.plugins:maven-dependency-plugin:2.4:get \
    -DrepoUrl=http://www.datanucleus.org/downloads/maven2/ \
    -Dartifact=oracle:ojdbc6:11.2.0.3 -Ddest=$SQOOP_SERVER_EXTRA_LIB/ojdbc6.jar && \
    mvn org.apache.maven.plugins:maven-dependency-plugin:2.4:get \
    -DrepoUrl=http://repo1.maven.org/maven2 \
    -Dartifact=mysql:mysql-connector-java:5.1.40 \
    -Ddest=$SQOOP_SERVER_EXTRA_LIB/mysql-connector-java.jar && \
    mvn org.apache.maven.plugins:maven-dependency-plugin:2.4:get \
    -DrepoUrl=http://repo1.maven.org/maven2 \
    -Dartifact=org.hsqldb:hsqldb:2.3.4 -Ddest=$SQOOP_SERVER_EXTRA_LIB/hsqldb.jar

# Create needed directories, copy files and execute script
RUN mkdir $DATA_DIR/dumps && mkdir $DATA_DIR/scripts
COPY dumps $DATA_DIR/dumps
COPY scripts $DATA_DIR/scripts

COPY populate.sh .
RUN chmod +x populate.sh && ./populate.sh

# Clean up
WORKDIR /opt
RUN rm -rf sqoop* /root/.m2

RUN apt-get --purge remove -y $REQ_BUILD && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*
