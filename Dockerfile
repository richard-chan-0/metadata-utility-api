FROM python:3.13-slim

# Install system dependencies: ffmpeg and mkvtoolnix
RUN apt-get update && \
    apt-get install -y ffmpeg mkvtoolnix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Command to run the Flask app
CMD ["python", "ffmpeg_utility"]



