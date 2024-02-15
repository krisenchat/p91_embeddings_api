# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install make and required build dependencies
RUN apt-get update && apt-get install -y make build-essential libfreetype6-dev git

# Copy the Makefile into the container
COPY Makefile .
COPY requirements.txt .

# Run make install to install the dependencies
RUN make install

# Copy the source code into the container
COPY . .
EXPOSE 8080

# Command to run the application
CMD ["make", "run"]
