from faster_whisper import WhisperModel
from pathlib import Path
from pydub import AudioSegment
import tempfile
from tqdm import tqdm
from src.audio import extract_audio

class TranscriptGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.model = WhisperModel(
            config['transcription']['model'],
            device=config['transcription']['device'],
            compute_type=config['transcription']['compute_type']
        )

    def transcribe_long_video(self, video_path: Path) -> list:
        audio_path = extract_audio(video_path)
        try:
            audio = AudioSegment.from_wav(audio_path)
            chunk_ms = self.config.get('processing', {}).get('chunk_duration', 300) * 1000
            segments = []

            for i in tqdm(range(0, len(audio), chunk_ms), desc="Transcribing chunks"):
                chunk = audio[i:i + chunk_ms]
                chunk_path = Path(tempfile.mktemp(suffix=".wav"))
                chunk.export(chunk_path, format="wav")

                chunk_segments, _ = self.model.transcribe(
                    str(chunk_path),
                    beam_size=5,
                    word_timestamps=True,
                    vad_filter=True
                )
                offset = i / 1000.0
                for seg in chunk_segments:
                    seg.start += offset
                    seg.end += offset
                    segments.append(seg)

                chunk_path.unlink()

            return segments
        finally:
            if audio_path.exists():
                audio_path.unlink()

    def save_transcript(self, segments: list, output_path: str | Path):
        output_path = Path(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                start = f"{int(seg.start//3600):02}:{int((seg.start%3600)//60):02}:{int(seg.start%60):02},{int((seg.start%1)*1000):03}"
                end = f"{int(seg.end//3600):02}:{int((seg.end%3600)//60):02}:{int(seg.end%60):02},{int((seg.end%1)*1000):03}"
                f.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n\n")