import re
import tempfile

import whisper
from pytube import YouTube
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    patterns = [r"(?:v=|\/)([\w-]{11})(?:&|\?|$)", r"youtu\.be\/([\w-]{11})"]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_youtube_transcript(video_id: str, languages: list) -> str:
    """Get transcript using YouTube's native API."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return " ".join([entry["text"] for entry in transcript])
    except (TranscriptsDisabled, NoTranscriptFound):
        return None


def transcribe_with_whisper(url: str, language: str) -> str:
    """Transcribe audio using Whisper ASR."""
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
            audio_stream.download(filename=temp_file.name)
            model = whisper.load_model("base")
            result = model.transcribe(temp_file.name, language=language)

        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Whisper transcription failed: {str(e)}")
