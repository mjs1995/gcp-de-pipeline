FROM centos:centos7

RUN yum install -y wget java-1.8.0-openjdk-devel && yum clean all

WORKDIR /install

RUN wget https://downloads.apache.org/hive/hive-standalone-metastore-3.0.0/hive-standalone-metastore-3.0.0-bin.tar.gz
RUN tar zxvf hive-standalone-metastore-3.0.0-bin.tar.gz
RUN rm -rf hive-standalone-metastore-3.0.0-bin.tar.gz
RUN mv apache-hive-metastore-3.0.0-bin metastore

RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
RUN tar zxvf hadoop-3.3.4.tar.gz
RUN rm -rf hadoop-3.3.4.tar.gz
RUN mv hadoop-3.3.4 hadoop

RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.0.32.tar.gz
RUN tar zxvf mysql-connector-j-8.0.32.tar.gz
RUN cp mysql-connector-j-8.0.32/mysql-connector-j-8.0.32.jar ./metastore/lib
RUN rm -rf mysql-connector-j-8.0.32.tar.gz mysql-connector-j-8.0.32

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
ENV HADOOP_HOME=/install/hadoop

RUN rm -f /install/metastore/lib/guava-19.0.jar \
  && cp ${HADOOP_HOME}/share/hadoop/common/lib/guava-27.0-jre.jar /install/metastore/lib \
  && cp ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws-3.3.4.jar /install/metastore/lib \
  && cp ${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk-bundle-*.jar /install/metastore/lib

COPY metastore.xml /install/metastore/conf/

VOLUME ["/user/hive/warehouse"]

WORKDIR /install/metastore

RUN bin/schematool -initSchema -dbType mysql

CMD ["/install/metastore/bin/start-metastore"]