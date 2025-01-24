import streamlit as st
from dotenv import load_dotenv
import os
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)
from pytube import YouTube
import tempfile
import whisper
import re
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Configure the API key for LLaMA3
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# Function to extract transcript details from YouTube videos
def extract_transcript_details(youtube_video_url, language):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            st.error("Invalid YouTube URL")
            return None
        transcript_text = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["ar", "en", "fr", "de", "it"]
        )

        transcript = " ".join([i["text"] for i in transcript_text])
        # Save the transcript to a text file
        with open("transcript.txt", "w") as f:
            f.write(transcript)
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        return generate_transcript_using_whisper(youtube_video_url, language)
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None


# Function to extract video ID from YouTube URL
def extract_video_id(url):
    video_id = None
    regex_patterns = [
        r"(?<=v=)[^#\&\?]*",
        r"(?<=be/)[^#\&\?]*",
        r"(?<=embed/)[^#\&\?]*",
        r"(?<=youtu.be/)[^#\&\?]*",
    ]
    for pattern in regex_patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(0)
            break
    return video_id


# Function to download audio from YouTube video and transcribe it using Whisper
def generate_transcript_using_whisper(youtube_video_url, language):
    try:
        yt = YouTube(youtube_video_url)
        stream = yt.streams.filter(only_audio=True).first()

        with tempfile.NamedTemporaryFile(
            suffix=".mp4", delete=False
        ) as temp_audio_file:
            stream.download(filename=temp_audio_file.name)
            audio_path = temp_audio_file.name

        # Load the Whisper model
        model = whisper.load_model("base")

        # Transcribe the audio file with the specified language
        result = model.transcribe(audio_path, language=language)
        transcript = result["text"]

        # Save the transcript to a text file
        with open("transcript.txt", "w") as f:
            f.write(transcript)

        return transcript
    except Exception as e:
        st.error(f"Error generating transcript: {e}")
        return None


# Function to generate summary using LLaMA3
def generate_llama3_content(transcript_text, prompt, language):
    try:
        llm = ChatGroq(temperature=0.2, model_name="llama3-70b-8192")

        # Define the prompt template with language variable
        template = PromptTemplate(input_variables=["language"], template=prompt)

        # Set up langchain for processing
        langchain = template + transcript_text | llm | StrOutputParser()

        # Input variables for the prompt
        prompt_input = {
            "language": language,
        }

        # Invoke langchain with input variables
        response = langchain.invoke(prompt_input)

        # Save the discussion (prompt and response)
        save_discussion(prompt, response, language, transcript_text)

        return response  # Return the response directly
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None


# Function to save the discussion with the model
def save_discussion(prompt, response, language, transcript_text):
    try:
        with open("discussion.log", "a") as f:
            f.write(f"Language: {language}\n")
            f.write(
                f"Prompt:\n{prompt}\nTranscript_text:\n{transcript_text}\n{'=' * 50}\n"
            )
            f.write(f"Response:\n{response}\n")
            f.write("=" * 50 + "\n\n")
    except Exception as e:
        st.error(f"Error saving discussion: {e}")


# Streamlit app interface
st.title("SmartNotes: AI-Powered Video Summarization")
youtube_link = st.text_input("Enter Video Link:")
language = st.selectbox(
    "Select Language:", ["english", "arabic", "french", "deutsch", "italien"]
)

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    else:
        st.error("Invalid YouTube URL. Unable to extract video ID.")

if st.button("Get Detailed Notes"):
    with st.spinner("Extracting transcript..."):
        transcript_text = extract_transcript_details(youtube_link, language)

    if transcript_text:
        # Update the prompt to include the selected language
        prompt = f"""
You are a professional note-taker with expertise in distilling key insights from video content. Your task is to generate a comprehensive, yet concise set of notes from the provided video transcript. Focus on the following:

1. Main points
2. Critical information
3. Key takeaways
4. Examples or case studies
5. Quotes or important statements
6. Actionable steps or recommendations

Make sure the notes are in {language} language ,well-structured and formatted as bullet points. The total length should not exceed 1000 words.

"""

        with st.spinner("Generating detailed notes..."):
            summary = generate_llama3_content(transcript_text, prompt, language)
            if summary:
                st.markdown("## Detailed Notes:")
                st.write(summary)
                st.success("Process completed successfully!")
            else:
                st.error("Failed to generate summary.")
    else:
        st.error("Failed to extract transcript.")
