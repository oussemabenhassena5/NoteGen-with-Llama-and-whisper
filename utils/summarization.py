from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

PROMPT_TEMPLATE = """
As an expert note-taker, analyze this video transcript and create comprehensive notes in {language}. Focus on:

1. Core concepts and main arguments
2. Key technical details and data points
3. Practical applications and examples
4. Important quotes and references
5. Actionable recommendations
6. Critical insights and conclusions

Format requirements:
- Use Markdown formatting
- Include section headers
- Use bullet points and numbered lists
- Highlight key terms in **bold**
- Keep under 1200 words
- Output language: {language}

Transcript: {transcript}
"""


def initialize_llm():
    """Initialize Groq/Llama3 model with optimal settings."""
    return ChatGroq(temperature=0.3, model_name="llama3-70b-8192", max_tokens=4000)


def generate_notes(transcript: str, language: str) -> str:
    """Generate structured notes from transcript."""
    llm = initialize_llm()
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"transcript": transcript, "language": language})
