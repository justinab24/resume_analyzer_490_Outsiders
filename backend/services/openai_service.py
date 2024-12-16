import openai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./backend/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set")

openai.api_key = OPENAI_API_KEY

def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
