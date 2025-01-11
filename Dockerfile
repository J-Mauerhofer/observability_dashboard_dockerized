# Use a base image with Java 8 JDK
FROM openjdk:8-jdk

# Install Python, pip, and Maven
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip maven && \
    apt-get clean

# Install specific versions of numpy and matplotlib
RUN pip3 install numpy==1.24.1 matplotlib==3.7.0

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Set the default command to show help if no arguments are provided
CMD ["python3", "--help"]
