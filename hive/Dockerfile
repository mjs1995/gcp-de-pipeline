FROM openjdk:11-slim

ARG HADOOP_VERSION=3.2.1

RUN apt-get update && apt-get install -y curl --no-install-recommends && \
        rm -rf /var/lib/apt/lists/*

RUN curl https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz \
        | tar xvz -C /opt/  \
        && ln -s /opt/hadoop-$HADOOP_VERSION /opt/hadoop \
        && rm -r /opt/hadoop/share/doc 

RUN ln -s /opt/hadoop/share/hadoop/tools/lib/hadoop-aws* /opt/hadoop/share/hadoop/common/lib/ && \
    ln -s /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk* /opt/hadoop/share/hadoop/common/lib/

ENV HADOOP_HOME="/opt/hadoop"
ENV PATH="/opt/spark/bin:/opt/hadoop/bin:${PATH}"

RUN curl https://repo1.maven.org/maven2/org/apache/hive/hive-standalone-metastore/3.1.2/hive-standalone-metastore-3.1.2-bin.tar.gz \
        | tar xvz -C /opt/ \
        && ln -s /opt/apache-hive-metastore-3.1.2-bin /opt/hive-metastore

RUN curl -L https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar \
    -o /opt/mysql-connector-j-8.0.33.jar \
    && ln -s /opt/mysql-connector-j-8.0.33.jar /opt/hadoop/share/hadoop/common/lib/ \
    && ln -s /opt/mysql-connector-j-8.0.33.jar /opt/hive-metastore/lib/

RUN rm /opt/hive-metastore/lib/guava-19.0.jar && \
        ls -lah /opt/hadoop/share/hadoop/common/lib/ && \
        cp /opt/hadoop/share/hadoop/common/lib/guava-27.0-jre.jar /opt/hive-metastore/lib/ && \
        cp /opt/hadoop/share/hadoop/tools/lib/hadoop-aws-3.2.1.jar /opt/hive-metastore/lib/ && \
        cp /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.375.jar /opt/hive-metastore/lib/

CMD ["/opt/hive-metastore/bin/start-metastore"]