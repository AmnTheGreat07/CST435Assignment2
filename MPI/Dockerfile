# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install MPI and OpenSSH server
RUN apt-get update && apt-get install -y \
    mpich \
    openssh-server \
    && apt-get clean

# Configure SSH
RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    # Allow root login
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    # Enable password authentication
    sed -i 's@#PasswordAuthentication yes@PasswordAuthentication yes@' /etc/ssh/sshd_config && \
    # Disable strict host key checking
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# Generate SSH keys and configure authorized keys for root user
RUN mkdir -p /root/.ssh && \
    ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -N "" && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Set permissions for SSH
RUN chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/authorized_keys

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose SSH port
EXPOSE 22

# Start SSH and keep the container running
CMD ["/usr/sbin/sshd", "-D"]
