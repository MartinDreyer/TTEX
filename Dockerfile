# Use an official lightweight Python image.
FROM python:3.11-slim

# Set environment variables to ensure Python runs smoothly and logs directly to the terminal.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a deployment user
RUN adduser --disabled-password --gecos '' deployer

# Set the working directory in the container to /code.
WORKDIR /code

# Install system dependencies required for typical Python projects and additional utilities.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into our working directory /code.
COPY requirements.txt /code/

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application.
COPY . /code/

# Set workdir to /code/ttex
WORKDIR /code/ttex

# Set deployer as the owner of the /code directory
RUN chown -R deployer:deployer /code/*

# Set deployer as the user to run the application
USER deployer