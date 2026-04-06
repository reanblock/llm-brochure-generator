import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    print("Using OpenAI")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    openai = OpenAI(api_key=OPENAI_API_KEY)
    print(f"Using OpenAI with model: {MODEL}")
else:
    print("Using Ollama")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    openai = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
    print(f"Using Ollama at {OLLAMA_BASE_URL} with model: {MODEL}")
