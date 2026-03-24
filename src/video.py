"""
src/video.py
Handles burning subtitles into the video at the bottom.
Preserves highest possible quality.
"""

import ffmpeg
from pathlib import Path
from typing import Optional, Dict
import yaml

def load_burn_config() -> Dict:
    """Load burn styling from config.yaml"""
    candidates = [Path("configs/config.yaml"), Path("configs/configs.yml")]
    config_path = next((path for path in candidates if path.exists()), None)
    if config_path is None:
        raise FileNotFoundError("No config file found. Expected configs/config.yaml or configs/configs.yml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("burn", {})

def burn_subtitles_into_video(
    video_path: str | Path,
    srt_path: str | Path,
    output_path: Optional[str | Path] = None,
) -> Path:
    """
    Burn subtitles into video at the bottom (YouTube-style).
    Uses high-quality settings (CRF 18 + slow preset).
    """
    video_path = Path(video_path)
    srt_path = Path(srt_path)
    
    if output_path is None:
        output_path = video_path.with_name(f"{video_path.stem}_with_subs{video_path.suffix}")
    else:
        output_path = Path(output_path)

    burn_config = load_burn_config()

    # Build ffmpeg subtitle style string
    style = (
        f"FontName={burn_config.get('font_name', 'Arial')},"
        f"FontSize={burn_config.get('font_size', 24)},"
        f"PrimaryColour={burn_config.get('primary_color', '&Hffffff')},"
        f"OutlineColour={burn_config.get('outline_color', '&H000000')},"
        f"BorderStyle={burn_config.get('border_style', 3)},"
        f"BackColour={burn_config.get('back_color', '&H80000000')},"
        f"MarginV={burn_config.get('margin_v', 20)},"
        f"Alignment={burn_config.get('alignment', 2)}"
    )

    try:
        # Input streams
        input_video = ffmpeg.input(str(video_path))

        # Output with burned subtitles
        stream = ffmpeg.output(
            input_video.video,
            input_video.audio,
            str(output_path),
            vf=f"subtitles={srt_path}:force_style='{style}'",
            acodec="copy",           # Keep original audio quality
            vcodec="libx264",        # Best quality codec
            preset="slow",           # Better compression/quality
            crf=18,                  # Visually lossless (17-23 range)
            pix_fmt="yuv420p"        # Maximum compatibility
        )

        print(f"🔥 Burning subtitles into video (this may take a while for long videos)...")
        ffmpeg.run(stream, overwrite_output=True, quiet=False)

        print(f"✅ Burned video saved to: {output_path}")
        return output_path

    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else "Unknown FFmpeg error. See logs above."
        raise RuntimeError(f"FFmpeg error while burning subtitles: {stderr}")