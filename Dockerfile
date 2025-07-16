# Use an official Python base image
FROM python:3.11-slim

# Install system dependencies for OpenCV and FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create output folder
RUN mkdir -p /app/output

# Healthcheck (calls healthcheck.py)
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s CMD python healthcheck.py || exit 1

# Run the main app
#CMD ["python", "rtsp_face_detection.py"]

CMD python rtsp_face_detection.py && tail -f /dev/null
