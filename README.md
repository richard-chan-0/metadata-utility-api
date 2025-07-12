# track-utility-api

## Description

This project provides a Flask-based API for managing and transforming media files using ffmpeg and mkvtoolnix. The main function of the utility is to allow users to select the preferred default audio and/or subtitle tracks for their video files, as well as to inspect and manipulate MKV file metadata.

## Features

- **Stream Inspection**: Read and list audio, subtitle, and attachment streams from video files (supports both ffmpeg and mkvtoolnix).
- **Default Track Selection**: Set default audio and subtitle tracks for all files in a directory.
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
