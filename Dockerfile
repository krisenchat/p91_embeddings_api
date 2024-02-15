# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install make, build-essential, libfreetype6-dev, git, and ssh client
RUN apt-get update && \
    apt-get install -y make build-essential libfreetype6-dev git openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Assume the private key is passed as a build argument
ARG SSH_PRIVATE_KEY

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the private key to ssh
RUN echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    # Ensure private key is removed (ensure this RUN command does not fail before it happens)
    git config --global url."git@github.com:".insteadOf "https://github.com/" && \
    ssh -T git@github.com || true

# Copy the Makefile and requirements.txt into the container
COPY Makefile .
COPY requirements.txt .

# Run make install to install the dependencies
RUN make install

# Removing SSH keys
RUN rm -rf /root/.ssh

# Copy the source code into the container
COPY . .

EXPOSE 8080

# Command to run the application
CMD ["make", "run"]
