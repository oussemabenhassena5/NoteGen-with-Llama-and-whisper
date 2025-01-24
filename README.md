# NoteGen: Automate Your Note-Taking Process With LLM

**NoteGen** is a tool designed to automate the process of generating detailed notes from YouTube video transcripts. Using Google's Gemini API and OpenAI's Whisper model, NoteGen extracts key insights, critical information, and actionable takeaways from video content, providing a concise summary formatted as bullet points.

## Features

- Extract transcripts from YouTube videos.
- Generate transcripts using OpenAI's Whisper model if transcripts are disabled.
- Summarize transcripts into comprehensive notes.
- Focus on main points, critical information, key takeaways, examples, quotes, and actionable steps.
- Easy-to-use interface powered by Streamlit.

## How It Works

1. **Extract Transcript**: NoteGen extracts the transcript of the provided YouTube video. If transcripts are disabled, it uses the Whisper model to generate the transcript.
2. **Generate Notes**: The extracted transcript is summarized using Google's Gemini API based on the provided prompt.
3. **Display Notes**: The summarized notes are displayed in a well-structured format.



## Installation

To run NoteGen locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/NoteGen.git
    cd NoteGen
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```

5. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit interface in your browser.
2. Enter the YouTube video link in the provided input field.
3. Click on the "Get Detailed Notes" button.
4. The detailed notes will be displayed below.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [PyTube](https://github.com/pytube/pytube)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Google Gemini API](https://ai.google/tools/)
