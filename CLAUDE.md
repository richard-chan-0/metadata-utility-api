# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask-based API for managing and transforming media file metadata using ffmpeg and mkvtoolnix. The API provides endpoints to inspect media streams (audio, subtitle, attachments) and modify metadata such as default tracks, titles, and track selection.

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable (required)
export MKV_DIRECTORY=/path/to/media/files
```

### Running the Application
```bash
# Start the Flask API
python ffmpeg_utility.py
# API will be available at http://localhost:5000
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest test/service/mkvtoolnix/test_mkvpropedit_builder.py

# Run with verbose output
pytest -v

# Run specific test function
pytest test/service/test_ffmpeg_builder.py::test_function_name
```

### Docker
```bash
# Build Docker image
docker build -t ffmpeg-api .

# Run Docker container
docker run -p 5000:5000 -e MKV_DIRECTORY=/path/to/files ffmpeg-api
```

## Architecture

### Core Components

**Builder Pattern for Command Generation**
The codebase uses the builder pattern to construct shell commands for ffmpeg and mkvtoolnix tools:
- `FfmpegCommandBuilder` (src/service/ffmpeg_builder.py) - Builds ffmpeg commands with stream mapping and disposition flags
- `MkvPropEditCommandBuilder` (src/service/mkvtoolnix/mkvpropedit_builder.py) - Builds mkvpropedit commands to edit track flags and titles
- `MkvMergeCommandBuilder` (src/service/mkvtoolnix/mkvmerge_builder.py) - Builds mkvmerge commands to selectively merge tracks

All builders return a `Command` object (src/lib/data_types/Command.py) which wraps the command array.

**Service Layer**
- `src/service/ffmpeg.py` - Uses ffprobe to read media streams, parses JSON output, and coordinates ffmpeg operations
- `src/service/mkvtoolnix/mkvtoolnix_service.py` - Orchestrates mkvtoolnix operations (mkvpropedit for editing, mkvmerge for merging)
- `src/service/mkvtoolnix/mkvinfo_processor.py` - Processes mkvinfo output to extract stream metadata

**API Layer**
- `src/api/ffmpeg/routes.py` - Endpoint: POST /ffmpeg/write (set default tracks using ffmpeg)
- `src/api/mkvtoolnix/routes.py` - Endpoints: POST /mkv/write (edit tracks), POST /mkv/merge (merge tracks)
- `src/api/__init__.py` - Flask app factory with error handlers and /read endpoint

**Data Types**
- `src/lib/data_types/media_types.py` - Stream dataclasses: AudioStream, SubtitleStream, AttachmentStream, plus Mkv variants with track numbers
- `src/lib/data_types/Command.py` - Command wrapper for shell command arrays
- `StreamType` enum defines AUDIO, SUBTITLE, ATTACHMENT types

**Factories**
- `src/lib/factories/app_factories.py` - Creates stream objects from raw metadata
- `src/lib/factories/api_factories.py` - Creates request objects from API payloads

**Utilities**
- `src/lib/utilities/os_functions.py` - File system operations (get_files, run_shell_command, parse_path)
- `src/lib/utilities/app_functions.py` - Application-level utilities

### Key Design Patterns

**Command Pattern**: All shell operations go through the `Command` class and `run_shell_command` utility

**Factory Pattern**: Stream creation is delegated to factory functions based on media type

**Builder Pattern**: Complex command construction is handled by dedicated builder classes with fluent interface

**Track Number Mapping**: MKV files have multiple track numbering schemes:
- `stream_number` - Used by ffprobe/ffmpeg (0-indexed within stream type)
- `absolute_track_number` - Absolute position in file (mkvinfo output)
- `merge_track_number` - Used by mkvmerge (0-indexed across all tracks)

## Important Notes

- The `MKV_DIRECTORY` environment variable must be set for the /read, /mkv/write, and /mkv/merge endpoints
- The forced flag is always set to 0 in mkvpropedit operations (see src/service/mkvtoolnix/mkvpropedit_builder.py:36)
- Tests require pytest and follow the same directory structure as src/ (test/service/, test/api/, test/lib/)
- CI/CD pipeline runs pytest on all PRs and pushes to main, then builds and pushes Docker image
- System dependencies: ffmpeg and mkvtoolnix must be installed (handled by Dockerfile)
