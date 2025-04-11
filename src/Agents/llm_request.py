from langchain_groq import ChatGroq

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get your GROQ API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

GROQ_API_KEY=groq_api_key
# Load environment variables

# Get your GROQ API key from environment
groq_api_key =GROQ_API_KEY

# Initialize the Groq LLM using LLaMA-3-8B
llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key=groq_api_key
)
