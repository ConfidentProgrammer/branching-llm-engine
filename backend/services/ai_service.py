from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_KEY")
ai_client = genai.Client(api_key=key)