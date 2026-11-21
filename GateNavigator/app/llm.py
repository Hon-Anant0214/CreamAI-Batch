import os

from dotenv import load_dotenv
from groq import Groq

# Load API key and model from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def generate_response(system_prompt, user_prompt):
    """Generate an answer using the Groq LLM."""

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    return response.choices[0].message.content
