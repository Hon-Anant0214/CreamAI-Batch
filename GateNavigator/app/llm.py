from functools import lru_cache
import logging
import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

@lru_cache(maxsize=100)
def _cached_generate_response(system_prompt, user_prompt):
    """Cache responses for identical prompts."""
    return _generate_response(system_prompt, user_prompt)


def _generate_response(system_prompt, user_prompt):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

    start_time = time.perf_counter()

    try:
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

        latency_ms = (time.perf_counter() - start_time) * 1000

        usage = response.usage

        prompt_tokens = usage.prompt_tokens if usage else 0
        completion_tokens = usage.completion_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0

        logger.info(
            "llm_request model=%s latency_ms=%.2f "
            "prompt_tokens=%s completion_tokens=%s "
            "total_tokens=%s status=success",
            GROQ_MODEL,
            latency_ms,
            prompt_tokens,
            completion_tokens,
            total_tokens,
        )

        return response.choices[0].message.content or ""

    except Exception:
        latency_ms = (time.perf_counter() - start_time) * 1000

        logger.exception(
            "llm_request model=%s latency_ms=%.2f status=failed",
            GROQ_MODEL,
            latency_ms,
        )
        raise
def generate_response(system_prompt, user_prompt):
    """Return a cached response when the same prompts are repeated."""

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

    return _cached_generate_response(system_prompt, user_prompt)