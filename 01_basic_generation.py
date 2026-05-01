#!/usr/bin/env python3
"""
01_basic_generation.py

Our first local LLM request with Ollama.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from ollama import Client, ResponseError

load_dotenv()

# Change this string to any model you already pulled with `ollama pull ...`.
# Keeping it near the top makes hardware swaps easy during the workshop.
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

# Ollama exposes an HTTP API on your own machine by default.
# This looks like a network call in Python, but the compute stays local.
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

PROMPT = (
    "In exactly 3 short bullet points, explain what Ollama is and why running a "
    "model locally can be useful for developers."
)


def main() -> None:
    client = Client(host=HOST)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly workshop assistant who explains local AI in "
                "simple language."
            ),
        },
        {"role": "user", "content": PROMPT},
    ]

    print(f"Using model: {MODEL}")
    print(f"Ollama host: {HOST}")
    print("\nPrompt:")
    print(PROMPT)
    print("\nResponse:\n")

    try:
        response = client.chat(
            model=MODEL,
            messages=messages,
            options={"temperature": 0.2},
        )
        print(response.message.content)
    except ResponseError as error:
        print(f"Ollama returned an error: {error.error}")
        print(
            f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
        )
        print(
            "If needed, edit MODEL at the top of this file or change OLLAMA_MODEL in .env."
        )
    except Exception as error:
        print(f"Couldn't reach Ollama at {HOST}: {error}")
        print(
            f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
        )


if __name__ == "__main__":
    main()
