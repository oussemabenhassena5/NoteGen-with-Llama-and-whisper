from datetime import datetime


def log_processing(url: str, language: str):
    """Log processing start with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n\n[{timestamp}] Processing: {url} | Language: {language}\n"
    with open("processing.log", "a") as f:
        f.write(log_entry)


def save_transcript(transcript: str):
    """Save transcript with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"transcripts/transcript_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(transcript)
    return filename
