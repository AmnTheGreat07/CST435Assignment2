# Use an official Hadoop base image
FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

# Set the working directory
WORKDIR /hadoop

# Install Python and dependencies
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list && \
    sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean


# Copy Python dependencies
COPY requirements.txt /hadoop/

# Install Python packages
RUN pip3 install -r requirements.txt

# Copy Hadoop streaming jar (if not already in the base image)
COPY hadoop-streaming.jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar

# Copy application scripts
COPY mapper.py reducer.py matrix_generator.py hadoop_matrix_multiplication.py test.py /hadoop/

# Copy deployment-related files
COPY deployment.yaml service.yaml /hadoop/

# Copy initial input files
COPY matrix_A.csv matrix_B.csv /hadoop/

# Expose ports
EXPOSE 8088 50070 50075 9000

# Start Hadoop services and keep the container running
CMD ["/bin/bash", "-c", "service ssh start && hdfs namenode -format && start-dfs.sh && start-yarn.sh && tail -f /dev/null"]

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64