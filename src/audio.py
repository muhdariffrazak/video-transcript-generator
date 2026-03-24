import ffmpeg
from pathlib import Path
import tempfile

def extract_audio(video_path: str | Path, 
                  output_path: str | Path = None) -> Path:
    """
    Extract audio from video without touching video stream.
    Keeps original video resolution intact.
    """
    video_path = Path(video_path)
    if output_path is None:
        temp_dir = Path("/app/temp") if Path("/app/temp").exists() else None
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir=temp_dir)
        output_path = Path(tmp.name)
        tmp.close()
    
    try:
        # Use ffmpeg to extract high-quality audio (no video processing)
        stream = ffmpeg.input(str(video_path))
        stream = ffmpeg.output(stream.audio, str(output_path),
                              acodec='pcm_s16le',  # 16-bit PCM
                              ar='44100',          # Standard sample rate
                              ac=1)                # Mono for Whisper efficiency
        
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        return Path(output_path)
        
    except ffmpeg.Error as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")