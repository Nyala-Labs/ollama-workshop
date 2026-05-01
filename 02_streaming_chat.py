#!/usr/bin/env python3
"""
02_streaming_chat.py

A tiny terminal chat app that streams tokens as they are generated.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from ollama import Client, ResponseError

load_dotenv()

# Swap this model name if you pulled a different one for your hardware.
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

SYSTEM_PROMPT = (
    "You are a concise, friendly workshop assistant. "
    "Keep responses short enough to read comfortably in a terminal."
)


def main() -> None:
    # We still talk to a local HTTP server, but it lives on our own computer.
    client = Client(host=HOST)

    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"Using model: {MODEL}")
    print(f"Ollama host: {HOST}")
    print("Type a message and watch the reply stream in real time.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nSession ended.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit"}:
            print("Session ended.")
            break

        messages.append({"role": "user", "content": user_input})

        print("Assistant: ", end="", flush=True)
        assistant_reply = ""

        try:
            # stream=True tells the Python SDK to yield small chunks instead of
            # waiting for the full answer to finish first.
            stream = client.chat(model=MODEL, messages=messages, stream=True)

            for chunk in stream:
                text = chunk.message.content or ""
                assistant_reply += text
                print(text, end="", flush=True)

            print()
            messages.append({"role": "assistant", "content": assistant_reply})
            print()
        except ResponseError as error:
            print(f"\n\nOllama returned an error: {error.error}")
            print(
                f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
            )
            messages.pop()
            print()
        except Exception as error:
            print(f"\n\nCouldn't reach Ollama at {HOST}: {error}")
            print(
                f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
            )
            messages.pop()
            print()


if __name__ == "__main__":
    main()
