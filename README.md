# Video Transcript Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A high-performance, GPU-accelerated Python tool for generating accurate transcripts and subtitles from videos of any length. Uses OpenAI's Whisper model (via Faster-Whisper) for fast, accurate speech-to-text conversion with optional subtitle burning.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Docker (Recommended)](#docker-recommended-quickstart)
  - [Local Setup (Optional)](#local-setup-optional)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [License](#license)
- [Author](#author)

## Features

- 🎬 **Long Video Support** - Handles videos of any length efficiently
- 🚀 **GPU Acceleration** - CUDA-optimized speech recognition with float16 compute
- 📝 **Multiple Output Formats** - Generate SRT subtitles and/or burn into video
- ⚙️ **Highly Configurable** - Full control over transcription, subtitle styling, and positioning
- 🐳 **Docker Support** - Pre-configured with NVIDIA GPU support
- 📦 **CLI Interface** - Simple command-line API powered by Typer
- 🎨 **Custom Subtitle Styling** - Configurable fonts, colors, positions, and backgrounds

## Prerequisites

### For Docker (Recommended)
- Docker 20.10+
- NVIDIA Docker Runtime
- NVIDIA GPU (CUDA 12.4 compatible)
- At least 8GB GPU VRAM (for large-v3 model)

### For Local Setup
- Python 3.11+
- CUDA 12.4 Toolkit
- cuDNN 9.x
- FFmpeg 4.4+
- 8GB+ GPU VRAM (recommended)

## Installation

### Docker (Recommended - Quickstart)

**No Python environment needed.** Docker handles all dependencies including GPU support.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd video-transcript-generator
   ```

2. **Ensure Docker and NVIDIA runtime are installed:**
   ```bash
   docker --version
   docker run --rm --runtime=nvidia nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 nvidia-smi
   ```

3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   Or use the convenience script:
   ```bash
   ./run_all.sh
   ```

4. **Place videos** in the `./videos` folder and update the video path in `docker-compose.yml`

5. **Find outputs** in the `./output` folder

That's it! No virtual environment, no Python installation needed.

### Local Setup (Optional)

**Only needed if you want to run directly on your machine without Docker.**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd video-transcript-generator
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip wheel
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python -m src.main transcribe --help
   ```

## Quick Start

### Docker (Recommended)

Edit `docker-compose.yml` and update the command:
```yaml
command: transcribe /videos/your_video.mp4 --srt /output/your_video.srt --output /output/your_video_with_subs.mp4
```

Then run:
```bash
docker-compose up
```

### Local (If using local setup)

**Transcription with SRT output only:**
```bash
python -m src.main transcribe /path/to/video.mp4 --no-burn
```

**Transcription with subtitle burning:**
```bash
python -m src.main transcribe /path/to/video.mp4 \
  --srt output.srt \
  --output output_with_subtitles.mp4
```

## Configuration

Edit `configs/configs.yml` to customize behavior:

### Transcription Settings
```yaml
transcription:
  model: "large-v3"         # Model size: tiny, small, medium, large-v3
  backend: "faster-whisper" # Speech recognition backend
  device: "cuda"            # Device: cuda or cpu
  compute_type: "float16"   # Precision: float16 or float32
```

### Subtitle Styling
```yaml
burn:
  enabled: true
  position: "bottom"        # bottom, top, middle
  font_size: 17
  primary_color: "&Hffffff"         # White
  outline_color: "&H000000"         # Black
  border_style: 3                   # Boxed style
  back_color: "&H80000000"          # Semi-transparent background
  margin_v: 20                      # Pixels from bottom
  font_name: "Arial"
  alignment: 2                      # 2 = bottom center
```

## Project Structure

```
video-transcript-generator/
├── src/                          # Source code
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── transcribe.py            # Transcription logic
│   ├── audio.py                 # Audio extraction
│   ├── video.py                 # Subtitle burning
│   ├── utils.py                 # Utilities and config loading
│   └── models/                  # Model definitions
├── configs/
│   └── configs.yml              # Configuration file
├── videos/                      # Input videos (Docker only)
├── output/                      # Generated transcripts and videos
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── run_all.sh                   # Convenience script
├── README.md                    # This file
└── LICENSE                      # MIT License

```

## Development

### Project Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| faster-whisper | ≥1.0.0 | Speech-to-text recognition |
| ffmpeg-python | ≥0.2.0 | Video/audio processing |
| pydub | ≥0.25.1 | Audio manipulation |
| typer | ≥0.12.0 | CLI framework |
| rich | ≥13.7.0 | Terminal output formatting |
| pyyaml | ≥6.0 | Configuration file parsing |
| tqdm | ≥4.66.0 | Progress bars |

### Code Style

This project aims to follow:
- PEP 8 style guidelines
- Type hints for function signatures
- Comprehensive docstrings

## Troubleshooting

### GPU Not Detected
```bash
docker run --rm --runtime=nvidia nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 nvidia-smi
```

### CUDA Out of Memory
Reduce model size in `configs.yml`:
```yaml
transcription:
  model: "small"  # Instead of large-v3
```

### FFmpeg Not Found
- **Linux:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from https://ffmpeg.org/download.html

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**muhdariffrazak**

---

**Note:** This project uses OpenAI's Whisper model. For more information about the model and its capabilities, visit [openai/whisper](https://github.com/openai/whisper).
