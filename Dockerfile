# Use the official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py"]
