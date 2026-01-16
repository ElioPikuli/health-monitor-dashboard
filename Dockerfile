# Use an official Python runtime as a parent image
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
# Set the working directory in the container
WORKDIR /app

# Install system dependencies (optional but useful)
# We add curl for healthchecks if needed later
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a directory for data (optional, but good practice to ensure permissions)
RUN mkdir -p /app/data

# Define the command to run the application
# (This will be overridden by docker-compose)
CMD ["python", "monitor.py"]
