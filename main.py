import streamlit as st
from dotenv import load_dotenv

from utils.logging import log_processing, save_transcript
from utils.summarization import generate_notes
from utils.transcript import (
    extract_video_id,
    get_youtube_transcript,
    transcribe_with_whisper,
)

# Local modules
from utils.validation import validate_api_keys, validate_youtube_url

# Configuration
load_dotenv()
SUPPORTED_LANGUAGES = {
    "english": "en",
    "arabic": "ar",
    "french": "fr",
    "german": "de",
    "italian": "it",
}


def main():
    """Main application interface."""
    st.set_page_config(page_title="SmartNotes", layout="wide")
    st.title("📝 SmartNotes: AI-Powered Video Insights")

    # Initialize session state
    if "process_requested" not in st.session_state:
        st.session_state.process_requested = False

    # Sidebar for inputs and thumbnail
    with st.sidebar:
        st.header("Configuration")
        youtube_url = st.text_input(
            "YouTube Video URL:", placeholder="https://youtube.com/..."
        )
        language = st.selectbox(
            "Output Language:", options=list(SUPPORTED_LANGUAGES.keys())
        )

        if st.button("⚡ Generate Notes"):
            try:
                validate_api_keys()
                if not validate_youtube_url(youtube_url):
                    st.error("Invalid YouTube URL format")
                    return

                # Set the flag and store parameters
                st.session_state.process_requested = True
                st.session_state.youtube_url = youtube_url
                st.session_state.language = language

            except Exception as e:
                st.error(f"Processing error: {str(e)}")

    # Process video if requested
    if st.session_state.process_requested:
        log_processing(st.session_state.youtube_url, st.session_state.language)
        process_video(
            st.session_state.youtube_url, SUPPORTED_LANGUAGES[st.session_state.language]
        )
        # Reset the flag
        st.session_state.process_requested = False


def process_video(url: str, lang_code: str):
    """Main processing pipeline."""
    # Show thumbnail in sidebar
    with st.sidebar:
        with st.spinner("🔍 Extracting video information..."):
            video_id = extract_video_id(url)
            if not video_id:
                st.error("Failed to extract video ID")
                return

            st.image(
                f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True
            )

    # Show processing status and results in main content area
    with st.spinner("📝 Extracting transcript..."):
        transcript = get_youtube_transcript(video_id, ["en", lang_code])
        if not transcript:
            st.warning("Using Whisper for transcription...")
            transcript = transcribe_with_whisper(url, lang_code)

        transcript_path = save_transcript(transcript)

    with st.spinner("🧠 Generating notes..."):
        notes = generate_notes(transcript, language=lang_code)

    st.subheader("🌟 Generated Notes")
    st.markdown(notes, unsafe_allow_html=True)
    st.success("✅ Analysis complete!")

    with st.expander("View Raw Transcript"):
        st.code(transcript)


if __name__ == "__main__":
    main()
