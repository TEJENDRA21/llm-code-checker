# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir openai requests

# Define the command to run the script
CMD ["python", "check_code.py"]
