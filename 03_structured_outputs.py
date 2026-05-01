#!/usr/bin/env python3
"""
03_structured_outputs.py

Force a local model to return machine-readable JSON instead of a paragraph.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from ollama import Client, ResponseError
from pydantic import BaseModel, RootModel

load_dotenv()

# Smaller models can work here, but feel free to swap this for a stronger one.
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


class Attendee(BaseModel):
    name: str
    role: str
    city: str
    email: str | None
    remote: bool


class AttendeeList(RootModel[list[Attendee]]):
    """Validate a top-level JSON array of attendees."""


RAW_NOTES = """
- Maya Chen is a product manager in Singapore. Her email is maya@acme.test. She works remotely.
- Luis Gomez is a sales lead in Mexico City. He works on-site and did not share an email address.
- Aisha Rahman is a data analyst in Kuala Lumpur. Her email is aisha@acme.test. She works remotely.
""".strip()


def main() -> None:
    client = Client(host=HOST)

    prompt = f"""
Read the workshop notes below and convert them into a JSON array.

Rules:
- Return JSON only.
- Match the schema exactly.
- Use null when a value is missing.
- Do not invent any new facts.

Notes:
{RAW_NOTES}
""".strip()

    print(f"Using model: {MODEL}")
    print(f"Ollama host: {HOST}")
    print("\nRaw notes:")
    print(RAW_NOTES)

    try:
        # format=... gives Ollama a JSON schema to aim for.
        # Pydantic then validates that the response really matches our shape.
        response = client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            format=AttendeeList.model_json_schema(),
            options={"temperature": 0},
        )

        attendees = AttendeeList.model_validate_json(response.message.content)

        print("\nValidated JSON:\n")
        print(attendees.model_dump_json(indent=2))

        print("\nPython objects:\n")
        for attendee in attendees.root:
            print(attendee)
    except ResponseError as error:
        print(f"Ollama returned an error: {error.error}")
        print(
            f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
        )
        print(
            "If the model struggles with JSON, try a stronger model or keep temperature at 0."
        )
    except Exception as error:
        print(f"Couldn't validate the structured output: {error}")
        print(
            f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
        )


if __name__ == "__main__":
    main()
