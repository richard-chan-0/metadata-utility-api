# Metadata Utility API

## Description

This project provides a Flask-based API for managing and transforming media file metadata using tools like ffmpeg and mkvtoolnix. The utility allows users to inspect, modify, and manage metadata such as default audio/subtitle tracks, titles, and more.

## Features

- **Stream Inspection**: Read and list audio, subtitle, and attachment streams from video files (supports both ffmpeg and mkvtoolnix).
- **Default Track Selection**: Set default audio and subtitle tracks for video files.
- **Title Management**: Add or modify the title metadata of MKV files.
- **Batch Processing**: Apply changes to all files in a given directory.
- **API Endpoints**:
  - `GET /`: Health check endpoint.
  - `GET /read`: Inspect the first file in the configured directory and return its streams.
  - `POST /ffmpeg/write`: Set default audio and subtitle tracks for files using ffmpeg.
  - `POST /mkv/write`: Set default audio and subtitle tracks for MKV files using mkvpropedit.

## Usage

1. **Install dependencies**  
   Make sure you have Python 3.10+ and [ffmpeg](https://ffmpeg.org/) and [mkvtoolnix](https://mkvtoolnix.download/) installed.

   ```sh
   pip install -r requirements.txt
   ```

2. **Set environment variables**

   - `MKV_DIRECTORY`: Path to the directory containing your MKV files.

   You can use a `.env` file for convenience.

3. **Run the API**

   ```sh
   python ffmpeg_utility.py
   ```

   The API will be available at `http://localhost:5000`.

4. **Example API Requests**

   - **Inspect Streams**

     ```sh
     curl http://localhost:5000/read
     ```

   - **Set Default Tracks (ffmpeg)**

     ```sh
     curl -X POST -F "path=/path/to/files" -F "audios=[0]" -F "subtitles=[1]" http://localhost:5000/ffmpeg/write
     ```

   - **Set Default Tracks (mkvtoolnix)**

     ```sh
     curl -X POST -F "audios=[0]" -F "subtitles=[1]" http://localhost:5000/mkv/default-tracks
     ```

   - **Set Title**

     ```sh
     curl -X POST -F "file=/path/to/file.mkv" -F "title=My Custom Title" http://localhost:5000/mkv/set-title
     ```

   - **Remove Tracks**

     ```sh
     curl -X POST -F "audios=[0]" -F "subtitles=[1]" http://localhost:5000/mkv/write
     ```

## Development

- All source code is in the [`src/`](src/) directory.
- Tests are in the [`test/`](test/) directory and use `pytest`.

## Requirements

- Python 3.10+
- Flask
- flask-cors
- ffmpeg (system dependency)
- mkvtoolnix (system dependency)
- python-dotenv

## License

MIT
