# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a directory for data
RUN mkdir -p /app/data

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the entrypoint script
CMD ["./entrypoint.sh"]
