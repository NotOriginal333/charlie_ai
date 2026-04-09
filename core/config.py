import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    EVALUATOR_MODEL = "llama-3.1-8b-instant"
    GENERATOR_MODEL = "llama-3.1-8b-instant"

    MAX_RETRIES_PER_WORD = 3


if not Config.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")
