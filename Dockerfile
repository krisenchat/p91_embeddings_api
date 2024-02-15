# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install make, build dependencies, and git
RUN apt-get update && apt-get install -y make build-essential libfreetype6-dev git && rm -rf /var/lib/apt/lists/*

# Use an argument for the GitHub token
ARG GITHUB_TOKEN

# Clone the private repo using HTTPS and the token for authentication
RUN pip install git+https://${GITHUB_TOKEN}:x-oauth-basic@github.com/krisenchat/encryption_manager.git

# Copy the Makefile and requirements.txt into the container
COPY Makefile .
COPY requirements.txt .

# Run make install to install the dependencies
RUN make install

# Copy the source code into the container
COPY . .

EXPOSE 8080

# Command to run the application
CMD ["make", "run"]
