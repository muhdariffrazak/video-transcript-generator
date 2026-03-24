# ====================== BUILD STAGE ======================
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3.11-dev \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip wheel && \
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124 && \
    pip install -r requirements.txt

# ====================== FINAL STAGE ======================
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    TRANSFORMERS_CACHE=/app/cache/huggingface \
    HF_HOME=/app/cache/huggingface

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/cache/huggingface /app/temp \
    && chmod -R 777 /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

# Copy application code
COPY src/ ./src/
COPY configs/ ./configs/

# Create non-root user for security (good practice)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Pre-download models on build (optional but speeds up first run)
RUN python - <<'PY' || echo "Model download will happen on first run"
from pathlib import Path
from faster_whisper import WhisperModel

cache_dir = Path('/app/cache/huggingface')
model_dir = cache_dir / 'models--large-v3'
if model_dir.exists():
    print('Model already cached, skipping download')
else:
    model = WhisperModel('large-v3', device='cuda', compute_type='float16')
    print('Model pre-loaded successfully')
PY

VOLUME ["/app/temp", "/videos", "/output"]

# Default command
ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--help"]