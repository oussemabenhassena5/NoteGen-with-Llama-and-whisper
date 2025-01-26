import os
import re


def validate_youtube_url(url: str) -> bool:
    """Validate YouTube URL format."""
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?",
        r"^https:\/\/youtu\.be\/[\w-]{11}$",
    ]
    return any(re.match(pattern, url) for pattern in patterns)


def validate_api_keys():
    """Check required environment variables."""
    if not os.getenv("GROQ_API_KEY"):
        raise EnvironmentError("GROQ_API_KEY is missing from environment variables")
