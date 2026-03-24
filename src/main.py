import typer
from pathlib import Path
from rich.console import Console
from src.transcribe import TranscriptGenerator
from src.video import burn_subtitles_into_video
from src.utils import load_config

app = typer.Typer()
console = Console()


@app.callback()
def main() -> None:
    """Video transcript generator CLI."""
    return None

@app.command()
def transcribe(
    video_path: Path = typer.Argument(..., help="Path to input video (e.g. /videos/my_video.mp4)"),
    output_srt: str = typer.Option(None, "--srt", "-s", help="Output path for .srt file"),
    output_video: str = typer.Option(None, "--output", "-o", help="Output path for video with burned subtitles"),
    no_burn: bool = typer.Option(False, "--no-burn", help="Generate only .srt, do not burn into video"),
):
    """
    Generate transcript and burn it into the video at the bottom.
    Works with any video length.
    """
    if not video_path.exists() and not video_path.is_absolute():
        candidate = Path("/videos") / video_path
        if candidate.exists():
            video_path = candidate

    if not video_path.exists():
        raise typer.BadParameter(
            f"Video not found: {video_path}. Use a valid host path for local runs or /videos/<file> in Docker."
        )

    console.print(f"[bold green]🚀 Processing:[/] {video_path}")

    config = load_config()
    generator = TranscriptGenerator(config)

    # Step 1: Generate transcript
    srt_path = output_srt or f"/output/{video_path.stem}.srt"
    result = generator.transcribe_long_video(video_path)
    
    # Save SRT
    generator.save_transcript(result, srt_path)
    console.print(f"[green]✅ SRT saved:[/] {srt_path}")

    # Step 2: Burn into video (default behavior)
    if not no_burn:
        burned_path = output_video or f"/output/{video_path.stem}_with_subs.mp4"
        burn_subtitles_into_video(video_path, srt_path, burned_path)

    console.print("[bold green]🎉 All done![/]")

if __name__ == "__main__":
    app()