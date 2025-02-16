import streamlit as st
from dotenv import load_dotenv

# Import your existing modules
from utils.logging import log_processing, save_transcript
from utils.summarization import generate_notes
from utils.transcript import (
    extract_video_id,
    get_youtube_transcript,
    transcribe_with_whisper,
)
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


def inject_custom_css():
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');
        /* Global styles */
        .stApp {
            background-color: #1c1c22;
            
        }
        
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1c1c22;
            border-right: 1px solid #334155;
        }
        
        /* Typography */
        body {
            font-family: 'JetBrains Mono';
            color:   #00ff99;;
        }
        
        /* Card styling */
        .card {
            background: #1c1c22;
            border: 1px solid #1c1c22;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
         /* Header styling */
         .header-container {
             background: #1c1c22;
             padding: 1.5rem;
             border-radius: 12px;
         border: 1px solid #1c1c22;
             display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .app-title {
            font-size: 2rem;
            font-weight: 700;
            color: #00ff99;
            margin: 0;
        }
        
        /* Button styling */
        .stButton > button {
            background: #7C3AED;
            color: #E2E8F0;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
        }
        
        .stButton > button:hover {
            background: #6D28D9;
            border: none;
        }
        
        /* Input fields */
        .stTextInput > div > div {
            background: #1c1c22;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #E2E8F0;
        }
        
        /* Selectbox */
        .stSelectbox > div > div {
            background: #1c1c22;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #E2E8F0;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background-color: #7C3AED;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #2D3748;
            border: 1px solid #334155;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            color:  #00ff99;;
        }
        
        .streamlit-expanderContent {
            background-color: #2D3748;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 1rem;
            color:  #00ff99;;
        }
        
        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 500;
            background: #1E293B;
            color:#E2E8F0;;
        }
        
        .status-success {
            background-color: #1E293B;
            color: #E2E8F0;
        }
        
        .status-warning {
            background-color: #783C00;
            color: #FDBA74;
        }
        
        .status-error {
            background-color: #7F1D1D;
            color: #FCA5A5;
        }
        
        /* Tips section */
        .tips-container {
            background: #312E81;
            border: 1px solid #4338CA;
            border-radius: 8px;
            padding: 1rem;
            margin: 1.5rem 0;
            color: #E2E8F0;
        }
        
        /* Download section */
        .download-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .download-button {
            background: #1c1c22;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 0.5rem;
            text-align: center;
            cursor: pointer;
            color: #E2E8F0;
        }
        
        /* Code block */
        .coded-text {
            background: #1c1c22;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono';
            color:  #00ff99;;
        }

        /* Override Streamlit defaults */
        .css-1544g2n {
            padding: 2rem 1rem;
        }
        
        .css-1y4p8pa {
            max-width: 100%;
            padding: 2rem;
        }

        /* Markdown text color */
        .stMarkdown {
            color: #E2E8F0;
        }
        
        /* Header text colors */
        h1 {
            color: #E2E8F0; 
        }
        
        /* Links */
        a {
            color: #7C3AED !important;
        }
        
        a:hover {
            color: #6D28D9 !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    """Enhanced main application interface."""
    st.set_page_config(
        page_title="SmartNotes AI",
        layout="wide",
        page_icon="📚",
        initial_sidebar_state="expanded",
    )
    inject_custom_css()

    # Header
    st.markdown(
        """
        <div class="header-container">
            <img src="https://cdn-icons-png.flaticon.com/512/2098/2098402.png" width="48">
            <div>
                <h1 class="app-title">SmartNotes: AI-Powered Video Insights</h1>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state
    if "process_requested" not in st.session_state:
        st.session_state.process_requested = False

    # Sidebar
    with st.sidebar:
        st.subheader("🎥 Video Configuration")

        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://youtube.com/...",
            help="Enter a valid YouTube video URL",
        )

        language = st.selectbox(
            "Output Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: f"{x.capitalize()}",
            help="Select preferred output language for notes",
        )

        if st.button(
            "⚡ Generate Smart Notes",
            use_container_width=True,
            help="Start processing the video",
        ):
            try:
                validate_api_keys()
                if not validate_youtube_url(youtube_url):
                    st.error("🚫 Invalid YouTube URL format")
                    return

                st.session_state.update(
                    {
                        "process_requested": True,
                        "youtube_url": youtube_url,
                        "language": language,
                    }
                )

            except Exception as e:
                st.error(f"⚠️ Configuration error: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Main content area
    if st.session_state.process_requested:
        display_processing_flow(
            st.session_state.youtube_url, SUPPORTED_LANGUAGES[st.session_state.language]
        )
        st.session_state.process_requested = False


def display_processing_flow(url: str, lang_code: str):
    """Enhanced processing flow with consistent styling"""
    # Video preview in sidebar
    with st.sidebar:
        with st.spinner("Loading preview..."):
            video_id = extract_video_id(url)
            if video_id:
                st.image(
                    f"http://img.youtube.com/vi/{video_id}/0.jpg",
                    use_column_width=True,
                )
            else:
                st.error("Failed to load video preview")
        st.markdown("</div>", unsafe_allow_html=True)

    # Main processing steps
    st.subheader("🔄 Processing Pipeline")
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Step 1: Transcript extraction
    with st.expander("📝 Step 1: Transcript Extraction", expanded=True):
        status_text.markdown(
            '<p class="status-badge">⏳ Extracting transcript...</p>',
            unsafe_allow_html=True,
        )
        transcript = None

        try:
            transcript = get_youtube_transcript(video_id, ["en", lang_code])
            if not transcript:
                st.warning("⚠️ Using Whisper for transcription...")
                transcript = transcribe_with_whisper(url, lang_code)

            transcript_path = save_transcript(transcript)
            progress_bar.progress(50)
            st.markdown(
                '<p class="status-badge status-success">✅ Transcript extracted</p>',
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.markdown(
                f'<p class="status-badge status-error">❌ {str(e)}</p>',
                unsafe_allow_html=True,
            )
            return

    # Step 2: Notes generation
    with st.expander("🧠 Step 2: AI Analysis", expanded=True):
        status_text.markdown(
            '<p class="status-badge">⏳ Generating notes...</p>',
            unsafe_allow_html=True,
        )

        try:
            notes = generate_notes(transcript, language=lang_code)
            progress_bar.progress(100)

            st.markdown(
                """
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="margin: 0;">🌟 Generated Notes</h3>
                        <span class="status-badge status-success">✅ Complete</span>
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(notes, unsafe_allow_html=True)

            st.markdown('<div class="download-section">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download Notes (Markdown)",
                    data=notes,
                    file_name="smart_notes.md",
                    mime="text/markdown",
                    key="download_notes",
                )
            with col2:
                st.download_button(
                    label="📥 Download Transcript",
                    data=transcript,
                    file_name="transcript.txt",
                    mime="text/plain",
                    key="download_transcript",
                )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.markdown(
                f'<p class="status-badge status-error">❌ {str(e)}</p>',
                unsafe_allow_html=True,
            )

    # Transcript viewer
    with st.expander("🔍 Raw Transcript", expanded=False):
        st.markdown('<div class="coded-text">', unsafe_allow_html=True)
        st.code(transcript, language="text")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
