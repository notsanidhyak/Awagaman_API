# Use an official Debian-based Python 3.10 image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install build tools and compilers
RUN apt-get update && \
    apt-get install -y build-essential cmake &&\
    apt-get install ffmpeg libsm6 libxext6  -y

# Install pip requirements
COPY requirements.txt .
RUN pip3 install --upgrade pip \
    && python -m pip install -r requirements.txt

# Create a non-root user with UID 5678 and grant permissions to the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

# Switch to the non-root user
USER appuser

# Expose the port your application will listen on
EXPOSE 5002

# Environment variables to control Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to start your application
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
