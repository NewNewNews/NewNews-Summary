# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first (for better layer caching)
COPY requirements.txt .

# Install dependencies, including wheel, and upgrade pip for latest package support
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the gRPC port
EXPOSE 50053

# Install supervisord for running multiple processes
RUN apt-get update && apt-get install -y supervisor
RUN apt-get install -y wget unzip fonts-liberation libglib2.0-0 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 libasound2
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord to manage multiple processes
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]