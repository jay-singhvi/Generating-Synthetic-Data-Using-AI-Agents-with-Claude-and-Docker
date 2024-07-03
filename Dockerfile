# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app  ## with .dockerignore file
COPY . /app

# Copy the current directory contents into the container at /app  ## without .dockerignore file
# COPY agents.py prompts.py requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /app/data

# Make port 80 available to the world outside this container
EXPOSE 80

# Run agents.py when the container launches
CMD ["python", "agents.py"]